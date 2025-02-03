from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.user import SystemUser
from app.core.config import supabase
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/upload",
    tags=["Image OPerations"],
)

@router.post('/image', summary="Upload image")
async def upload_image(user: SystemUser = Depends(get_current_user)):
    try:
        response = supabase.storage.from_('images').upload('file_name', 'file_path')
        return {"message": "Image uploaded"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )