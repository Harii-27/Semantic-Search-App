from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .scraper import fetch_clean_text
from .chunker import chunk_text
from .embeddings import embed_texts, embed_query
from .vectordb import init_db, add_to_db, search_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_methods=["*"],            
    allow_headers=["*"],     
)

db = init_db()

class SearchRequest(BaseModel):
    url: str
    query: str

@app.post("/search")
def search(req: SearchRequest):

    try:
        text = fetch_clean_text(req.url)
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text content from the provided URL. The page might be empty or inaccessible."
            )
        
        chunks = chunk_text(text)
        
        if not chunks or len(chunks) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to create text chunks from the URL content."
            )
        
        chunk_embeddings = embed_texts(chunks)
        
        global db
        db = init_db()
        
        add_to_db(db, chunks, chunk_embeddings)
        
        q_emb = embed_query(req.query)
        
        results = search_db(db, q_emb)
        
        if not results or len(results) == 0:
            raise HTTPException(
                status_code=404,
                detail="No relevant results found for the given query."
            )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during search: {str(e)}"
        )
