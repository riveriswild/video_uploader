from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    name: str


class UploadVideo(BaseModel):
    title: str
    description: str
    # tags: List[str] = None


class GetVideo(BaseModel):
    user: User
    video: UploadVideo
