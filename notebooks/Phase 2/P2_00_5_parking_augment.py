from pathlib import Path
import random
import xml.etree.ElementTree as ET
from typing import Tuple, List, Dict
import json

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
import albumentations as A


# Crop regions for each parking lot
CROP_REGIONS = {
    "UFPR04": (200, 0, 1100, 720),
    "UFPR05": (80, 30, 1200, 720),
    "PUCPR": (300, 180, 1200, 600),
}


def parse_parking_xml(xml_path: Path):
    """Parse PKLot XML file and return parking spaces."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    parking_id = root.attrib.get("id", "")
    
    spaces = []
    for space_el in root.findall("space"):
        sid = int(space_el.attrib["id"])
        
        if "occupied" in space_el.attrib:
            occupied = bool(int(space_el.attrib["occupied"]))
        else:
            occupied_el = space_el.find("occupied")
            occupied = bool(int(occupied_el.text or "0")) if occupied_el is not None else False
        
        contour_pts = []
        contour_el = space_el.find("contour")
        if contour_el is not None:
            for pt in contour_el.findall("point"):
                x = int(pt.attrib["x"])
                y = int(pt.attrib["y"])
                contour_pts.append((x, y))
        
        spaces.append({
            "id": sid,
            "occupied": occupied,
            "contour": contour_pts,
        })
    
    return parking_id, spaces


def polygon_to_bbox(contour: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Convert polygon contour to axis-aligned bounding box (x_min, y_min, x_max, y_max)."""
    if not contour:
        return (0, 0, 0, 0)
    
    xs = [pt[0] for pt in contour]
    ys = [pt[1] for pt in contour]
    return (min(xs), min(ys), max(xs), max(ys))


def get_lot_name(img_path: Path) -> str:
    """Extract parking lot name from image path."""
    for part in img_path.parts:
        part_upper = part.upper()
        if "UFPR04" in part_upper:
            return "UFPR04"
        elif "UFPR05" in part_upper:
            return "UFPR05"
        elif "PUCPR" in part_upper:
            return "PUCPR"
    return None


