import shutil
from typing import List
from urllib import response

from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse

from schemas import UploadVideo, GetVideo, Message
from models import Video, User

video_router = APIRouter()


@video_router.post("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file = file.filename, user=user, **info.dict())


# @video_router.post("/img")
# async def upload_image(files: List[UploadFile] = File(...)):
#     for img in files:
#         with open(f'{img.filename}', 'wb') as buffer:
#             shutil.copyfileobj(img.file, buffer)
#     return {"file_name": img.filename}


# @video_router.post("/info")
# async def info_set(info: UploadVideo):
#     return info

# @video_router.post("/video")
# async def create_video(video: Video):
#     await video.save()
#     return video

# @video_router.get("/video/{video_pk}", response_model=Video, responses={404: {"model": Message}})
@video_router.get("/video/{video_pk}", response_model=GetVideo, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related('user').get(pk=video_pk)

@video_router.get("/test")
async def get_test(req: Request):
    return {}

# https://www.youtube.com/watch?v=X2M2LY2Sb78&list=PLaED5GKTiQG-nG7rJiBE8vq9yVEq-5pzm&index=3