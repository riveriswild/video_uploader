import databases
import sqlalchemy
from fastapi import FastAPI
from api import video_router
import ormar

app = FastAPI()
metadata = sqlalchemy.MetaData()  # to work with sqlalchemy orm that generates requests
database = databases.Database("sqlite:///sqlite.db")
app.state.database = database  # add property database to app object


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(video_router)
