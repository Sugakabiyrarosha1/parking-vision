"""
Command-line script for single image prediction.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import argparse
import json
import cv2
import numpy as np
from PIL import Image

from models.model_loader import load_detection_model
from inference.single_inference import predict_image
from utils.visualization import draw_detections, draw_patch_predictions


def main():
    parser = argparse.ArgumentParser(description="Predict parking spaces on a single image")
    parser.add_argument("--model", type=str, required=True,
                       choices=['ssd', 'faster_rcnn'],
                       help="Model to use")
    parser.add_argument("--image", type=str, required=True,
                       help="Path to input image")
    parser.add_argument("--output", type=str, default="results",
                       help="Output directory")
    parser.add_argument("--conf", type=float, default=0.5,
                       help="Confidence threshold")
    parser.add_argument("--device", type=str, default="cpu",
                       choices=['cpu', 'cuda'],
                       help="Device to use")
    parser.add_argument("--layout", type=str, default=None,
                       help="Path to slot layout JSON (required for cnn_patch)")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load model
    print(f"Loading {args.model} model...")
    if args.model not in ['ssd', 'faster_rcnn']:
        raise ValueError(f"Unsupported model: {args.model}. Supported models: 'ssd', 'faster_rcnn'")
    
    model = load_detection_model(args.model, device=args.device)
    model_type = args.model
    
    # Predict
    print(f"Predicting on {args.image}...")
    result = predict_image(
        model,
        args.image,
        model_type=model_type,
        conf_threshold=args.conf,
        device=args.device
    )
    
    # Save visualization
    image_name = Path(args.image).stem
    vis_path = output_dir / f"{image_name}_result.jpg"
    
    if 'visualization' in result:
        Image.fromarray(result['visualization']).save(vis_path)
        print(f"Visualization saved to {vis_path}")
    
    # Save results JSON
    json_result = result.copy()
    if 'visualization' in json_result:
        del json_result['visualization']  # Remove large array
    
    json_path = output_dir / f"{image_name}_result.json"
    with open(json_path, 'w') as f:
        json.dump(json_result, f, indent=2)
    print(f"Results saved to {json_path}")
    
    # Print summary
    if 'num_detections' in result:
        print(f"\nDetections: {result['num_detections']}")
        for i, det in enumerate(result.get('detections', []), 1):
            print(f"  {i}. Class: {det.get('class', 'N/A')}, "
                  f"Score: {det.get('score', 0):.3f}, "
                  f"BBox: {det.get('bbox', [])}")
    elif 'num_slots' in result:
        print(f"\nSlots: {result['num_slots']}")
        print(f"Occupied: {result['num_occupied']}")


if __name__ == "__main__":
    main()

