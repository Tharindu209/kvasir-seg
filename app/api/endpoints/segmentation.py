from fastapi import APIRouter, Depends, HTTPException, status
from app.services.segmentation_services import SegmentationService
from app.core.deps import get_current_user
from app.schemas.user import SystemUser
from app.schemas.segmentation import SegmentationResult

router = APIRouter(
    prefix="/segmentation",
    tags=["Image Segmentation"],
)

@router.post("/process/{image_id}", response_model=SegmentationResult)
async def process_image(
    image_id: str,
    current_user: SystemUser = Depends(get_current_user)
    ):
    
    try:
        result = await segmentation_service.process_image(image_id, current_user)
        return {
            "original_url": result["original_url"],
            "segmented_url": result["segmented_url"],
            "processing_time": result["processing_time"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
