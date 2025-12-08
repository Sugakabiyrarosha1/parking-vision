#!/bin/bash
# Parking Vision Deployment - Linux Launcher

set -e  # Exit on error

echo "Starting Parking Vision Application..."
echo ""

# Get the directory where this script is located and go to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "Project root: $PROJECT_ROOT"
echo ""

# Check if virtual environment exists
if [ ! -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    echo "========================================"
    echo "ERROR: Virtual environment not found!"
    echo "========================================"
    echo "Please ensure .venv folder exists in the project root."
    echo "Expected location: $PROJECT_ROOT/.venv"
    echo ""
    echo "To create a virtual environment, run:"
    echo "  python3 -m venv .venv"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$PROJECT_ROOT/.venv/bin/activate"
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "ERROR: Failed to activate virtual environment!"
    echo "========================================"
    echo "Please check that the virtual environment is properly set up."
    echo ""
    exit 1
fi
echo "Virtual environment activated successfully."

# Go to Deployment folder
cd "$PROJECT_ROOT/Deployment"
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "ERROR: Failed to navigate to Deployment folder!"
    echo "========================================"
    echo "Expected location: $PROJECT_ROOT/Deployment"
    echo ""
    exit 1
fi
echo "Working directory: $(pwd)"
echo ""

# Check if streamlit is installed
echo "Checking for Streamlit..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Streamlit not found. Installing..."
    pip install streamlit
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Streamlit!"
        echo ""
        exit 1
    fi
else
    echo "Streamlit is installed."
fi

echo ""
echo "All checks passed. Starting Streamlit application..."
echo "The application will open in your default browser."
echo "Press Ctrl+C to stop the application."
echo ""

# Run Streamlit
streamlit run streamlit_app.py


