import chromadb

def init_db():
    # Create fresh client
    client = chromadb.Client()

    # Delete old collection if exists (prevents old example.com chunks being reused)
    try:
        client.delete_collection("web_chunks")
    except:
        pass

    # Create a new clean collection every run
    return client.create_collection("web_chunks")


def add_to_db(db, chunks, embeddings):
    ids = [f"id_{i}" for i in range(len(chunks))]
    db.add(ids=ids, embeddings=embeddings, documents=chunks)


def search_db(db, query_emb):
    results = db.query(query_embeddings=[query_emb], n_results=10)
    docs = results["documents"][0]
    scores = results["distances"][0]

    return [{"chunk": docs[i], "score": scores[i]} for i in range(len(docs))]
