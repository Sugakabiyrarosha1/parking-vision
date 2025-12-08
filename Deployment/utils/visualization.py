"""
Visualization utilities for parking vision deployment.
"""

import cv2
import numpy as np
from typing import List, Dict


def draw_detections(
    image: np.ndarray,
    detections: List[Dict],
    class_names: List[str] = None,
    conf_threshold: float = 0.5
) -> np.ndarray:
    """
    Draw bounding boxes and labels on image for detection results.
    
    Args:
        image: Image as numpy array (RGB)
        detections: List of detection dictionaries with 'bbox', 'class', 'score'
        class_names: List of class names
        conf_threshold: Confidence threshold for displaying detections
    
    Returns:
        Image with drawn detections (RGB)
    """
    if class_names is None:
        class_names = ["free_parking_space", "not_free_parking_space"]
    
    # Color map: green for free, red for occupied
    colors = {
        "free_parking_space": (0, 255, 0),  # Green
        "not_free_parking_space": (255, 0, 0),  # Red
    }
    
    img_copy = image.copy()
    
    for det in detections:
        if det.get('score', 0) < conf_threshold:
            continue
        
        bbox = det['bbox']
        class_id = det.get('class', 0)
        class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
        score = det.get('score', 0)
        
        # Get color
        color = colors.get(class_name, (255, 255, 0))
        
        # Draw bounding box
        x_min, y_min, x_max, y_max = map(int, bbox)
        cv2.rectangle(img_copy, (x_min, y_min), (x_max, y_max), color, 2)
        
        # Draw label
        label = f"{class_name}: {score:.2f}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        
        # Background for text
        cv2.rectangle(
            img_copy,
            (x_min, y_min - label_size[1] - 5),
            (x_min + label_size[0], y_min),
            color,
            -1
        )
        
        # Text
        cv2.putText(
            img_copy,
            label,
            (x_min, y_min - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
    
    return img_copy


def draw_patch_predictions(
    image: np.ndarray,
    predictions: List[Dict],
    conf_threshold: float = 0.5
) -> np.ndarray:
    """
    Draw patch predictions on image for CNN patch classifier.
    
    Args:
        image: Image as numpy array (RGB)
        predictions: List of prediction dictionaries with 'bbox', 'predicted_occupied', 'prob_occupied'
        conf_threshold: Confidence threshold for displaying predictions
    
    Returns:
        Image with drawn predictions (RGB)
    """
    img_copy = image.copy()
    
    for pred in predictions:
        if pred.get('prob_occupied', 0) < conf_threshold and pred.get('predicted_occupied', False):
            continue
        
        bbox = pred['bbox']
        predicted_occupied = pred.get('predicted_occupied', False)
        prob = pred.get('prob_occupied', 0)
        
        # Color: Green for empty, Red for occupied
        color = (0, 255, 0) if not predicted_occupied else (255, 0, 0)
        
        # Draw bounding box
        x_min, y_min, x_max, y_max = map(int, bbox)
        cv2.rectangle(img_copy, (x_min, y_min), (x_max, y_max), color, 2)
        
        # Draw label
        status = "Occupied" if predicted_occupied else "Empty"
        label = f"{status} ({prob:.2f})"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        
        # Background for text
        cv2.rectangle(
            img_copy,
            (x_min, y_min - label_size[1] - 5),
            (x_min + label_size[0], y_min),
            color,
            -1
        )
        
        # Text
        cv2.putText(
            img_copy,
            label,
            (x_min, y_min - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
    
    return img_copy



