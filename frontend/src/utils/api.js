export async function searchAPI(url, query) {
  const res = await fetch("http://127.0.0.1:8000/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, query })
  });
  return await res.json();
}
