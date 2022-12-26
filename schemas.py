from pydantic import BaseModel
from typing import List

class UploadVideo(BaseModel):
    title: str
    description: str
    tags: List[str]