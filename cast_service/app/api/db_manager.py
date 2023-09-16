from app.api.models import CastIn, CastOut, CastUpdate
from app.api.db import casts, database
from sqlalchemy import select


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_casts():
    query = casts.select()
    return await database.fetch_all(query=query)


async def get_cast_by_id(cast_id: int):
    query = casts.select().where(cast_id == casts.c.id)

    return await database.fetch_one(query=query)
