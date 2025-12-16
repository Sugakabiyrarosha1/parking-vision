# GCP Deployment - Parking Vision

This folder contains all files needed to deploy the Parking Vision application to Google Cloud Run as a single service with HTML frontend and API endpoints.

## Architecture

- **Framework:** FastAPI (with Jinja2 templates for HTML frontend)
- **Deployment:** Google Cloud Run (single service)
- **Models:** Checkpoints baked into Docker image
- **Frontend:** Server-rendered HTML (Jinja2 templates)
- **API:** REST endpoints for programmatic access

## Deployment Status

**Status:** Successfully Deployed  
**Version:** 2.0 (Optimized)  
**Service URL:** https://parking-vision-web-2lpqmedrkq-uc.a.run.app  
**Date:** December 16, 2025

## Service Configuration

- **Service Name:** parking-vision-web
- **Project ID:** parking-vision-deployment
- **Region:** us-central1
- **CPU:** 2 vCPU
- **Memory:** 4 GiB
- **Timeout:** 300 seconds (5 minutes)
- **Port:** 8080
- **Image Size:** 2.03GB (optimized from 9.17GB - 77% reduction)

## Available Endpoints

### Frontend (HTML)
- **Root:** `GET /` - Upload form with model selector
- **Detection:** `POST /detect` - Process image and show results

### API (JSON)
- **Health Check:** `GET /health` - Service status
- **List Models:** `GET /models` - Available models
- **Model Details:** `GET /models/{model_name}` - Model information
- **Predict:** `POST /api/predict` - Image prediction (JSON response)

## Quick Start

### Access the Application
Open the service URL in any web browser:
```
https://parking-vision-web-2lpqmedrkq-uc.a.run.app
```

### Local Testing (Optional)
```bash
# Build Docker image
docker build -t parking-vision-gcp:local .

# Run container
docker run -p 8080:8080 -e PORT=8080 parking-vision-gcp:local

# Test in browser
# http://localhost:8080
```

### GCP Deployment Commands
```bash
# Set variables
PROJECT_ID="parking-vision-deployment"
REGION="us-central1"
REPO="parking-vision"
SERVICE="parking-vision-web"

# Build and push
gcloud builds submit \
  --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$SERVICE:2.0 .

# Deploy
gcloud run deploy $SERVICE \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$SERVICE:2.0 \
  --allow-unauthenticated \
  --cpu 2 --memory 4Gi \
  --timeout 300 \
  --port 8080 \
  --region $REGION
```

## Key Features

- Server-rendered HTML frontend with Jinja2 templates
- REST API for programmatic access
- Two detection models (SSD and Faster R-CNN)
- Image upload and visualization with bounding boxes
- JSON download of detection results
- Optimized Docker image (2.03GB with CPU-only PyTorch)

## Optimization

The deployment uses an optimized multi-stage Docker build:
- CPU-only PyTorch (saves ~6GB)
- Removed unused packages (pandas, scikit-learn, matplotlib, seaborn)
- OpenCV headless version
- Multi-stage build for smaller final image

## Cloud Run Requirements

The container adheres to Cloud Run requirements:
- Listens on `0.0.0.0` (not `127.0.0.1`)
- Uses `$PORT` environment variable (default 8080)
- Handles cold starts (model loading on first request)

## Documentation

- See `report/deployment_report.tex` for complete deployment documentation (LaTeX report)
- Additional deployment details available in helper files

---

**Last Updated:** December 16, 2025
