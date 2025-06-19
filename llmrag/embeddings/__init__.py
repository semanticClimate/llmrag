from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder

def load_embedder(config):
    embed_type = config.get("type", "sentence-transformers")
    if embed_type == "sentence-transformers":
        return SentenceTransformersEmbedder(
            model_name=config.get("model_name", "all-MiniLM-L6-v2"),
            device=config.get("device", "cpu")
        )
    else:
        raise NotImplementedError(f"Embedder type {embed_type} not implemented.")
