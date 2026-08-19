"use client";

import { useState } from "react";
import Image from "next/image";

type Movie = {
  id: number;
  title: string;
  year: number | null;
  director: string | null;
  genre: string | null;
  rating: number | null;
  poster_url: string | null;
  plot?: string | null;
  score: number;
};

// In Docker, cererea din browser merge catre Nginx (acelasi origin),
// nu direct catre backend - Nginx face proxy la /api catre serviciul backend.
const API_URL = "/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, limit: 12 }),
      });
      if (!res.ok) throw new Error(`Eroare server: ${res.status}`);
      const data = await res.json();
      setResults(data.results);
      setSearched(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare necunoscuta");
    } finally {
      setLoading(false);
    }
  }

  // Scorul brut de similaritate cosinus nu se citeste intuitiv ca procent -
  // afisam potrivirea relativa la cel mai bun rezultat din setul curent.
  const maxScore = results.length ? Math.max(...results.map((m) => m.score)) : 1;

  return (
    <main>
      <div className="eyebrow">motor de recomandari · cautare semantica</div>
      <h1>CineMatch</h1>
      <p className="tagline">
        Descrie o senzatie, o tema, o atmosfera — nu un titlu. Motorul citeste
        intelesul, nu cuvintele exacte.
      </p>

      <form className="search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="ex: case bantuite cu atmosfera onirica"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Caut" : "Cauta"}
        </button>
      </form>

      {error && <p className="error-text">{error}</p>}

      {!searched && !error && (
        <div className="empty-state">
          <strong>Sala e goala, ecranul asteapta.</strong>
          Scrie o descriere si apasa Cauta.
        </div>
      )}

      <div className="grid">
        {results.map((movie) => (
          <div className="card" key={movie.id} tabIndex={0}>
            <div className="card-poster">
              {movie.poster_url && (
                <Image
                  src={movie.poster_url}
                  alt={movie.title}
                  fill
                  unoptimized
                  sizes="(max-width: 640px) 45vw, 190px"
                />
              )}
              <div className="card-reveal">
                <p className="card-plot">{movie.plot || "Fara descriere disponibila."}</p>
              </div>
            </div>
            <div className="card-body">
              <div className="card-title">{movie.title}</div>
              <div className="card-meta">
                {movie.year ?? "—"} · {movie.director ?? "regizor necunoscut"}
              </div>
              <div className="match-bar">
                <div
                  className="match-bar-fill"
                  style={{ width: `${Math.round((movie.score / maxScore) * 100)}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
