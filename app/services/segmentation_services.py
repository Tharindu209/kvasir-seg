import time
import cv2
import numpy as np
import torch
from io import BytesIO
from app.core.config import configs, supabase
from app.utils.image_processing import preprocess_image, postprocess_mask

class SegmentationService:
    def __init__(self, model):
        self.model = model
        self.device = torch.device(configs.DEVICE)
        self.model.to(self.device)

    async def process_image(self, file_bytes: bytes, user_id: str, filename: str) -> dict:
        start_time = time.time()
        try:
            image = preprocess_image(file_bytes)
            mask = self._run_inference(image)
            print(mask)
            result_url = await self._store_results(mask, user_id, filename)    
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
            
            preprocess_mask_image = postprocess_mask(output)
            return preprocess_mask_image

    async def _store_results(self, mask: np.ndarray, user_id: str, file_name: str) -> str:
        try:
            _, encoded_mask = cv2.imencode('.png', mask)
            file_path = f"{configs.SEGMENTED_IMAGES_PATH}/{file_name}"
            
            res = supabase.storage.from_(configs.MAIN_BUCKET).upload(
                file=encoded_mask.tobytes(),
                path=file_path,
                file_options={"cache-control": "3600", "upsert": "true", "content_type": "image/jpeg"},
            )
            return supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(file_path)
            
        except Exception as upload_error:
            raise RuntimeError(f"Failed to upload result: {str(upload_error)}")