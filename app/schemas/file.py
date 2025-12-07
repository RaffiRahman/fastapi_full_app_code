from fastapi import FastAPI
from pydantic import BaseModel

class UploadResponse(BaseModel):
    """Response model for uploaded files"""
    url: str