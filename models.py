import datetime
from typing import Optional, Union

import ormar
from db import metadata, database


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMeta):
        pass

    id: str = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100)


class Video(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Union[User, int, None] = ormar.ForeignKey(User)

