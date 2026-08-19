from pydantic import BaseModel


class SearchQuery(BaseModel):
    query: str
    limit: int = 12


class MovieResult(BaseModel):
    id: int
    title: str
    year: int | None = None
    director: str | None = None
    genre: str | None = None
    rating: float | None = None
    plot: str | None = None
    poster_url: str | None = None
    score: float

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    query: str
    cached: bool
    results: list[MovieResult]
