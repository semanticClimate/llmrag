from abc import ABC, abstractmethod
from typing import List

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate an embedding for a single query."""
        pass