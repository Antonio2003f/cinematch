from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas import SearchQuery, SearchResponse
from app.search import semantic_search
from app.mq import publish_movie_ingestion
from app.models import Movie
from app.db import get_db
from pydantic import BaseModel


app = FastAPI(title="CineMatch API")

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(payload: SearchQuery):
    results, cached = semantic_search(payload.query, payload.limit)
    return SearchResponse(query=payload.query, cached=cached, results=results)


class MovieCreate(BaseModel):
    title: str
    year: int | None = None
    director: str | None = None
    genre: str | None = None
    rating: float | None = None
    plot: str
    poster_url: str | None = None


@app.post("/movies")
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)

    publish_movie_ingestion(movie.id, movie.title, movie.plot)
    return {"status": "queued", "movie_id": movie.id}