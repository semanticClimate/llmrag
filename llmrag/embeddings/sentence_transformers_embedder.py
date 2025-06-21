from typing import List
from sentence_transformers import SentenceTransformer
from llmrag.embeddings.base_embedder import BaseEmbedder

class SentenceTransformersEmbedder(BaseEmbedder):
    """
    Embedding model using SentenceTransformers.
sentence_transformer
    Args:
        model_name (str): Name of the SentenceTransformer model.
        device (str): Device to use ('cpu' or 'cuda').

    Methods:
        embed(texts: list[str]) -> list[list[float]]:
            Embed a batch of texts.
        embed_query(query: str) -> list[float]:
            Embed a single query.
        embed_documents(texts: list[str]) -> list[list[float]]:
            Embed multiple documents.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(self, texts):
        """
        Embed a batch of texts.

        Args:
            texts (list[str]): The texts to embed.

        Returns:
            list[list[float]]: Embeddings for each text.
        """
        return self.model.encode(texts).tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            query (str): The query to embed.

        Returns:
            list[float]: The embedding vector.
        """
        return self.model.encode(query, convert_to_numpy=True).tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple documents.

        Args:
            texts (list[str]): The documents to embed.

        Returns:
            list[list[float]]: List of embedding vectors.
        """
        return self.model.encode(texts, convert_to_tensor=False).tolist()
