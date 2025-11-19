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
        // Try to parse JSON error response
        let errorMessage = `Server error: ${res.status}`;
        try {
          const errorData = await res.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch {
          // If not JSON, try text
          const txt = await res.text();
          errorMessage = txt || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const data = await res.json();
      // ensure array
      setResults(Array.isArray(data) ? data : []);
      if (!Array.isArray(data) || data.length === 0) {
        setError("No results found for this query / page.");
      }
    } catch (err) {
      setError(err.message || "Request failed. Please check the URL and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Website Content Search</h1>
        <p className="subtitle">Search through website content with precision</p>
      </div>

      <form className="form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <span className="input-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
          </span>
          <input
            className="input"
            type="text"
            placeholder="Enter website URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div className="input-wrapper query-wrapper">
          <span className="input-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </span>
          <input
            className="input query-input"
            type="text"
            placeholder="Enter your search query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
      </form>

      {error && <div className="error">{error}</div>}

      {results.length > 0 && (
        <>
          <h2 className="results-title">Search Results:</h2>
          <div className="results-scroll">
            {results.map((r, i) => (
              <ResultCard
                key={i}
                index={i + 1}
                chunk={r.chunk}
                match={r.match}
                query={query}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
