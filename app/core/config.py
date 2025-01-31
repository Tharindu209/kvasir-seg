import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ENV: str = ""

class Configs(BaseSettings):
    # base
    ENV: str = os.getenv("ENV", "dev")
    API: str = "/api"
    PROJECT_NAME: str = "fca-api"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        case_sensitive = True


configs = Configs()
