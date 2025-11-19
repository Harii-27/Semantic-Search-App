import React, { useState } from "react";
import { searchAPI } from "../utils/api";

export default function SearchForm({ setResults }) {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    const data = await searchAPI(url, query);
    setResults(data);
  };

  return (
    <form onSubmit={submit}>
      <input type="text" placeholder="Website URL" value={url} onChange={(e) => setUrl(e.target.value)} /><br /><br />
      <input type="text" placeholder="Search Query" value={query} onChange={(e) => setQuery(e.target.value)} /><br /><br />
      <button type="submit">Search</button>
    </form>
  );
}
