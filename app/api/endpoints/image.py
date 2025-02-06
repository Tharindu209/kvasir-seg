from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.services.image_services import ImageService
from app.core.deps import get_current_user
from app.schemas.user import SystemUser
from app.core.config import configs
from typing import List

router = APIRouter(
    prefix="/image",
    tags=["Image Operations"],
)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image( file: UploadFile = File(...), current_user: SystemUser = Depends(get_current_user)):
    try:
        file_bytes = await file.read()
        return await ImageService.upload_image(file_bytes, file.filename, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{image_id}")
async def delete_image(image_id: str,current_user: SystemUser = Depends(get_current_user)):
    success = await ImageService.delete_image(image_id, current_user)
    if success:
        return {"message": "Images deleted successfully"}
    raise HTTPException(status_code=404, detail="Images not found")

@router.get("/", response_model=List[dict])
async def list_images(current_user: SystemUser = Depends(get_current_user)):
    return await ImageService.list_images(current_user)

@router.get("/original/{image_id}")
async def get_original_image(image_id: str):
    image_id = f"{configs.ORIGINAL_IMAGES_PATH}/{image_id}"
    return {"url": ImageService.get_image_url(image_id, configs.MAIN_BUCKET)}

@router.get("/segmented/{image_id}")
async def get_segmented_image(image_id: str):
    image_id = f"{configs.SEGMENTED_IMAGES_PATH}/{image_id}"
    return {"url": ImageService.get_image_url(image_id, configs.MAIN_BUCKET)}