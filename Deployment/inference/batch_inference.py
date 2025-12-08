"""
Batch inference script for parking vision deployment.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent.parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import os
from typing import List, Dict
import json
from tqdm import tqdm
import numpy as np
from PIL import Image

from inference.single_inference import predict_image
from models.model_loader import load_detection_model


def batch_predict(
    model,
    input_dir: str,
    output_dir: str,
    model_type: str = 'ssd',
    conf_threshold: float = 0.5,
    device: str = 'cpu',
    save_visualizations: bool = True,
    save_json: bool = True
):
    """
    Run batch prediction on all images in a directory.
    
    Args:
        model: Loaded model
        input_dir: Directory containing input images
        output_dir: Directory to save results
        model_type: Type of model ('ssd', 'faster_rcnn')
        conf_threshold: Confidence threshold
        device: Device ('cpu' or 'cuda')
        save_visualizations: Whether to save visualization images
        save_json: Whether to save JSON results
    
    Returns:
        List of prediction results
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if save_visualizations:
        vis_dir = output_path / 'visualizations'
        vis_dir.mkdir(exist_ok=True)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]
    
    if len(image_files) == 0:
        raise ValueError(f"No image files found in {input_dir}")
    
    results = []
    
    # Process each image
    for image_file in tqdm(image_files, desc=f"Processing images with {model_type}"):
        try:
            # Predict
            result = predict_image(
                model,
                str(image_file),
                model_type=model_type,
                conf_threshold=conf_threshold,
                device=device
            )
            
            # Save visualization
            if save_visualizations and 'visualization' in result:
                vis_file = vis_dir / f"{image_file.stem}_result.jpg"
                vis_image = result['visualization']
                Image.fromarray(vis_image).save(vis_file)
                result['visualization_path'] = str(vis_file)
            
            # Remove visualization from JSON (too large)
            if save_json:
                json_result = result.copy()
                if 'visualization' in json_result:
                    del json_result['visualization']
                
                json_file = output_path / f"{image_file.stem}_result.json"
                with open(json_file, 'w') as f:
                    json.dump(json_result, f, indent=2)
            
            results.append(result)
        
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            continue
    
    # Save summary
    summary = {
        'total_images': len(image_files),
        'processed_images': len(results),
        'model_type': model_type,
        'conf_threshold': conf_threshold,
        'total_detections': sum(r.get('num_detections', 0) for r in results),
        'results': [r for r in results if 'visualization' not in r]  # Remove large arrays
    }
    
    summary_file = output_path / 'summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return results

