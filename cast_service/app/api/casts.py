from fastapi import APIRouter, HTTPException, Request
from typing import List

from app.api.models import CastOut, CastIn, CastUpdate
from app.api import db_manager

casts = APIRouter()


@casts.get(path="/", response_model=List[CastOut])
async def get_all_cast(request: Request):
    if request.query_params:
        raise HTTPException(status_code=400,
                            detail="This endpoint does not support query parameters.")
    return await db_manager.get_all_casts()


@casts.post(path="/", response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await db_manager.add_cast(payload)

    response = {
        "id": cast_id,
        **payload.model_dump()
    }

    return response


@casts.get(path="/{cast_id}/", response_model=CastOut)
async def get_cast_by_id(cast_id: int):
    cast = await db_manager.get_cast_by_id(cast_id)
    if not cast:
        raise HTTPException(status_code=404,
                            detail=f"Cast with given id {cast_id} not found")
    return cast


@casts.put(path="/{cast_id}/", response_model=CastOut)
async def update_cast(cast_id: int, payload: CastUpdate):
    cast = await db_manager.get_cast_by_id(cast_id)

    if not cast:
        raise HTTPException(status_code=404,
                            detail=f"Cast with given id {cast_id} not found")

    update_data = payload.model_dump(exclude_unset=True)

    cast_in_db = CastIn(**cast)

    updated_cast = cast_in_db.model_copy(update=update_data)
    cast_id = await db_manager.update_cast(cast_id, updated_cast)

    update_data["id"] = cast_id

    return update_data