def create_augmented_dataset(
    data_root: Path,
    output_dir: Path,
    target_size: Tuple[int, int] = (640, 640),
    num_augmentations: int = 3,
    random_seed: int = 42,
):
    """
    Create an augmented parking lot dataset.
    
    Parameters
    ----------
    data_root : Path
        Root directory of PKLot dataset
    output_dir : Path
        Output directory for the new dataset
    target_size : (width, height)
        Target size for output images
    num_augmentations : int
        Number of augmented versions per original image (including original)
    random_seed : int
        Random seed for reproducibility
    """
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Create output directories
    output_dir = Path(output_dir)
    images_dir = output_dir / "images"
    annotations_dir = output_dir / "annotations"
    images_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    all_images = sorted(data_root.rglob("*.jpg"))
    print(f"Found {len(all_images)} images")
    
    # Define augmentation pipeline with rotation
    transform = A.Compose([
        A.Rotate(limit=45, border_mode=0, p=0.5),  # Rotate up to ±15 degrees
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.5),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
        A.GaussianBlur(blur_limit=(3, 5), p=0.3),
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels'], min_area=10, min_visibility=0.3))
    
    dataset_info = []
    img_counter = 0
    
    # Process each image
    for img_idx, img_path in enumerate(all_images):
        if img_idx % 100 == 0:
            print(f"Processing image {img_idx}/{len(all_images)}...")
        
        # Get lot name and crop region
        lot_name = get_lot_name(img_path)
        if lot_name not in CROP_REGIONS:
            continue
        
        crop_x1, crop_y1, crop_x2, crop_y2 = CROP_REGIONS[lot_name]
        
        # Load image and XML
        xml_path = img_path.with_suffix(".xml")
        if not xml_path.exists():
            continue
        
        try:
            img = Image.open(img_path).convert("RGB")
            parking_id, spaces = parse_parking_xml(xml_path)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
        
        # Crop image
        cropped_img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
        
        # Filter and convert spaces to bboxes in cropped coordinates
        bboxes = []
        labels = []
        for space in spaces:
            bbox_abs = polygon_to_bbox(space["contour"])
            x1, y1, x2, y2 = bbox_abs
            
            # Convert to cropped coordinates
            x1_crop = x1 - crop_x1
            y1_crop = y1 - crop_y1
            x2_crop = x2 - crop_x1
            y2_crop = y2 - crop_y1
            
            # Check if bbox is within cropped region
            if x2_crop > 0 and y2_crop > 0 and x1_crop < (crop_x2 - crop_x1) and y1_crop < (crop_y2 - crop_y1):
                # Clip to crop boundaries
                x1_crop = max(0, x1_crop)
                y1_crop = max(0, y1_crop)
                x2_crop = min(crop_x2 - crop_x1, x2_crop)
                y2_crop = min(crop_y2 - crop_y1, y2_crop)
                
                if x2_crop > x1_crop and y2_crop > y1_crop:
                    bboxes.append([x1_crop, y1_crop, x2_crop, y2_crop])
                    labels.append(1 if space["occupied"] else 0)
        
        if len(bboxes) == 0:
            continue
        
        # Create augmented versions
        for aug_idx in range(num_augmentations):
            img_array = np.array(cropped_img)
            current_bboxes = bboxes.copy()
            current_labels = labels.copy()
            
            # Apply augmentation (skip for first iteration to keep original)
            if aug_idx > 0:
                try:
                    augmented = transform(
                        image=img_array,
                        bboxes=current_bboxes,
                        class_labels=current_labels
                    )
                    img_array = augmented['image']
                    current_bboxes = augmented['bboxes']
                    current_labels = augmented['class_labels']
                    
                    # Filter out any invalid bboxes after augmentation
                    valid_bboxes = []
                    valid_labels = []
                    for bbox, label in zip(current_bboxes, current_labels):
                        x1, y1, x2, y2 = bbox
                        # Ensure bbox is valid and within image bounds
                        if x2 > x1 and y2 > y1 and x1 >= 0 and y1 >= 0:
                            valid_bboxes.append([x1, y1, x2, y2])
                            valid_labels.append(label)
                    
                    current_bboxes = valid_bboxes
                    current_labels = valid_labels
                    
                    # Skip if no valid boxes remain
                    if len(current_bboxes) == 0:
                        continue
                        
                except Exception as e:
                    print(f"Augmentation failed for {img_path}, aug {aug_idx}: {e}")
                    continue
            
            # Resize to target size
            pil_img = Image.fromarray(img_array)
            orig_w, orig_h = pil_img.size
            pil_img_resized = pil_img.resize(target_size, Image.LANCZOS)
            
            # Scale bboxes
            scale_x = target_size[0] / orig_w
            scale_y = target_size[1] / orig_h
            
            scaled_bboxes = []
            for bbox, label in zip(current_bboxes, current_labels):
                x1, y1, x2, y2 = bbox
                scaled_bboxes.append({
                    "bbox": [
                        int(x1 * scale_x),
                        int(y1 * scale_y),
                        int(x2 * scale_x),
                        int(y2 * scale_y)
                    ],
                    "occupied": bool(label)
                })
            
            # Save image and annotation
            img_name = f"img_{img_counter:06d}.jpg"
            ann_name = f"img_{img_counter:06d}.json"
            
            pil_img_resized.save(images_dir / img_name, quality=95)
            
            annotation = {
                "image_name": img_name,
                "image_size": list(target_size),
                "original_image": str(img_path.relative_to(data_root)),
                "parking_lot": lot_name,
                "augmentation_index": aug_idx,
                "spaces": scaled_bboxes
            }
            
            with open(annotations_dir / ann_name, 'w') as f:
                json.dump(annotation, f, indent=2)
            
            dataset_info.append({
                "image": img_name,
                "annotation": ann_name,
                "num_spaces": len(scaled_bboxes),
                "num_occupied": sum(1 for s in scaled_bboxes if s["occupied"])
            })
            
            img_counter += 1
    
    # Save dataset summary
    with open(output_dir / "dataset_info.json", 'w') as f:
        json.dump({
            "num_images": len(dataset_info),
            "target_size": target_size,
            "num_augmentations": num_augmentations,
            "images": dataset_info
        }, f, indent=2)
    
    print(f"\nDataset creation complete!")
    print(f"Total images: {len(dataset_info)}")
    print(f"Output directory: {output_dir}")


def visualize_sample(output_dir: Path, num_samples: int = 3):
    """Visualize random samples from the created dataset."""
    output_dir = Path(output_dir)
    images_dir = output_dir / "images"
    annotations_dir = output_dir / "annotations"
    
    # Get all annotations
    ann_files = sorted(annotations_dir.glob("*.json"))
    if not ann_files:
        print("No annotations found!")
        return
    
    # Sample random annotations
    samples = random.sample(ann_files, min(num_samples, len(ann_files)))
    
    fig, axes = plt.subplots(1, len(samples), figsize=(6 * len(samples), 6))
    if len(samples) == 1:
        axes = [axes]
    
    for ax, ann_file in zip(axes, samples):
        with open(ann_file, 'r') as f:
            annotation = json.load(f)
        
        img_path = images_dir / annotation["image_name"]
        img = Image.open(img_path)
        
        ax.imshow(img)
        
        # Draw bboxes
        for space in annotation["spaces"]:
            x1, y1, x2, y2 = space["bbox"]
            color = 'red' if space["occupied"] else 'lime'
            rect = plt.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                linewidth=2, edgecolor=color, facecolor='none'
            )
            ax.add_patch(rect)
        
        ax.set_title(f"{annotation['parking_lot']} (aug {annotation['augmentation_index']})")
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    DATA_ROOT = Path("PKLot/PKLot")
    OUTPUT_DIR = Path("parking_dataset_augmented")
    
    # Create dataset
    create_augmented_dataset(
        data_root=DATA_ROOT,
        output_dir=OUTPUT_DIR,
        target_size=(640, 640),
        num_augmentations=3,  # Original + 2 augmented versions
        random_seed=42
    )
    
    # Visualize samples
    visualize_sample(OUTPUT_DIR, num_samples=3)