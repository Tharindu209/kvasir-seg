import cv2
import numpy as np
import torch

def preprocess_image(file_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256))
    return image.astype(np.float32) / 255.0

def postprocess_mask(output: torch.Tensor) -> np.ndarray:
    output = torch.sigmoid(output).squeeze().cpu().numpy()
    mask = (output > 0.5).astype(np.uint8) * 255
    return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) 