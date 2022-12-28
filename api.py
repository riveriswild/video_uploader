from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates
import os

import shutil
from typing import List
from urllib import response

from fastapi import APIRouter, UploadFile, File, Form, Request,HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from schemas import UploadVideo, GetVideo, Message
from models import Video, User
from services import write_video

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post("/")
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    file_name = f'media/{file.filename}'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")
    info = UploadVideo(title=title, description=description)
    user = await User.objects.first()
    return await Video.objects.create(file=file.filename, user=user, **info.dict())


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
@video_router.get("/video/{video_pk}", responses={404: {"model": Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related('user').get(pk=video_pk)
    print(file)
    video_path = os.path.join('media', file.dict().get('file'))
    file_like = open(video_path, mode='rb')
    return StreamingResponse(file_like, media_type="video/mp4")

# @video_router.get("/test")
# async def get_test(req: Request):
#     return {}

# https://www.youtube.com/watch?v=X2M2LY2Sb78&list=PLaED5GKTiQG-nG7rJiBE8vq9yVEq-5pzm&index=3