# Parking Vision Deployment

Complete deployment package for parking space detection models.

## Quick Start

### Windows

#### Easy Method (Recommended)

**Double-click `run.bat`** - That's it!

The application will automatically:
1. Activate the virtual environment
2. Start the Streamlit web application
3. Open in your browser at `http://localhost:8501`

#### Manual Method

If the batch file doesn't work:

```powershell
# 1. Navigate to project root (adjust path to your location)
cd "path\to\parking-vision"

# 2. Activate virtual environment
.venv\Scripts\Activate.ps1

# 3. Go to Deployment folder
cd Deployment

# 4. Install Streamlit (if needed)
pip install streamlit

# 5. Run the app
streamlit run streamlit_app.py
```

### Linux / macOS

#### Easy Method (Recommended)

**Run the shell script**:

```bash
chmod +x Deployment/run.sh
./Deployment/run.sh
```

The application will automatically:
1. Activate the virtual environment
2. Start the Streamlit web application
3. Open in your browser at `http://localhost:8501`

#### Manual Method

If the shell script doesn't work:

```bash
# 1. Navigate to project root
cd /path/to/parking-vision

# 2. Create virtual environment if needed
python3 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Go to Deployment folder
cd Deployment

# 5. Install dependencies (if needed)
pip install -r requirements.txt

# 6. Run the app
streamlit run streamlit_app.py
```

## Setup on a New Machine

When cloning this repository to a different laptop, you may need to make the following adjustments:

### 1. Update `run.bat` Script (If Needed)

The `run.bat` script automatically detects the project root, so it should work on any machine. However, if you encounter issues:

- **Location**: `Deployment/run.bat`
- **What to check**: The script uses `%~dp0..` to go to the project root, which should work automatically
- **Only change if**: The script fails to find the virtual environment - then update the path logic

### 2. Virtual Environment Path

The code uses relative paths, so no changes are needed in Python files. However:

- **Create virtual environment** in the project root if it doesn't exist:
  ```powershell
  python -m venv .venv
  ```

- **Location**: Project root (parent of `Deployment/` folder)
- **No code changes needed**: All Python files use `Path(__file__).parent` for relative paths

### 3. Model Checkpoint Paths

**Important**: The model checkpoints are located in `Deployment/checkpoints/` folder.

- **Current structure**: `Deployment/checkpoints/phase2_ssd_parking/best_model.pt`
- **Code location**: `Deployment/models/model_loader.py`
- **Path calculation**: Uses `DEPLOYMENT_DIR = Path(__file__).parent.parent` which resolves to `Deployment/` folder
- **Checkpoint lookup**: Looks for `DEPLOYMENT_DIR / 'checkpoints'` which correctly points to `Deployment/checkpoints/`

✅ **No changes needed**: The code automatically uses relative paths and will work on any machine as long as the folder structure is maintained.

**Required checkpoint files**:
- `Deployment/checkpoints/phase2_ssd_parking/best_model.pt`
- `Deployment/checkpoints/phase2_faster_rcnn_parking/best_model.pt`

**If checkpoints are missing**, ensure these files are present in the `Deployment/checkpoints/` folder.

### 4. No Hardcoded Paths in Code

✅ **Good news**: All Python code uses relative paths:
- `Path(__file__).parent` - Gets current file's directory
- `Path(__file__).parent.parent` - Gets parent directory (Deployment folder from models/)
- All paths are calculated dynamically, so they work on any machine without modification

### 5. File Structure Requirements

The deployment expects this structure:
```
parking-vision/                    # Project root
├── .venv/                        # Virtual environment (create if missing)
└── Deployment/                   # Deployment folder
    ├── checkpoints/              # Model checkpoints (REQUIRED)
    │   ├── phase2_ssd_parking/
    │   │   └── best_model.pt
    │   └── phase2_faster_rcnn_parking/
    │       └── best_model.pt
    ├── models/                   # Model loading code
    ├── inference/                # Inference functions
    ├── utils/                    # Utility functions
    ├── run.bat                   # Main launcher
    └── streamlit_app.py          # Web application
```

**Important**: Checkpoints must be in `Deployment/checkpoints/` folder. The code automatically finds them using relative paths.

### 6. Verification Steps

After cloning, verify:

1. **Check virtual environment exists** (from project root):
   ```powershell
   Test-Path ".venv\Scripts\activate.bat"
   ```

2. **Check model checkpoints exist** (from project root):
   ```powershell
   Test-Path "Deployment\checkpoints\phase2_ssd_parking\best_model.pt"
   Test-Path "Deployment\checkpoints\phase2_faster_rcnn_parking\best_model.pt"
   ```

3. **Install dependencies**:
   ```powershell
   .venv\Scripts\Activate.ps1
   pip install -r Deployment\requirements.txt
   ```

4. **Test the application**:
   ```powershell
   cd Deployment
   streamlit run streamlit_app.py
   ```

## Available Models

- **SSD** - Fast detection, good accuracy
- **Faster R-CNN** - Highest accuracy, slower inference

## Usage

1. Start the application using `run.bat` (Windows) or `run.sh` (Linux/macOS)
2. Select a model from the sidebar
3. Adjust confidence threshold if needed
4. Upload a parking lot image
5. View detection results with visualizations
6. Download results as JSON if needed

## Requirements

All dependencies are listed in `requirements.txt`. 

**Note:** The `run.bat` (Windows) or `run.sh` (Linux/macOS) script will automatically install missing dependencies (Streamlit and transformers). If you prefer to install manually:

```bash
pip install -r requirements.txt
```

**Important:** DETR model requires the `transformers` library. If you see an error about missing transformers, make sure you're using the virtual environment (via `run.bat` on Windows or `run.sh` on Linux/macOS).

## Troubleshooting

**PyTorch DLL Error (Windows):**
- Make sure you're using the virtual environment (use `run.bat`)
- Don't run from system Python

**PyTorch Import Error (Linux/macOS):**
- Make sure you're using the virtual environment (use `run.sh` or activate manually)
- Ensure PyTorch is installed: `pip install torch torchvision`

**Port Already in Use:**
- Change port in `streamlit_app.py` or use `--server.port 8502`

**Models Not Found:**
- Verify models are in `checkpoints/` folder
- All `best_model.pt` files should be present

## File Structure

```
Deployment/
├── README.md                 # This file
├── run.bat                   # Main batch file to run the app (Windows)
├── run.sh                    # Main shell script to run the app (Linux/macOS)
├── streamlit_app.py          # Streamlit web application
├── requirements.txt          # Python dependencies
├── checkpoints/              # Model files (best_model.pt)
├── models/                   # Model loading utilities
├── inference/                # Inference functions
└── utils/                    # Utility functions
```
