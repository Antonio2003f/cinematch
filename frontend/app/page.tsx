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
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare necunoscuta");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1 style={{ marginBottom: "0.4rem" }}>CineMatch</h1>
      <p style={{ color: "#999", marginBottom: "2rem" }}>
        Descrie ce vrei sa vezi, nu cauta cuvinte cheie.
      </p>

      <form className="search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="ex: case bantuite cu atmosfera onirica"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Caut..." : "Cauta"}
        </button>
      </form>

      {error && <p style={{ color: "#ff6b6b", marginBottom: "1rem" }}>{error}</p>}

      <div className="grid">
        {results.map((movie) => (
          <div className="card" key={movie.id}>
            {movie.poster_url && (
              <Image
                src={movie.poster_url}
                alt={movie.title}
                width={300}
                height={450}
                unoptimized
              />
            )}
            <div className="card-body">
              <div className="card-title">{movie.title}</div>
              <div className="card-meta">
                {movie.year} · {movie.director}
              </div>
              <div className="card-meta">scor: {movie.score.toFixed(3)}</div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
