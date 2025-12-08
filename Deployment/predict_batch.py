"""
Command-line script for batch image prediction.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import argparse

from models.model_loader import load_detection_model
from inference.batch_inference import batch_predict


def main():
    parser = argparse.ArgumentParser(description="Batch prediction on multiple images")
    parser.add_argument("--model", type=str, required=True,
                       choices=['ssd', 'faster_rcnn'],
                       help="Model to use")
    parser.add_argument("--input", type=str, required=True,
                       help="Input directory containing images")
    parser.add_argument("--output", type=str, required=True,
                       help="Output directory for results")
    parser.add_argument("--conf", type=float, default=0.5,
                       help="Confidence threshold")
    parser.add_argument("--device", type=str, default="cpu",
                       choices=['cpu', 'cuda'],
                       help="Device to use")
    parser.add_argument("--no-viz", action="store_true",
                       help="Don't save visualization images")
    parser.add_argument("--no-json", action="store_true",
                       help="Don't save JSON results")
    
    args = parser.parse_args()
    
    # Load model
    print(f"Loading {args.model} model...")
    if args.model not in ['ssd', 'faster_rcnn']:
        raise ValueError(f"Unsupported model: {args.model}. Supported models: 'ssd', 'faster_rcnn'")
    
    model = load_detection_model(args.model, device=args.device)
    
    # Run batch prediction
    print(f"Processing images from {args.input}...")
    results = batch_predict(
        model,
        args.input,
        args.output,
        model_type=args.model,
        conf_threshold=args.conf,
        device=args.device,
        save_visualizations=not args.no_viz,
        save_json=not args.no_json
    )
    
    print(f"\nProcessed {len(results)} images")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()

