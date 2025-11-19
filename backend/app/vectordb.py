import chromadb

def init_db():
    client = chromadb.Client()

    try:
        client.delete_collection("web_chunks")
    except:
        pass

    return client.create_collection("web_chunks")


def add_to_db(db, chunks, embeddings):
    if not chunks or len(chunks) == 0:
        raise Exception("Cannot add empty chunks to database")
    
    if len(chunks) != len(embeddings):
        raise Exception("Mismatch between chunks and embeddings count")
    
    ids = [f"id_{i}" for i in range(len(chunks))]
    db.add(ids=ids, embeddings=embeddings, documents=chunks)


def search_db(db, query_emb):
 
    try:
        results = db.query(query_embeddings=[query_emb], n_results=10)
        docs = results["documents"][0]
        distances = results["distances"][0]

        if not docs or len(docs) == 0:
            return []

  
        results_list = []
        for i in range(len(docs)):
            distance = float(distances[i])
           
            percentage = max(0, min(100, (1 - distance / 6.0) * 100))
            
            results_list.append({
                "chunk": docs[i],
                "match": round(percentage, 0) 
            })
        
        return results_list
    except Exception as e:
        raise Exception(f"Database search failed: {str(e)}")
