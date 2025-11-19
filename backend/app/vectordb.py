import chromadb

def init_db():
    """
    Initialize a fresh ChromaDB collection for storing web chunks.
    Deletes old collection if it exists to ensure clean state.
    """
    # Create fresh client
    client = chromadb.Client()

    # Delete old collection if exists (prevents old chunks being reused)
    try:
        client.delete_collection("web_chunks")
    except:
        pass

    # Create a new clean collection every run
    return client.create_collection("web_chunks")


def add_to_db(db, chunks, embeddings):
    """
    Add chunks and their embeddings to the vector database.
    """
    if not chunks or len(chunks) == 0:
        raise Exception("Cannot add empty chunks to database")
    
    if len(chunks) != len(embeddings):
        raise Exception("Mismatch between chunks and embeddings count")
    
    ids = [f"id_{i}" for i in range(len(chunks))]
    db.add(ids=ids, embeddings=embeddings, documents=chunks)


def search_db(db, query_emb):
    """
    Search the vector database for most relevant chunks.
    Returns top 10 results with match percentage (0-100%).
    Converts distance score to percentage match.
    """
    try:
        results = db.query(query_embeddings=[query_emb], n_results=10)
        docs = results["documents"][0]
        distances = results["distances"][0]

        if not docs or len(docs) == 0:
            return []

        # Convert distance to percentage match
        # Cosine distance ranges from 0 (identical) to ~2 (completely different)
        # Formula: percentage = max(0, min(100, (1 - distance/2) * 100))
        results_list = []
        for i in range(len(docs)):
            distance = float(distances[i])
            # Convert distance to percentage: 0 distance = 100%, 2 distance = 0%
            percentage = max(0, min(100, (1 - distance / 2) * 100))
            results_list.append({
                "chunk": docs[i],
                "match": round(percentage, 0)  # Round to whole number
            })
        
        return results_list
    except Exception as e:
        raise Exception(f"Database search failed: {str(e)}")
