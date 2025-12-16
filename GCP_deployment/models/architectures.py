"""
Model architecture definitions for parking vision deployment.
"""

import torch
import torch.nn as nn
from torchvision.models.detection import (
    ssdlite320_mobilenet_v3_large,
    SSDLite320_MobileNet_V3_Large_Weights,
    fasterrcnn_resnet50_fpn,
    FasterRCNN_ResNet50_FPN_Weights
)
from torchvision.models import MobileNet_V3_Large_Weights


# Class names for all detection models
DETECTION_CLASS_NAMES = [
    "free_parking_space",
    "not_free_parking_space",
]
NUM_DETECTION_CLASSES = len(DETECTION_CLASS_NAMES)
NUM_DETECTION_CLASSES_WITH_BG = NUM_DETECTION_CLASSES + 1  # +1 for background


def build_ssd_model(num_classes=3, pretrained=True):
    """
    Build SSD Lite 320 MobileNetV3 model for parking space detection.
    
    Args:
        num_classes: Number of classes including background (default: 3 for 2 parking classes + bg)
        pretrained: Whether to use pretrained weights
    
    Returns:
        SSD model ready for inference
    """
    if pretrained:
        weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
        ssd_model = ssdlite320_mobilenet_v3_large(weights=weights, num_classes=num_classes)
    else:
        ssd_model = ssdlite320_mobilenet_v3_large(weights=None, num_classes=num_classes)
    
    return ssd_model


def build_faster_rcnn_model(num_classes=3, pretrained=True):
    """
    Build Faster R-CNN ResNet50 FPN model for parking space detection.
    
    Args:
        num_classes: Number of classes including background (default: 3 for 2 parking classes + bg)
        pretrained: Whether to use pretrained weights
    
    Returns:
        Faster R-CNN model ready for inference
    """
    if pretrained:
        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        model = fasterrcnn_resnet50_fpn(weights=weights, num_classes=num_classes)
    else:
        model = fasterrcnn_resnet50_fpn(weights=None, num_classes=num_classes)
    
    return model


def build_detr_model(num_classes=2, hidden_dim=256, nheads=8, num_encoder_layers=6, num_decoder_layers=6):
    """
    Build DETR (Detection Transformer) model for parking space detection.
    Uses transformers library DetrForObjectDetection.
    
    Args:
        num_classes: Number of classes (not including background/no-object)
        hidden_dim: Hidden dimension size (default 256 for DETR-ResNet-50)
        nheads: Number of attention heads
        num_encoder_layers: Number of encoder layers
        num_decoder_layers: Number of decoder layers
    
    Returns:
        DETR model ready for inference
    """
    try:
        from transformers import DetrForObjectDetection, DetrConfig
    except ImportError:
        raise ImportError("transformers library is required for DETR. Install with: pip install transformers")
    
    # DETR configuration
    config = DetrConfig.from_pretrained("facebook/detr-resnet-50")
    config.num_labels = num_classes
    
    # Create label mappings
    id2label = {0: "free_parking_space", 1: "not_free_parking_space"}
    label2id = {"free_parking_space": 0, "not_free_parking_space": 1}
    
    config.id2label = id2label
    config.label2id = label2id
    
    # Build model
    model = DetrForObjectDetection.from_pretrained(
        "facebook/detr-resnet-50",
        config=config,
        ignore_mismatched_sizes=True
    )
    
    return model


def build_cnn_patch_model(input_size=(80, 80), num_classes=2):
    """
    Build CNN patch classifier for individual parking slot classification.
    
    Args:
        input_size: Input patch size (height, width)
        num_classes: Number of classes (2: Empty, Occupied)
    
    Returns:
        CNN model ready for inference
    """
    import torch.nn.functional as F
    
    class PatchCNN(nn.Module):
        def __init__(self, num_classes=2):
            super(PatchCNN, self).__init__()
            # Convolutional layers (no BatchNorm - matches trained model)
            self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
            
            # Pooling
            self.pool = nn.MaxPool2d(2, 2)
            
            # Fully connected layers
            # After 3 maxpool layers: 80/8 = 10, so 10*10*128 = 12800
            conv_output_size = 12800
            self.fc1 = nn.Linear(conv_output_size, 128)
            self.dropout = nn.Dropout(0.5)
            self.fc2 = nn.Linear(128, num_classes)
            
        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))  # 80x80 -> 40x40
            x = self.pool(F.relu(self.conv2(x)))  # 40x40 -> 20x20
            x = self.pool(F.relu(self.conv3(x)))  # 20x20 -> 10x10
            
            x = x.view(x.size(0), -1)
            x = self.dropout(F.relu(self.fc1(x)))
            x = self.fc2(x)
            return x
    
    return PatchCNN(num_classes=num_classes)

