import React, { useState } from "react";
import ResultCard from "./components/ResultCard";

function App() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function validateUrl(value) {
    try {
      const u = new URL(value);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch {
      return false;
    }
  }

  const handleSubmit = async (e) => {
    e?.preventDefault();
    setError("");
    setResults([]);

    if (!url || !query) {
      setError("Please enter both URL and search query.");
      return;
    }

    if (!validateUrl(url)) {
      setError("Please enter a valid URL (include http:// or https://).");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, query }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`Server error: ${res.status} ${txt}`);
      }

      const data = await res.json();
      // ensure array
      setResults(Array.isArray(data) ? data : []);
      if (!Array.isArray(data) || data.length === 0) {
        setError("No results found for this query / page.");
      }
    } catch (err) {
      setError("Request failed: " + (err.message || err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Semantic Search App</h1>

      <form className="form" onSubmit={handleSubmit}>
        <input
          className="input"
          type="text"
          placeholder="Enter website URL (include http:// or https://)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <input
          className="input"
          type="text"
          placeholder="Enter search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="controls">
          <button className="btn" type="submit" disabled={loading}>
            Search
          </button>

          {loading && (
            <div className="loader" aria-hidden="true" title="Searching..."></div>
          )}
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      <h2 className="results-title">Results:</h2>

      <div className="results-scroll">
        {results.map((r, i) => (
          <ResultCard
            key={i}
            index={i + 1}
            chunk={r.chunk}
            score={r.score}
            query={query}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
