"""
Single image inference functions for parking vision deployment.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent.parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import torch
import numpy as np
from typing import List, Dict, Optional
import cv2

from utils.image_utils import load_image, preprocess_image_for_detection
from utils.visualization import draw_detections, draw_patch_predictions


def predict_image(
    model,
    image_path: str,
    model_type: str = 'ssd',
    conf_threshold: float = 0.5,
    device: str = 'cpu'
) -> Dict:
    """
    Predict parking spaces on a single image using detection models.
    
    Args:
        model: Loaded model
        image_path: Path to image file
        model_type: Type of model ('ssd', 'faster_rcnn')
        conf_threshold: Confidence threshold
        device: Device ('cpu' or 'cuda')
    
    Returns:
        Dictionary with predictions and visualization
    """
    # Load image - ensure we read fresh each time
    image = load_image(image_path)
    if image is None:
        raise ValueError(f"Failed to load image from {image_path}")
    original_shape = image.shape
    
    # Ensure image is properly formatted (RGB, uint8)
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8) if image.max() <= 1.0 else image.astype(np.uint8)
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # Predict based on model type
    if model_type in ['ssd', 'faster_rcnn']:
        # PyTorch detection models
        # Ensure model is in eval mode
        if hasattr(model, 'eval'):
            model.eval()
        
        # Preprocess image - ensure fresh preprocessing (use copy to avoid modifying original)
        import copy as cp
        image_copy = cp.deepcopy(image)
        image_tensor = preprocess_image_for_detection(image_copy).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(image_tensor)
        
        detections = []
        if len(outputs) > 0 and isinstance(outputs, list):
            boxes = outputs[0]['boxes'].cpu().numpy()
            scores = outputs[0]['scores'].cpu().numpy()
            labels = outputs[0]['labels'].cpu().numpy()
            
            # Scale boxes back to original image size
            h, w = original_shape[:2]
            # Preprocessing resizes to 320x320, so we need to scale back
            scale_x = w / 320.0
            scale_y = h / 320.0
            
            for box, score, label in zip(boxes, scores, labels):
                if score >= conf_threshold:
                    # Convert to x_min, y_min, x_max, y_max format and scale
                    x_min, y_min, x_max, y_max = box
                    x_min = x_min * scale_x
                    y_min = y_min * scale_y
                    x_max = x_max * scale_x
                    y_max = y_max * scale_y
                    
                    detections.append({
                        'bbox': [float(x_min), float(y_min), float(x_max), float(y_max)],
                        'class': int(label - 1),  # Subtract 1 because 0 is background
                        'score': float(score),
                    })
    
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    # Visualize
    class_names = ["free_parking_space", "not_free_parking_space"]
    visualized = draw_detections(image, detections, class_names, conf_threshold)
    
    return {
        'image_path': str(image_path),
        'detections': detections,
        'num_detections': len(detections),
        'visualization': visualized,
        'original_shape': original_shape
    }


def predict_image_patch(
    model,
    image_path: str,
    slot_layout: List[Dict],
    patch_size: tuple = (80, 80),
    threshold: float = 0.5,
    device: str = 'cpu'
) -> Dict:
    """
    Predict parking space occupancy using CNN patch classifier.
    
    Args:
        model: Loaded CNN patch model
        image_path: Path to image file
        slot_layout: List of slot dictionaries with 'bbox' keys
        patch_size: Patch size (height, width)
        threshold: Probability threshold for occupied classification
        device: Device ('cpu' or 'cuda')
    
    Returns:
        Dictionary with predictions and visualization
    """
    # Load image
    image = load_image(image_path)
    
    predictions = []
    patch_tensors = []
    slot_bboxes = []
    
    # Extract patches
    for slot in slot_layout:
        bbox = slot.get('bbox', [])
        slot_id = slot.get('slot_id', 0)
        
        # Extract patch
        patch = extract_patch_from_image(image, bbox)
        if patch.size == 0:
            continue
        
        # Preprocess patch
        patch_tensor = preprocess_patch_for_cnn(patch, patch_size).unsqueeze(0).to(device)
        patch_tensors.append(patch_tensor)
        slot_bboxes.append({'bbox': bbox, 'slot_id': slot_id})
    
    # Batch inference
    if len(patch_tensors) > 0:
        batch = torch.cat(patch_tensors, dim=0)
        
        with torch.no_grad():
            outputs = model(batch)
            probs = torch.nn.functional.softmax(outputs, dim=1)
        
        # Process predictions
        for i, slot_info in enumerate(slot_bboxes):
            prob_occupied = probs[i, 1].item()
            predicted_occupied = prob_occupied >= threshold
            
            predictions.append({
                'slot_id': slot_info['slot_id'],
                'bbox': slot_info['bbox'],
                'prob_occupied': float(prob_occupied),
                'predicted_occupied': bool(predicted_occupied),
            })
    
    # Visualize
    visualized = draw_patch_predictions(image, predictions, threshold)
    
    return {
        'image_path': str(image_path),
        'predictions': predictions,
        'num_slots': len(predictions),
        'num_occupied': sum(p['predicted_occupied'] for p in predictions),
        'visualization': visualized
    }

