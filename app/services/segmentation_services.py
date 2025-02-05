import time
import cv2
import numpy as np
import torch
from io import BytesIO
from app.core.config import configs, supabase
from app.utils.image_processing import preprocess_image, postprocess_mask
from app.core.model_loader import model

class SegmentationService:
    def __init__(self, model):
        self.model = model
        self.device = torch.device(configs.DEVICE)
        self.model.to(self.device)

    async def process_image(self, file_bytes: bytes, user_id: str) -> dict:
        start_time = time.time()
        
        try:
            image = preprocess_image(file_bytes)
            mask = self._run_inference(image)
            result_url = await self._store_results(mask, user_id)
            
            return {
                "segmented_url": result_url,
                "processing_time": time.time() - start_time
            }
            
        except Exception as e:
            raise Exception(
                detail=str(e),
                error_type=type(e).__name__
            )

    def _run_inference(self, image: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            image_tensor = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).to(self.device)
            output = self.model(image_tensor)
            return postprocess_mask(output)

    async def _store_results(self, mask: np.ndarray, user_id: str) -> str:
        try:
            _, encoded_mask = cv2.imencode('.png', mask)
            file_path = f"user_{user_id}/{int(time.time())}_segmented.png"
            
            supabase.storage.from_(configs.SEGMENTATION_BUCKET).upload(
                file_path=file_path,
                file=encoded_mask.tobytes(),
                file_options={"content-type": "image/png"}
            )
            
            return supabase.storage.from_(configs.SEGMENTATION_BUCKET).get_public_url(file_path)
            
        except Exception as upload_error:
            raise RuntimeError(f"Failed to upload result: {str(upload_error)}")