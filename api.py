import shutil
from typing import List

from fastapi import APIRouter, UploadFile, File, Form

from schemas import UploadVideo

video_router = APIRouter()


@video_router.post("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename, 'info': info}


@video_router.post("/img")
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)
    return {"file_name": img.filename}


@video_router.post("/info")
async def info_set(info: UploadVideo):
    return info


@video_router.get("/info")
async def info_get():
    title = 'Test'
    desc = 'Description'
    return UploadVideo(title=title, description=desc)
