import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from supabase import create_client, Client

load_dotenv(verbose=True)

ENV: str = ""

class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    API: str = "/api"
    PROJECT_NAME: str = "Image-api"
    # model_path: str = "models/best_model.pth"
    allowed_file_types: list = ["image/jpeg", "image/png", "application/dicom"]
    supabase_url: str = os.getenv("SUPABASE_URL")
    supabase_key: str = os.getenv("SUPABASE_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    ORIGINAL_IMAGES_BUCKET: str = "original_images"
    SEGMENTED_IMAGES_BUCKET: str = "segment_images"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


configs = Configs()
supabase: Client = create_client(configs.supabase_url, configs.supabase_key)
