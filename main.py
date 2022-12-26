from fastapi import FastAPI

from api import video_router

app = FastAPI()  # create fastapi obj


app.include_router(video_router)
