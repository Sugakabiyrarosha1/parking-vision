"""
FastAPI web application for parking vision deployment.
Supports both HTML frontend (Jinja2 templates) and JSON API endpoints.
"""

import sys
import os
import time
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from typing import Optional, List
import io
import json
import base64
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

# Initialize FastAPI app
app = FastAPI(
    title="Parking Vision",
    description="AI-Powered Parking Space Detection System",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint - renders HTML upload form."""
    return templates.TemplateResponse("index.html", {"request": request})


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


@app.post("/detect", response_class=HTMLResponse)
async def detect_html(
    request: Request,
    file: UploadFile = File(...),
    model_name: str = Form(...),
    conf_threshold: Optional[float] = Form(0.5),
    device: Optional[str] = Form(None)
):
    """
    HTML endpoint - processes image and renders results page.
    """
    start_time = time.time()
    model_name = model_name.lower()
    device_to_use = device or loaded_models.get(model_name, {}).get('device', 'cpu')
    
    # Load model if not already loaded
    if model_name not in loaded_models:
        try:
            await load_model(ModelLoadRequest(model_name=model_name, device=device_to_use))
        except Exception as e:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": f"Failed to load model: {str(e)}"
                }
            )
    
    model_info = loaded_models[model_name]
    model = model_info['model']
    model_type = model_info['type']
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": "Failed to decode image. Please upload a valid image file."
                }
            )
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Save temporarily
        temp_path = Path("/tmp") / file.filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(img_rgb).save(temp_path)
        
        if model_type == 'detection':
            # Run inference
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
            vis_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Calculate statistics and add class_name to detections
            detections = result.get('detections', [])
            class_names = ["free_parking_space", "not_free_parking_space"]
            
            # Add class_name and confidence (alias for score) to each detection for template
            detections_with_names = []
            for det in detections:
                class_id = det.get('class', 0)
                class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
                det_with_name = det.copy()
                det_with_name['class_name'] = class_name
                # Add confidence as alias for score (template uses confidence)
                det_with_name['confidence'] = det.get('score', 0.0)
                detections_with_names.append(det_with_name)
            
            free_spaces = sum(1 for d in detections_with_names if d.get('class_name', '').lower() == 'free_parking_space')
            occupied_spaces = sum(1 for d in detections_with_names if d.get('class_name', '').lower() == 'not_free_parking_space')
            
            processing_time = round(time.time() - start_time, 2)
            
            # Prepare detection data for JSON download
            detection_data = {
                "model_type": model_name,
                "num_detections": result['num_detections'],
                "detections": detections_with_names,
                "statistics": {
                    "free_spaces": free_spaces,
                    "occupied_spaces": occupied_spaces,
                    "total": result['num_detections']
                },
                "conf_threshold": conf_threshold,
                "processing_time": processing_time
            }
            
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "model_type": model_name,
                    "num_detections": result['num_detections'],
                    "free_spaces": free_spaces,
                    "occupied_spaces": occupied_spaces,
                    "conf_threshold": conf_threshold,
                    "processing_time": processing_time,
                    "visualization_base64": vis_base64,
                    "detections": detections_with_names,
                    "detection_json": json.dumps(detection_data)
                }
            )
        else:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": f"Model type {model_type} not supported for HTML interface."
                }
            )
    
    except Exception as e:
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "error": f"Error processing image: {str(e)}"
            }
        )
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


@app.post("/api/predict")
async def predict(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    conf_threshold: Optional[float] = Form(0.5),
    device: Optional[str] = Form(None)
):
    """
    JSON API endpoint - returns predictions as JSON.
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
    if img is None:
        raise HTTPException(status_code=400, detail="Failed to decode image")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Save temporarily
    temp_path = Path("/tmp") / file.filename
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
            vis_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return {
                "success": True,
                "model_type": model_name,
                "num_detections": result['num_detections'],
                "detections": result['detections'],
                "visualization": vis_base64
            }
        
        elif model_type == 'classification':
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
    # Cloud Run requires binding to 0.0.0.0 and using PORT env var
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
