from typing import List
from langchain_core.documents import Document
from llmrag.embeddings.base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer

class SentenceTransformersEmbedder(BaseEmbedder):
    """
    Embedding model using SentenceTransformers.
sentence_transformer
    Args:
        model_name (str): Name of the SentenceTransformer model.
        device (str): Device to use ('cpu' or 'cuda').

    Methods:
        embed(texts: List[str]) -> List[List[float]]:
            Embed a batch of texts.
        embed_query(query: str) -> List[float]:
            Embed a single query.
        embed_documents(texts: List[str]) -> List[List[float]]:
            Embed multiple documents.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts.

        Args:
            texts (List[str]): The texts to embed.

        Returns:
            List[List[float]]: Embeddings for each text.
        """
        if texts and isinstance(texts[0], Document):
            texts = [doc.page_content for doc in texts]

        # Show progress for large batches
        if len(texts) > 100:
            print(f"[Embed] Generating embeddings for {len(texts)} chunks...")
        
        embeddings = self.model.encode(texts).tolist()
        
        if len(texts) > 100:
            print(f"[Embed] Completed embedding generation")
        
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            query (str): The query to embed.

        Returns:
            List[float]: The embedding vector.
        """
        return self.model.encode(query, convert_to_numpy=True).tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.

        Args:
            texts (List[str]): The documents to embed.

        Returns:
            List[List[float]]: List of embedding vectors.
        """
        # Show progress for large batches
        if len(texts) > 100:
            print(f"[Embed] Generating embeddings for {len(texts)} documents...")
        
        embeddings = self.model.encode(texts, convert_to_tensor=False).tolist()
        
        if len(texts) > 100:
            print(f"[Embed] Completed embedding generation")
        
        return embeddings
