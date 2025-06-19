from typing import List

from sentence_transformers import SentenceTransformer
from llmrag.embeddings.base_embedder import BaseEmbedder

class SentenceTransformersEmbedder(BaseEmbedder):
    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(self, texts):
        return self.model.encode(texts).tolist()


    def embed_query(self, query: str) -> List[float]:
        return self.model.encode(query, convert_to_numpy=True).tolist()