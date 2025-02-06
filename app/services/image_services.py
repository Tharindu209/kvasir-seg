import time
from typing import List
import requests
from fastapi import HTTPException
from app.core.config import supabase, configs
from app.schemas.user import SystemUser

class ImageService:
    @staticmethod
    async def upload_image(file_bytes: bytes, filename: str, user: SystemUser) -> dict:
        try:
            file_path = f"{configs.ORIGINAL_IMAGES_PATH}/{filename}"
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
                "id": f'{configs.ORIGINAL_IMAGES_PATH}/{file["name"]}',
                "original_url": supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(f'{configs.ORIGINAL_IMAGES_PATH}/{file["name"]}')
            } for file in original_files]
            
            segment_dict = [{
                "id": f'{configs.SEGMENTED_IMAGES_PATH}/{file["name"]}',
                "segmented_url": supabase.storage.from_(configs.MAIN_BUCKET).get_public_url(f'{configs.SEGMENTED_IMAGES_PATH}/{file["name"]}')
            } for file in segmented_files]
            
            return [
                {
                    "original": original_dict,
                    "segmented": segment_dict
                }
            ]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list images: {str(e)}"
            )

    def get_image_url(image_id: str, bucket: str) -> str:
        try:
            res = supabase.storage.from_(bucket).get_public_url(image_id)
            
            response = requests.get(res)
            if response.status_code == 200:
                return res
            else:
                raise Exception(f"Failed to access the image URL: {res}")
        except:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )
            
    def get_the_image(image_id: str, bucket: str) -> bytes:
        try:
            res = supabase.storage.from_(bucket).download(image_id)
            return res
        except:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )