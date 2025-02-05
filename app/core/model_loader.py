import torch
import segmentation_models_pytorch as smp
from app.core.config import configs

def load_segmentation_model():
    """Load and configure the segmentation model"""
    model = smp.Unet(
        encoder_name='resnet50',
        encoder_weights='imagenet',
        in_channels=3,
        classes=1
    )
    model.load_state_dict(torch.load(configs.MODEL_PATH, map_location=torch.device(configs.DEVICE)))
    model.eval()
    return model

model = load_segmentation_model()