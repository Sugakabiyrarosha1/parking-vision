"""
FastAPI web application for parking vision deployment.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import io
import json
import numpy as np
from PIL import Image
import cv2
import torch
from pydantic import BaseModel

from models.model_loader import (
    load_detection_model,
    list_available_models,
    get_model_info
)
from inference.single_inference import predict_image
from inference.batch_inference import batch_predict
from utils.image_utils import load_image


app = FastAPI(
    title="Parking Vision API",
    description="API for parking space detection and classification",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model cache
loaded_models = {}
device = "cuda" if torch.cuda.is_available() else "cpu"


class ModelLoadRequest(BaseModel):
    model_name: str
    device: Optional[str] = "cpu"


class PredictionResponse(BaseModel):
    success: bool
    model_type: str
    num_detections: Optional[int] = None
    detections: Optional[List] = None
    predictions: Optional[List] = None
    message: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Parking Vision API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "device": device,
        "loaded_models": list(loaded_models.keys())
    }


@app.get("/models")
async def get_models():
    """List all available models."""
    models = list_available_models()
    return {
        "available_models": models,
        "loaded_models": list(loaded_models.keys())
    }


@app.get("/models/{model_name}")
async def get_model_details(model_name: str):
    """Get details about a specific model."""
    try:
        info = get_model_info(model_name)
        return info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/models/load")
async def load_model(request: ModelLoadRequest):
    """Load a model into memory."""
    model_name = request.model_name.lower()
    device_to_use = request.device or device
    
    try:
        if model_name in ['ssd', 'faster_rcnn']:
            model = load_detection_model(model_name, device=device_to_use)
        else:
            raise ValueError(f"Unknown model: {model_name}. Supported models: 'ssd', 'faster_rcnn'")
        
        loaded_models[model_name] = {
            'model': model,
            'device': device_to_use,
            'type': 'detection'
        }
        
        return {
            "success": True,
            "message": f"Model {model_name} loaded successfully",
            "device": device_to_use
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    conf_threshold: Optional[float] = Form(0.5),
    device: Optional[str] = Form(None)
):
    """
    Predict parking spaces on a single uploaded image.
    
    - **file**: Image file (JPG, PNG, etc.)
    - **model_name**: Model to use ('ssd', 'faster_rcnn')
    - **conf_threshold**: Confidence threshold (0.0 to 1.0)
    - **device**: Device to use ('cpu' or 'cuda'), defaults to available device
    """
    model_name = model_name.lower()
    device_to_use = device or loaded_models.get(model_name, {}).get('device', 'cpu')
    
    # Load model if not already loaded
    if model_name not in loaded_models:
        try:
            await load_model(ModelLoadRequest(model_name=model_name, device=device_to_use))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    model_info = loaded_models[model_name]
    model = model_info['model']
    model_type = model_info['type']
    
    # Read image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Save temporarily
    temp_path = Path("static/uploads") / file.filename
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img_rgb).save(temp_path)
    
    try:
        if model_type == 'detection':
            # Detection models
            result = predict_image(
                model,
                str(temp_path),
                model_type=model_name,
                conf_threshold=conf_threshold,
                device=device_to_use
            )
            
            # Convert visualization to base64
            vis_img = result['visualization']
            _, buffer = cv2.imencode('.jpg', cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))
            vis_base64 = buffer.tobytes()
            
            return {
                "success": True,
                "model_type": model_name,
                "num_detections": result['num_detections'],
                "detections": result['detections'],
                "visualization": vis_base64.hex()  # Convert to hex string for JSON
            }
        
        elif model_type == 'classification':
            # CNN patch classifier (requires slot layout - placeholder)
            raise HTTPException(
                status_code=400,
                detail="CNN patch classifier requires slot layout. Use /predict/patch endpoint."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 or localhost for local access
    # 0.0.0.0 is for binding to all interfaces but can't be accessed in browser
    uvicorn.run(app, host="127.0.0.1", port=8000)

