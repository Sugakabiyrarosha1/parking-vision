"""
Image preprocessing utilities for parking vision deployment.
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from torchvision import transforms
import torch


def load_image(image_path: str) -> np.ndarray:
    """
    Load image from file path.
    
    Args:
        image_path: Path to image file
    
    Returns:
        Image as numpy array in RGB format
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def preprocess_image_for_detection(image: np.ndarray, target_size: int = 320) -> torch.Tensor:
    """
    Preprocess image for detection models (SSD, Faster R-CNN, DETR).
    
    Args:
        image: Image as numpy array (RGB)
        target_size: Target size for resizing
    
    Returns:
        Preprocessed image tensor
    """
    # Convert to PIL
    pil_image = Image.fromarray(image)
    
    # Transform
    transform = transforms.Compose([
        transforms.Resize((target_size, target_size)),
        transforms.ToTensor(),
    ])
    
    tensor = transform(pil_image)
    return tensor


def preprocess_image_for_yolo(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for YOLO (handled internally by ultralytics).
    Just return the image array.
    
    Args:
        image: Image as numpy array (RGB)
    
    Returns:
        Image array (YOLO handles preprocessing internally)
    """
    return image


def preprocess_patch_for_cnn(patch: np.ndarray, patch_size: tuple = (80, 80)) -> torch.Tensor:
    """
    Preprocess a patch for CNN patch classifier.
    
    Args:
        patch: Patch image as numpy array (RGB)
        patch_size: Target patch size (height, width)
    
    Returns:
        Preprocessed patch tensor
    """
    # Resize patch
    patch_resized = cv2.resize(patch, patch_size, interpolation=cv2.INTER_AREA)
    
    # Convert to PIL
    pil_patch = Image.fromarray(patch_resized)
    
    # Transform
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    tensor = transform(pil_patch)
    return tensor


def extract_patch_from_image(image: np.ndarray, bbox: list) -> np.ndarray:
    """
    Extract a patch from image using bounding box coordinates.
    
    Args:
        image: Full image as numpy array (RGB)
        bbox: Bounding box [x_min, y_min, x_max, y_max]
    
    Returns:
        Extracted patch as numpy array
    """
    H, W = image.shape[:2]
    x_min, y_min, x_max, y_max = map(int, bbox)
    
    # Clamp coordinates
    x_min = max(0, min(W, x_min))
    y_min = max(0, min(H, y_min))
    x_max = max(0, min(W, x_max))
    y_max = max(0, min(H, y_max))
    
    patch = image[y_min:y_max, x_min:x_max]
    return patch


def preprocess_image(image: np.ndarray, model_type: str = 'ssd', **kwargs) -> torch.Tensor:
    """
    Universal preprocessing function that routes to appropriate preprocessor.
    
    Args:
        image: Image as numpy array (RGB)
        model_type: Type of model ('ssd', 'faster_rcnn', 'detr', 'yolo', 'cnn_patch')
        **kwargs: Additional arguments for specific preprocessors
    
    Returns:
        Preprocessed image tensor or array
    """
    if model_type in ['ssd', 'faster_rcnn', 'detr']:
        target_size = kwargs.get('target_size', 320)
        return preprocess_image_for_detection(image, target_size)
    elif model_type == 'yolo':
        return preprocess_image_for_yolo(image)
    elif model_type == 'cnn_patch':
        patch_size = kwargs.get('patch_size', (80, 80))
        return preprocess_patch_for_cnn(image, patch_size)
    else:
        raise ValueError(f"Unknown model type: {model_type}")



