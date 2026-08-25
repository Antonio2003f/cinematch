import json
import time
import requests

with open("scripts/movies.json", encoding="utf-8") as f:
    movies = json.load(f)

LIMIT = 5000  # scoate limita cand testul merge bine

url = "http://localhost:18000/movies"

for i, m in enumerate(movies[:LIMIT], 1):
    payload = {
        "title": m["title"],
        "year": m.get("year"),
        "director": m.get("director"),
        "genre": m.get("genre"),
        "rating": m.get("rating"),
        "plot": m["plot"],
        "poster_url": m.get("poster_url"),
    }
    r = requests.post(url, json=payload)
    print(f"{i}/{LIMIT}: {m['title']} -> {r.status_code}")
    time.sleep(0.05)

print("Gata.")
