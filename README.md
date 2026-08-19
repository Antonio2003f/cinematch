# CineMatch

Motor de recomandari de filme bazat pe cautare semantica (nu keyword search),
construit ca proiect de portofoliu / invatare Docker multi-service.

## Status
Pas curent: PostgreSQL configurat si functional. Urmeaza: Redis, Qdrant, backend FastAPI, frontend Next.js, Nginx.

## Cum pornesti local
1. Copiaza `.env.example` in `.env` si completeaza valorile.
2. `docker compose up -d`
3. `docker compose ps` - asteapta status `healthy` pentru postgres.
