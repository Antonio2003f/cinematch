from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import SearchQuery, SearchResponse
from app.search import semantic_search

app = FastAPI(title="CineMatch API")

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
