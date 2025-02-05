from pydantic import BaseModel

class SegmentationResult(BaseModel):
    original_url: str
    segmented_url: str
    processing_time: float

class SegmentationError(BaseModel):
    detail: str
    error_type: str