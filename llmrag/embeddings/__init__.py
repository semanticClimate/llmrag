from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder

def load_embedder(config):
    return SentenceTransformersEmbedder(
        model_name=config.get("model_name", "all-MiniLM-L6-v2"),
        device=config.get("device", "cpu")
    )
