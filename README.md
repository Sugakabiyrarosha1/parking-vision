# 🚗 Parking Vision - Deep Learning Parking Space Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**An intelligent parking space detection system powered by state-of-the-art deep learning models**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Models](#-models)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [File Structure](#-file-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 About

**Parking Vision** is a comprehensive deep learning-based parking space detection system that leverages state-of-the-art object detection models to identify and classify parking spaces in real-world scenarios. The system is designed to help optimize parking lot management, improve space utilization, and provide real-time parking availability information.

### Key Highlights

- 🎯 **High Accuracy**: Utilizes advanced deep learning models (SSD, Faster R-CNN) trained on extensive parking lot datasets
- ⚡ **Fast Inference**: Optimized models for real-time detection with configurable speed/accuracy trade-offs
- 🌐 **Web Interface**: User-friendly Streamlit-based web application for easy interaction
- 🔌 **REST API**: FastAPI backend for programmatic access and integration
- 🐳 **Docker Ready**: Containerized deployment for easy setup and scaling
- 🔧 **Cross-Platform**: Works seamlessly on Windows, Linux, and macOS

---

## ✨ Features

### Core Capabilities

- 🖼️ **Image Upload & Processing**: Support for various image formats (JPG, PNG, etc.)
- 🎨 **Real-time Visualization**: Interactive bounding box overlays with confidence scores
- 📊 **Detection Metrics**: Detailed statistics including:
  - Total parking spots detected
  - Occupied vs. empty spaces
  - Confidence scores per detection
  - Processing time metrics
- 💾 **Export Results**: Download detection results as JSON for further analysis
- 🎛️ **Configurable Thresholds**: Adjustable confidence thresholds for fine-tuning detection sensitivity

### Model Support

- **SSD (Single Shot Detector)**: Fast inference with good accuracy, ideal for real-time applications
- **Faster R-CNN**: Highest accuracy detection, suitable for precision-critical scenarios
- **DETR (Detection Transformer)**: Transformer-based detection (optional, requires additional setup)

### Additional Features

- 🔄 **Model Caching**: Automatic model loading and caching for faster subsequent inferences
- 📱 **Responsive Design**: Works on desktop and tablet devices
- 🛠️ **Debug Mode**: Comprehensive error messages and debugging information
- 🔍 **Batch Processing**: Support for processing multiple images via command-line tools

---

## 📸 Screenshots

### Web Interface

The Streamlit web application provides an intuitive interface for parking space detection:

- **Landing Page**: Clean, modern design with easy model selection
- **Detection Results**: Visualized bounding boxes with color-coded confidence levels
- **Statistics Panel**: Real-time metrics and detection summaries

### Command-Line Interface

Batch processing tools for automated workflows and integration with other systems.

---

## 🚀 Quick Start

### Windows

#### Easy Method (Recommended) ⭐

**Simply double-click `run.bat`** - The application will automatically:
1. ✅ Activate the virtual environment
2. ✅ Install missing dependencies
3. ✅ Start the Streamlit web application
4. ✅ Open in your browser at `http://localhost:8501`

#### Manual Method

```powershell
# 1. Navigate to project root
cd "path\to\parking-vision"

# 2. Activate virtual environment
.venv\Scripts\Activate.ps1

# 3. Navigate to Deployment folder
cd Deployment

# 4. Install dependencies (if needed)
pip install -r requirements.txt

# 5. Run the application
streamlit run streamlit_app.py
```

### Linux / macOS

#### Easy Method (Recommended) ⭐

```bash
# Make script executable (first time only)
chmod +x Deployment/run.sh

# Run the application
./Deployment/run.sh
```

The application will automatically:
1. ✅ Activate the virtual environment
2. ✅ Install missing dependencies
3. ✅ Start the Streamlit web application
4. ✅ Display the URL in the terminal

#### Manual Method

```bash
# 1. Navigate to project root
cd /path/to/parking-vision

# 2. Create virtual environment (if needed)
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Navigate to Deployment folder
cd Deployment

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
streamlit run streamlit_app.py
```

---

## 📦 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, Linux, or macOS
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: ~5GB free space for models and dependencies
- **GPU**: Optional but recommended for faster inference (CUDA-compatible)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/parking-vision.git
   cd parking-vision
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   
   # Linux/macOS
   python3 -m venv .venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   .venv\Scripts\Activate.ps1
   
   # Linux/macOS
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   cd Deployment
   pip install -r requirements.txt
   ```

5. **Verify Model Checkpoints**
   Ensure model checkpoints are present in `Deployment/checkpoints/`:
   - `phase2_ssd_parking/best_model.pt`
   - `phase2_faster_rcnn_parking/best_model.pt`

6. **Test Installation**
   ```bash
   streamlit run streamlit_app.py
   ```

### Docker Installation (Optional)

```bash
# Build Docker image
docker build -t parking-vision:latest .

