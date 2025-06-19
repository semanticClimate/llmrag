from typing import List
from llmrag.embeddings.base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer

class SentenceTransformersEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(self, texts: List[str]) -> List[List[float]]:
        # This is the embedding method expected by the rest of the code
        return self.model.encode(texts)