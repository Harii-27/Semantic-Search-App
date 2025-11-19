import React from "react";

/**
 * Highlight all occurrences of query (case-insensitive) inside text.
 * Wrap matches with <mark>.
 */
function highlightText(text = "", query = "") {
  if (!query) return escapeHtml(text);
  // escape regex special chars
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escaped})`, "gi");

  // split and mark
  const parts = text.split(regex);
  return parts.map((part, idx) =>
    regex.test(part) ? (
      <mark key={idx} className="highlight">
        {part}
      </mark>
    ) : (
      <span key={idx}>{escapeHtml(part)}</span>
    )
  );
}

// simple HTML escape to avoid inserting raw HTML
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "<")
    .replace(/>/g, ">");
}

export default function ResultCard({ index, chunk, match, query }) {
  return (
    <div className="card">
      <div className="card-header">
        <div className="chunk-num">#{index}</div>
        <div className="match-score">{match}% match</div>
      </div>

      <div className="card-body">{highlightText(chunk, query)}</div>
    </div>
  );
}
