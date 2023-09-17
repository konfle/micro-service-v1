import asyncio

from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api import db_manager
from app.api.service import is_cast_present

movies = APIRouter()


@movies.get("/", response_model=List[MovieOut])
async def get_movies():
    return await db_manager.get_all_movies()


@movies.get("/{movie_id}/", response_model=MovieOut)
async def get_movie(movie_id: int):
    movie = await db_manager.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404,
                            detail=f"Movie with given id: {movie_id} not found")
    return movie


@movies.post("/", response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):

    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404,
                                detail=f"Cast with given id: {cast_id} not found")

    movie_id = await db_manager.add_movie(payload)

    response = {"id": movie_id, **payload.model_dump()}

    return response


@movies.put("/{movie_id}/", response_model=MovieOut)
async def update_movie(movie_id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(movie_id)

    if not movie:
        raise HTTPException(status_code=404,
                            detail=f"Movie with given id:{movie_id} not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "casts_id" in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404,
                                    detail=f"Cast with given id:{cast_id} not found")
    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.model_copy(update=update_data)

    movie_id = await db_manager.update_movie(movie_id, updated_movie)
    update_data["id"] = movie_id

    return await db_manager.update_movie(movie_id, updated_movie)


@movies.delete("/{movie_id}/", response_model=None)
async def delete_movie(movie_id: int):
    movie = await db_manager.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404,
                            detail=f"Movie with given id:{movie_id} not found")
    return await db_manager.delete_movie(movie_id)
