"""
Inference scripts for parking vision deployment.
"""

from .single_inference import predict_image, predict_image_patch

__all__ = [
    'predict_image',
    'predict_image_patch'
]
