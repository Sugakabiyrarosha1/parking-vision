"""
Streamlit web application for parking vision deployment.
"""

import sys
from pathlib import Path

# Add Deployment folder to path for imports
DEPLOYMENT_DIR = Path(__file__).parent
if str(DEPLOYMENT_DIR) not in sys.path:
    sys.path.insert(0, str(DEPLOYMENT_DIR))

import streamlit as st
import numpy as np
from PIL import Image
import cv2
import json
import tempfile
import os
from typing import Dict, List
import io

from models.model_loader import (
    load_detection_model,
    list_available_models,
    get_model_info
)
from inference.single_inference import predict_image
from utils.image_utils import load_image


# Page configuration
st.set_page_config(
    page_title="Parking Vision",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .model-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model_cached(model_name: str, device: str = "cpu"):
    """Load and cache model in memory."""
    try:
        if model_name in ['ssd', 'faster_rcnn']:
            model = load_detection_model(model_name, device=device)
            return {
                'model': model,
                'type': 'detection',
                'device': device
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return None


def main():
    # Header
    st.markdown('<h1 class="main-header">🚗 Parking Vision Detection System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        available_models = list_available_models()
        model_names = [name for name, info in available_models.items() if info.get('exists', False)]
        
        selected_model = st.selectbox(
            "Select Model",
            options=model_names,
            help="Choose which model to use for detection"
        )
        
        # Device selection
        device = st.radio(
            "Device",
            options=["cpu", "cuda"],
            index=0,
            help="Select CPU or GPU (CUDA) for inference"
        )
        
        # Confidence threshold
        conf_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence score for detections"
        )
        
        # Model info
        if selected_model:
            try:
                model_info = get_model_info(selected_model)
                st.subheader("Model Info")
                st.write(f"**Type:** {model_info.get('type', 'N/A')}")
                st.write(f"**Size:** {model_info.get('size_mb', 'N/A')} MB")
                if 'classes' in model_info:
                    st.write(f"**Classes:** {', '.join(model_info['classes'])}")
            except:
                pass
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Choose a page",
            ["Single Image", "Batch Processing", "About"]
        )
    
    # Main content area
    if page == "Single Image":
        single_image_page(selected_model, device, conf_threshold)
    elif page == "Batch Processing":
        batch_processing_page(selected_model, device, conf_threshold)
    else:
        about_page()


def single_image_page(model_name: str, device: str, conf_threshold: float):
    """Single image prediction page."""
    st.header("📸 Single Image Detection")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Upload a parking lot image to detect parking spaces"
    )
    
    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        
        # Display original image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)
            st.caption(f"Size: {image.size[0]} x {image.size[1]}")
        
        with col2:
            st.subheader("Detection Results")
            
            # Load model
            with st.spinner(f"Loading {model_name} model..."):
                model_data = load_model_cached(model_name, device)
            
            if model_data:
                # Temporary save for inference - ensure unique filename
                import time
                timestamp = int(time.time() * 1000)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', prefix=f'img_{timestamp}_') as tmp_file:
                    temp_path = tmp_file.name
                    # Save image as RGB
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(temp_path, format='JPEG', quality=95)
                
                try:
                    # Predict
                    with st.spinner("Running detection..."):
                        result = predict_image(
                            model_data['model'],
                            temp_path,
                            model_type=model_name,
                            conf_threshold=conf_threshold,
                            device=device
                        )
                    
                    # Clean up temp file
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                    
                    if result:
                        # Display results
                        st.image(result['visualization'], use_container_width=True)
                        
                        # Statistics
                        st.metric("Detections Found", result['num_detections'])
                        
                        # Detections table
                        if result.get('detections'):
                            st.subheader("Detection Details")
                            detections_data = []
                            class_names = ["free_parking_space", "not_free_parking_space"]
                            
                            for i, det in enumerate(result['detections'], 1):
                                detections_data.append({
                                    'ID': i,
                                    'Class': class_names[det.get('class', 0)] if det.get('class', 0) < len(class_names) else f"Class {det.get('class', 0)}",
                                    'Confidence': f"{det.get('score', 0):.3f}",
                                    'BBox': f"[{det['bbox'][0]:.0f}, {det['bbox'][1]:.0f}, {det['bbox'][2]:.0f}, {det['bbox'][3]:.0f}]"
                                })
                            
                            st.dataframe(detections_data, use_container_width=True)
                            
                            # Download results
                            json_str = json.dumps({
                                'num_detections': result['num_detections'],
                                'detections': [
                                    {k: v for k, v in det.items() if k != 'bbox'}  # Remove bbox for JSON
                                    for det in result['detections']
                                ]
                            }, indent=2)
                            
                            st.download_button(
                                label="Download Results (JSON)",
                                data=json_str,
                                file_name="detection_results.json",
                                mime="application/json"
                            )
                
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
                finally:
                    # Clean up temp file
                    import os
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            else:
                st.error("Failed to load model. Please check the model files.")
    
    else:
        st.info("👆 Please upload an image to get started")


def batch_processing_page(model_name: str, device: str, conf_threshold: float):
    """Batch processing page."""
    st.header("📦 Batch Processing")
    
    st.write("Upload multiple images as a ZIP file for batch processing.")
    
    uploaded_zip = st.file_uploader(
        "Upload ZIP file with images",
        type=['zip'],
        help="Upload a ZIP file containing multiple parking lot images"
    )
    
    if uploaded_zip:
        st.info("Batch processing feature coming soon! For now, please use the Single Image page.")
        # TODO: Implement batch processing with ZIP extraction
    
    else:
        st.info("👆 Please upload a ZIP file containing images")


def about_page():
    """About page."""
    st.header("ℹ️ About Parking Vision")
    
    st.write("""
    This application provides parking space detection using deep learning models.
    
    ### Available Models:
    - **SSD**: Fast detection with good accuracy
    - **Faster R-CNN**: Highest accuracy, slower inference
    
    ### Features:
    - Real-time parking space detection
    - Multiple model support
    - Confidence threshold adjustment
    - Visualization of results
    - Batch processing capability
    
    ### Usage:
    1. Select a model from the sidebar
    2. Upload an image
    3. Adjust confidence threshold if needed
    4. View detection results
    """)


if __name__ == "__main__":
    main()

