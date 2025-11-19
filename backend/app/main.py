from fastapi import FastAPI, HTTPException
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
    """
    Search endpoint: Fetches URL, chunks content, and performs semantic search.
    Returns top 10 most relevant chunks.
    """
    try:
        # Fetch and clean HTML content
        text = fetch_clean_text(req.url)
        
        # Validate text was extracted
        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text content from the provided URL. The page might be empty or inaccessible."
            )
        
        # Chunk the text
        chunks = chunk_text(text)
        
        # Validate chunks were created
        if not chunks or len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to create text chunks from the URL content."
            )
        
        # Generate embeddings for chunks
        chunk_embeddings = embed_texts(chunks)
        
        # Initialize fresh database for this search
        global db
        db = init_db()
        
        # Add chunks to database
        add_to_db(db, chunks, chunk_embeddings)
        
        # Generate query embedding
        q_emb = embed_query(req.query)
        
        # Perform semantic search
        results = search_db(db, q_emb)
        
        # Validate results
        if not results or len(results) == 0:
            raise HTTPException(
                status_code=404,
                detail="No relevant results found for the given query."
            )
        
        return results
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during search: {str(e)}"
        )
