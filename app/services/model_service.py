import torch
from PIL import Image
import numpy as np

class SegmentationService:
    def __init__(self, model_path: str, device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = self.load_model(model_path, device)
        self.device = device
        
    def load_model(self, model_path: str, device: str):
        # Initialize your model architecture
        model = YourModelClass()  # Replace with your model class
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        return model.to(device)
    
    def preprocess(self, image: Image.Image) -> torch.Tensor:
        # Implement your preprocessing logic
        transforms = Compose([Resize((256, 256)), ToTensor()])
        return transforms(image).unsqueeze(0).to(self.device)
    
    def predict(self, image: Image.Image) -> np.ndarray:
        with torch.no_grad():
            tensor = self.preprocess(image)
            output = self.model(tensor)
            return output.squeeze().cpu().numpy()