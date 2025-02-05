import time
from typing import List, Optional
from fastapi import HTTPException
from app.core.config import supabase, configs
from app.schemas.user import SystemUser

class ImageService:
    @staticmethod
    async def upload_image(file_bytes: bytes, filename: str, user: SystemUser) -> dict:
        try:
            file_path = f"{configs.ORIGINAL_IMAGES_PATH}/{filename}"
            print(file_path)
            res = supabase.storage.from_(configs.MAIN_BUCKET).upload(
                file=file_bytes,
                path=file_path,
                file_options={"cache-control": "3600", "upsert": "true", "content_type": "image/jpeg"},
            )
            return {
                "id": file_path,
                "url": supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(file_path)
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Image upload failed: {str(e)}"
            )

    @staticmethod
    async def delete_image(image_id: str, user: SystemUser) -> bool:
        try:
            supabase.storage.from_(configs.ORIGINAL_IMAGES_PATH).remove([image_id])
            supabase.storage.from_(configs.SEGMENTED_IMAGES_PATH).remove([image_id])
            return True
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail="Image not found or already deleted"
            )

    @staticmethod
    async def list_images(user: SystemUser) -> List[dict]:
        try:
            original_files = supabase.storage.from_(configs.MAIN_BUCKET).list(configs.ORIGINAL_IMAGES_PATH)
            segmented_files = supabase.storage.from_(configs.MAIN_BUCKET).list(configs.SEGMENTED_IMAGES_PATH)
            
            original_dict = [{
                "id": f'{configs.ORIGINAL_IMAGES_PATH}/{file['name']}',
                "original_url": supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(f'{configs.ORIGINAL_IMAGES_PATH}/{file['name']}')
            } for file in original_files]
            
            segment_dict = [{
                "id": f.name,
                "segmented_url": supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(f['name'])
            } for f in segmented_files]
            
            print(l)
            
            return {}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list images: {str(e)}"
            )

    @staticmethod
    def get_image_url(image_id: str, bucket: str) -> str:
        try:
            return supabase.storage.from_(bucket).get_public_url(image_id)
        except:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )