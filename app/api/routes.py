from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.image import router as image_router
from app.api.endpoints.segmentation import router as segmentation_router


routers = APIRouter()
router_list = [auth_router, image_router, segmentation_router]

for router in router_list:
    routers.include_router(router)
