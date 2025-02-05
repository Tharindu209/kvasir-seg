from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import routers
from app.core.config import configs
from app.core.model_loader import load_segmentation_model

app = FastAPI()

if configs.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get('/')
def read_root():
    return {'message': 'welcome to the API for KVASIR segmentation prediction'} 

@app.on_event("startup")
async def startup_event():
    load_segmentation_model()

app.include_router(routers)