from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    },
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]


class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]


@app.get('/', response_model=List[Movie])
async def index():
    return fake_movie_db


@app.post('/', status_code=201)
async def add_movie(payload: Movie):
    movie = dict(payload)
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}


@app.put('/{id}')  # Where movie_id is an index of fake_movie_db
async def update_movie(movie_id: int, payload: Movie):
    movie = dict(payload)
    movies_length = len(fake_movie_db)
    if 0 <= movie_id <= movies_length:
        fake_movie_db[movie_id] = movie
        return None
    raise HTTPException(status_code=404,
                        detail="Movie with given id not found")


@app.delete('/{id}')  # Where movie_id is an index of fake_movie_db
async def delete_movie(movie_id: int):
    movies_length = len(fake_movie_db)
    if 0 <= movie_id <= movies_length:
        del fake_movie_db[movie_id]
        return None
    raise HTTPException(status_code=404, detail="Movie with given id not found")
