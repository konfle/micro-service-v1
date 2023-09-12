from fastapi import FastAPI
from python_microservices.cast_service.app.api.casts import casts
from python_microservices.cast_service.app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(casts, prefix="/api/v1/casts", tags=["casts"])
