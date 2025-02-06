from fastapi import APIRouter, Depends, HTTPException, status
from app.services.segmentation_services import SegmentationService
from app.core.deps import get_current_user
from app.core.config import configs
from app.core.model_loader import model, load_segmentation_model
from app.schemas.user import SystemUser
from app.schemas.segmentation import SegmentationResult
from app.services.image_services import ImageService


router = APIRouter(
    prefix="/segmentation",
    tags=["Image Segmentation"],
)

model = load_segmentation_model()

@router.post("/process/{image_name}", response_model=SegmentationResult)
async def process_image(image_name: str,current_user: SystemUser = Depends(get_current_user) ):
    try:
        segmentation_service = SegmentationService(model)
        image_path  = f'{configs.ORIGINAL_IMAGES_PATH}/{image_name}'
        image = ImageService.get_the_image(image_path, configs.MAIN_BUCKET)
        result = await segmentation_service.process_image(image, current_user.id, image_name)
        return {
            "original_url": ImageService.get_image_url(image_path, configs.MAIN_BUCKET),
            "segmented_url": result["segmented_url"],
            "processing_time": result["processing_time"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

