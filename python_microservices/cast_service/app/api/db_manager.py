from python_microservices.cast_service.app.api.models import CastIn, CastOut, CastUpdate
from python_microservices.cast_service.app.api.db import casts, database


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_cast(cast_id):
    query = casts.select(casts.c.id == cast_id)
    return await database.fetch_one(query=query)
