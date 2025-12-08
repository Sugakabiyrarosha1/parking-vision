"""
Model loading utilities for parking vision deployment.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports if not already there
DEPLOYMENT_DIR = Path(__file__).parent.parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import os
import torch
from typing import Optional, Dict, List
import json

from models.architectures import (
    build_ssd_model,
    build_faster_rcnn_model,
    NUM_DETECTION_CLASSES_WITH_BG,
    DETECTION_CLASS_NAMES
)


# Base directory (Deployment folder)
BASE_DIR = Path(__file__).parent.parent


# Model checkpoint paths (relative to Deployment folder)
CHECKPOINT_PATHS = {
    'ssd': BASE_DIR / 'checkpoints' / 'phase2_ssd_parking' / 'best_model.pt',
    'faster_rcnn': BASE_DIR / 'checkpoints' / 'phase2_faster_rcnn_parking' / 'best_model.pt',
}


def get_checkpoint_path(model_name: str) -> Path:
    """
    Get checkpoint path for a model.
    
    Args:
        model_name: Name of the model ('ssd', 'faster_rcnn')
    
    Returns:
        Path to checkpoint file
    """
    model_name = model_name.lower()
    if model_name not in CHECKPOINT_PATHS:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(CHECKPOINT_PATHS.keys())}")
    
    path = CHECKPOINT_PATHS[model_name]
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    
    return path


def load_detection_model(model_name: str, device: str = 'cpu', checkpoint_path: Optional[Path] = None):
    """
    Load a detection model (SSD or Faster R-CNN).
    
    Args:
        model_name: Name of the model ('ssd', 'faster_rcnn')
        device: Device to load model on ('cpu' or 'cuda')
        checkpoint_path: Optional custom checkpoint path
    
    Returns:
        Loaded model in evaluation mode
    """
    model_name = model_name.lower()
    device = torch.device(device)
    
    # Build detection models
    if model_name == 'ssd':
        model = build_ssd_model(num_classes=NUM_DETECTION_CLASSES_WITH_BG, pretrained=False)
    elif model_name == 'faster_rcnn':
        model = build_faster_rcnn_model(num_classes=NUM_DETECTION_CLASSES_WITH_BG, pretrained=False)
    else:
        raise ValueError(f"Unknown detection model: {model_name}. Supported: 'ssd', 'faster_rcnn'")
    
    # Load checkpoint
    if checkpoint_path is None:
        checkpoint_path = get_checkpoint_path(model_name)
    
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    # Handle different checkpoint formats
    if isinstance(checkpoint, dict):
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        elif 'state_dict' in checkpoint:
            model.load_state_dict(checkpoint['state_dict'])
        else:
            # Assume the whole dict is the state_dict
            model.load_state_dict(checkpoint)
    else:
        model.load_state_dict(checkpoint)
    
    model.to(device)
    model.eval()
    
    return model


def list_available_models() -> Dict[str, Dict]:
    """
    List all available models and their checkpoint status.
    
    Returns:
        Dictionary with model information
    """
    models_info = {}
    
    for model_name, path in CHECKPOINT_PATHS.items():
        exists = path.exists()
        info = {
            'name': model_name,
            'checkpoint_path': str(path),
            'exists': exists,
            'type': 'detection'
        }
        
        if exists:
            try:
                size = path.stat().st_size / (1024 * 1024)  # Size in MB
                info['size_mb'] = round(size, 2)
            except:
                info['size_mb'] = None
        
        models_info[model_name] = info
    
    return models_info


def get_model_info(model_name: str) -> Dict:
    """
    Get detailed information about a specific model.
    
    Args:
        model_name: Name of the model
    
    Returns:
        Dictionary with model information
    """
    all_models = list_available_models()
    if model_name not in all_models:
        raise ValueError(f"Unknown model: {model_name}")
    
    info = all_models[model_name].copy()
    
    # Add class information
    info['classes'] = DETECTION_CLASS_NAMES
    info['num_classes'] = NUM_DETECTION_CLASSES_WITH_BG
    
    return info