# Run container
docker run -p 8501:8501 parking-vision:latest
```

---

## 💻 Usage

### Web Interface (Streamlit)

1. **Start the Application**
   - Windows: Double-click `run.bat`
   - Linux/macOS: Run `./Deployment/run.sh`

2. **Select Model**
   - Choose from available models in the sidebar (SSD or Faster R-CNN)
   - Adjust confidence threshold if needed (default: 0.5)

3. **Upload Image**
   - Click "Upload Image" or drag and drop a parking lot image
   - Supported formats: JPG, PNG, JPEG

4. **View Results**
   - Detection results appear automatically
   - Bounding boxes overlay on the image
   - Statistics panel shows detection metrics

5. **Export Results** (Optional)
   - Click "Download Results" to save JSON output
   - JSON contains bounding boxes, confidence scores, and metadata

### Command-Line Interface

#### Single Image Prediction

```bash
python predict_image.py --image path/to/image.jpg --model ssd --output results/
```

**Options:**
- `--image`: Path to input image
- `--model`: Model to use (`ssd` or `faster_rcnn`)
- `--output`: Output directory for results
- `--confidence`: Confidence threshold (default: 0.5)
- `--device`: Device to use (`cpu` or `cuda`)

#### Batch Processing

```bash
python predict_batch.py --input images/ --model ssd --output results/
```

**Options:**
- `--input`: Directory containing input images
- `--model`: Model to use
- `--output`: Output directory for results
- `--confidence`: Confidence threshold
- `--device`: Device to use

### API Usage (FastAPI)

Start the API server:

```bash
cd Deployment
uvicorn app:app --host 0.0.0.0 --port 8000
```

**Example API Request:**

```python
import requests

# Upload image and get predictions
with open('parking_lot.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'image': f},
        data={'model': 'ssd', 'confidence': 0.5}
    )

results = response.json()
print(f"Detected {results['num_detections']} parking spaces")
```

**API Endpoints:**

- `POST /predict`: Single image prediction
- `POST /predict/batch`: Batch image processing
- `GET /models`: List available models
- `GET /health`: Health check endpoint

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
├─────────────────────────────────────────────────────────────┤
│  Streamlit Web App  │  FastAPI REST API  │  CLI Tools        │
└─────────────────────┼────────────────────┼──────────────────┘
                      │                    │
┌─────────────────────┴────────────────────┴──────────────────┐
│                    Application Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Model Loader  │  Inference Engine  │  Image Processing     │
└────────────────┼────────────────────┼───────────────────────┘
                 │                    │
┌────────────────┴────────────────────┴───────────────────────┐
│                    Model Layer                                │
├─────────────────────────────────────────────────────────────┤
│  SSD Model  │  Faster R-CNN Model  │  DETR Model (Optional) │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. **Model Loader** (`models/model_loader.py`)
- Handles model checkpoint loading
- Manages model caching and memory optimization
- Provides model information and metadata

#### 2. **Inference Engine** (`inference/`)
- `single_inference.py`: Single image prediction
- `batch_inference.py`: Batch processing capabilities
- Optimized for CPU and GPU inference

#### 3. **Image Processing** (`utils/`)
- `image_utils.py`: Image loading and preprocessing
- `visualization.py`: Bounding box drawing and result visualization

#### 4. **Web Interface** (`streamlit_app.py`)
- Streamlit-based interactive UI
- Real-time model selection and configuration
- Result visualization and export

#### 5. **API Backend** (`app.py`)
- FastAPI REST API server
- CORS-enabled for cross-origin requests
- Async request handling

---

## 📡 API Documentation

### FastAPI Endpoints

When running the FastAPI server, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoint Details

#### `POST /predict`

Predict parking spaces in a single image.

**Request:**
- `image`: Image file (multipart/form-data)
- `model`: Model name (`ssd` or `faster_rcnn`)
- `confidence`: Confidence threshold (0.0-1.0, optional)

**Response:**
```json
{
  "num_detections": 45,
  "detections": [
    {
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.95,
      "class": "parking_space"
    }
  ],
  "processing_time": 0.234,
  "model": "ssd"
}
```

#### `POST /predict/batch`

Process multiple images in batch.

**Request:**
- `images`: List of image files
- `model`: Model name
- `confidence`: Confidence threshold

**Response:**
```json
{
  "results": [
    {
      "filename": "image1.jpg",
      "num_detections": 45,
      "detections": [...]
    }
  ],
  "total_images": 10,
  "processing_time": 2.345
}
```

#### `GET /models`

List available models and their information.

**Response:**
```json
{
  "available_models": ["ssd", "faster_rcnn"],
  "models": {
    "ssd": {
      "name": "SSD Lite 320 MobileNetV3",
      "checkpoint": "phase2_ssd_parking/best_model.pt",
      "status": "loaded"
    }
  }
}
```

---

## 🤖 Models

### Available Models

#### 1. **SSD (Single Shot Detector)**
- **Architecture**: SSD Lite 320 with MobileNetV3 backbone
- **Speed**: ⚡⚡⚡ Fast (real-time capable)
- **Accuracy**: ⭐⭐⭐ Good
- **Use Case**: Real-time applications, mobile deployment
- **Checkpoint**: `phase2_ssd_parking/best_model.pt`

#### 2. **Faster R-CNN**
- **Architecture**: Faster R-CNN with ResNet50 FPN backbone
- **Speed**: ⚡ Moderate
- **Accuracy**: ⭐⭐⭐⭐⭐ Excellent
- **Use Case**: High-precision requirements, offline processing
- **Checkpoint**: `phase2_faster_rcnn_parking/best_model.pt`

### Model Performance

| Model | mAP@50 | Inference Speed (FPS) | Memory Usage |
|-------|--------|------------------------|--------------|
| SSD | 0.85 | ~15-20 | ~500MB |
| Faster R-CNN | 0.92 | ~5-8 | ~1.2GB |

*Performance metrics may vary based on hardware and image resolution*

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `Deployment/` folder:

```env
# Model Configuration
MODEL_DEVICE=cpu  # or cuda
DEFAULT_CONFIDENCE=0.5
MODEL_CACHE_SIZE=2

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*

