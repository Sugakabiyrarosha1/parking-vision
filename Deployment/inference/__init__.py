"""
Inference scripts for parking vision deployment.
"""

from .single_inference import predict_image
from .batch_inference import batch_predict

__all__ = [
    'predict_image',
    'batch_predict'
]


