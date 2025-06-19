import faiss
import numpy as np
from typing import List, Tuple
from llmrag.embeddings.base_embedder import BaseEmbedder

class FAISSVectorStore:
    def __init__(self, embedder: BaseEmbedder):
        self.index = None
        self.documents = []
        self.embedder = embedder

    def add_documents(self, documents: List[str], embeddings: List[List[float]]) -> None:
        dim = len(embeddings[0])
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(documents)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        query = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(dist)))
        return results

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        query_embedding = self.embedder.embed([query])[0]
        results = self.search(query_embedding, top_k)
        return [doc for doc, _ in results]