# Streamlit Configuration
STREAMLIT_PORT=8501
STREAMLIT_THEME=light
```

### Model Configuration

Model settings can be adjusted in `models/model_loader.py`:

```python
# Default device
DEFAULT_DEVICE = "cpu"  # Change to "cuda" for GPU

# Confidence threshold
DEFAULT_CONFIDENCE = 0.5

# Model cache settings
CACHE_SIZE = 2  # Number of models to cache
```

---

## 🚢 Deployment

### Production Deployment

#### Option 1: Docker Deployment

```bash
# Build image
docker build -t parking-vision:latest .

# Run with port mapping
docker run -d -p 8501:8501 \
  -v $(pwd)/checkpoints:/app/checkpoints \
  parking-vision:latest
```

#### Option 2: Cloud Deployment

**Streamlit Cloud:**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure model checkpoint paths
4. Deploy

**AWS/GCP/Azure:**
- Use container services (ECS, Cloud Run, Container Instances)
- Mount model checkpoints as volumes
- Configure load balancing for high traffic

### Setup on New Machine

When cloning to a different machine:

✅ **No code changes needed** - All paths are relative!

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

2. **Install Dependencies**
   ```bash
   .venv\Scripts\Activate.ps1  # Windows
   source .venv/bin/activate    # Linux/macOS
   pip install -r Deployment/requirements.txt
   ```

3. **Verify Checkpoints**
   Ensure `Deployment/checkpoints/` contains:
   - `phase2_ssd_parking/best_model.pt`
   - `phase2_faster_rcnn_parking/best_model.pt`

4. **Run Application**
   ```bash
   # Windows
   Deployment\run.bat
   
   # Linux/macOS
   ./Deployment/run.sh
   ```

### File Structure Requirements

```
parking-vision/                    # Project root
├── .venv/                        # Virtual environment
├── Deployment/                   # Deployment folder
│   ├── checkpoints/              # Model checkpoints (REQUIRED)
│   │   ├── phase2_ssd_parking/
│   │   │   └── best_model.pt
│   │   └── phase2_faster_rcnn_parking/
│   │       └── best_model.pt
│   ├── models/                   # Model loading code
│   ├── inference/                # Inference functions
│   ├── utils/                    # Utility functions
│   ├── run.bat                   # Windows launcher
│   ├── run.sh                    # Linux/macOS launcher
│   ├── streamlit_app.py          # Web application
│   ├── app.py                    # FastAPI backend
│   └── requirements.txt          # Dependencies
└── README.md                      # Project README
```

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ PyTorch DLL Error (Windows)

**Problem**: `OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed`

**Solution**:
- ✅ Use the virtual environment (run `run.bat`)
- ✅ Don't run from system Python
- ✅ Reinstall PyTorch: `pip uninstall torch torchvision && pip install torch torchvision`

#### ❌ PyTorch Import Error (Linux/macOS)

**Problem**: `ModuleNotFoundError: No module named 'torch'`

**Solution**:
- ✅ Activate virtual environment: `source .venv/bin/activate`
- ✅ Install PyTorch: `pip install torch torchvision`
- ✅ Verify installation: `python -c "import torch; print(torch.__version__)"`

#### ❌ Port Already in Use

**Problem**: `Address already in use`

**Solution**:
- ✅ Change port: `streamlit run streamlit_app.py --server.port 8502`
- ✅ Kill existing process: `lsof -ti:8501 | xargs kill` (Linux/macOS)

#### ❌ Models Not Found

**Problem**: `FileNotFoundError: Model checkpoint not found`

**Solution**:
1. ✅ Verify checkpoints exist:
   ```bash
   # Windows
   Test-Path "Deployment\checkpoints\phase2_ssd_parking\best_model.pt"
   
   # Linux/macOS
   ls Deployment/checkpoints/phase2_ssd_parking/best_model.pt
   ```

2. ✅ Check folder structure matches expected paths
3. ✅ Review debug information in Streamlit sidebar
4. ✅ Ensure file permissions allow reading (Linux): `chmod -R 644 Deployment/checkpoints/**/*.pt`

#### ❌ Linux-Specific Issues

**Path Resolution:**
- ✅ Code uses absolute paths with `.resolve()` for cross-platform compatibility
- ✅ Ensure working directory is correct (use `run.sh` script)

**Case Sensitivity:**
- ✅ Linux is case-sensitive - folder names must match exactly
- ✅ Use `phase2_ssd_parking` not `Phase2_SSD_Parking`

**File Permissions:**
```bash
chmod -R 644 Deployment/checkpoints/**/*.pt
```

### Getting Help

If you encounter issues not covered here:

1. 📖 Check the debug information in the Streamlit sidebar
2. 🔍 Review error messages and stack traces
3. 📝 Check that all dependencies are installed correctly
4. 🐛 Verify model checkpoints are in the correct location
5. 💬 Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python version)

---

## 📁 File Structure

```
Deployment/
├── 📄 README.md                    # This file
├── 🚀 run.bat                      # Windows launcher script
├── 🚀 run.sh                       # Linux/macOS launcher script
├── 🐍 streamlit_app.py            # Streamlit web application
├── 🔌 app.py                       # FastAPI REST API backend
├── 📋 requirements.txt            # Python dependencies
├── 🐳 Dockerfile                   # Docker configuration
├── 📦 .dockerignore                # Docker ignore patterns
│
├── 🤖 checkpoints/                 # Model checkpoints
│   ├── phase2_ssd_parking/
│   │   ├── best_model.pt
│   │   └── hyperparameter_tuning_results.json
│   ├── phase2_faster_rcnn_parking/
│   │   └── best_model.pt
│   ├── phase2_detr_parking/
│   │   └── best_model.pt
│   └── phase2_yolo_parking/
│       └── training_summary.json
│
├── 🧠 models/                      # Model loading utilities
│   ├── __init__.py
│   ├── model_loader.py             # Model loading and caching
│   └── architectures.py            # Model architecture definitions
│
├── 🔍 inference/                   # Inference functions
│   ├── __init__.py
│   ├── single_inference.py         # Single image prediction
│   └── batch_inference.py          # Batch processing
│
├── 🛠️ utils/                       # Utility functions
│   ├── __init__.py
│   ├── image_utils.py              # Image loading and preprocessing
│   └── visualization.py             # Result visualization
│
├── 🖼️ static/                      # Static files
│   └── uploads/                    # Uploaded images (temporary)
│
└── 📝 Command-line tools
    ├── predict_image.py            # Single image prediction CLI
    └── predict_batch.py            # Batch processing CLI
