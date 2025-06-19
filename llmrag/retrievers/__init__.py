from llmrag.retrievers.chroma_store import ChromaVectorStore

def load_vector_store(config, embedder, persist=True, collection_name="rag_collection"):
    name = config["type"] if isinstance(config, dict) else config
    if name == "chroma":
        return ChromaVectorStore(embedder, collection_name=collection_name, persist=persist)
    elif name == "faiss":
        try:
            from llmrag.retrievers.faiss_store import FAISSVectorStore
        except ImportError:
            raise ImportError("FAISS not installed. Install with 'pip install faiss-cpu' or switch to chroma.")
        return FAISSVectorStore(embedder)
    else:
        raise ValueError(f"Unknown vector store: {name}")