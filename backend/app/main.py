from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .scraper import fetch_clean_text
from .chunker import chunk_text
from .embeddings import embed_texts, embed_query
from .vectordb import init_db, add_to_db, search_db

app = FastAPI()

# --------------------------
# CORS ENABLED
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow all frontend origins
    allow_methods=["*"],     # allow all HTTP methods
    allow_headers=["*"],     # allow all headers
)

db = init_db()

class SearchRequest(BaseModel):
    url: str
    query: str

@app.post("/search")
def search(req: SearchRequest):
    text = fetch_clean_text(req.url)
    chunks = chunk_text(text)
    chunk_embeddings = embed_texts(chunks)
    add_to_db(db, chunks, chunk_embeddings)
    q_emb = embed_query(req.query)
    results = search_db(db, q_emb)
    return results
