import os
import shutil
from typing import List
from urllib import response
from uuid import uuid4

from fastapi import (APIRouter, BackgroundTasks, File, Form, HTTPException,
                     Request, UploadFile)
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from models import User, Video
from schemas import GetListVideo, GetVideo, Message, UploadVideo
from services import open_file, save_video

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post("/")
async def create_video(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...)
):
    user = await User.objects.first()
    # file_name = f'media/{user.dict().get("id")}_{uuid4()}.mp4'
    return await save_video(user, file, title, description, background_tasks)


# @video_router.get("/video/{video_pk}")
# async def get_video(video_pk: int):
#     file = await Video.objects.select_related('user').get(pk=video_pk)
#     # video_path = os.path.join('media', file.dict().get('file'))
#     # video_path = os.path.join('media', file.file)
#     file_like = open(file.file, mode='rb')
#     return StreamingResponse(file_like, media_type="video/mp4")


@video_router.get('/user/{user_pk}', response_model=List[GetListVideo])
async def get_list_video(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


@video_router.get("index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html",{"request": request, "path": video_pk})

@video_router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type="video/mp4",
        status_code=status_code,
    )
    response.headers.update({
        'Accept-Ranges':'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response
