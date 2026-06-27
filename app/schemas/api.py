# app/schemas/api.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class JobRequest(BaseModel):
    text: str = Field(min_length=3, max_length=4000)
    language: str = "auto"
    material: str = "PLA"
    quality_mode: str = "production"

class JobResponse(BaseModel):
    job_id: str
    status: str
    build_allowed: bool
    message: str
    files: List[str]
    report: Dict
