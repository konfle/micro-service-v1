from app.api.models import CastIn, CastOut, CastUpdate
from app.api.db import casts, database
from sqlalchemy import select


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_cast(cast_id: int):
    query = casts.select().where(cast_id == casts.c.id)

    return await database.fetch_one(query=query)