```

---

## 👥 Contributing

This project was developed as part of a Deep Learning II course project. The team members include:

- **Francis Cho** - Project Manager & SAM Model Training
- **Hitakshi Chugh** - Scrum Master & YOLO Implementation
- **Sugakabiyrarosha** - Dataset Exploration, CNN Baseline, SSD/DETR Training, Main Report Writing, Deployment 
- **Alvis Chi Hin Ngan** - Data Augmentation, Faster R-CNN Implementation, Hyperparameter Tuning
- **John Allan Ellingson** - YOLO Implementation, Clustering Pipeline, Visualizations

### Development Guidelines

If you wish to contribute or extend this project:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔀 Open a Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Write unit tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **PKLot Dataset** - For providing the parking lot dataset
- **PyTorch Team** - For the excellent deep learning framework
- **Streamlit** - For the intuitive web framework
- **FastAPI** - For the high-performance API framework
- **Ultralytics** - For YOLOv8 implementation and resources

---

## 📞 Contact & Support

For questions, issues, or contributions:

- 📧 **Email**: [Your Email]
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/parking-vision/issues)
- 📚 **Documentation**: [Full Documentation](https://github.com/yourusername/parking-vision/wiki)

---

<div align="center">

**Made with ❤️ by the Parking Vision Team**

⭐ Star this repo if you find it helpful!

</div>
