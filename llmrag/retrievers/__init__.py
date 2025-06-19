from llmrag.retrievers.faiss_store import FAISSVectorStore

def load_vector_store(config, embedder):
    store_type = config.get("type", "faiss")
    if store_type == "faiss":
        return FAISSVectorStore(embedder)
    else:
        raise NotImplementedError(f"Vector store type {store_type} not implemented.")
