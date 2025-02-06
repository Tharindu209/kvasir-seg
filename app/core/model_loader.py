import torch
import segmentation_models_pytorch as smp
from app.core.config import configs

model = None

def load_segmentation_model():
    """Load and configure the segmentation model"""
    global model
    local_model = smp.Unet(
        encoder_name='resnet50',
        encoder_weights='imagenet',
        in_channels=3,
        classes=1
    )
    
    local_model.load_state_dict(torch.load(configs.MODEL_PATH, map_location=torch.device(configs.DEVICE)))
    local_model.eval()
    
    model = local_model
    return model