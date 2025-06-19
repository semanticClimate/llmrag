"""
### What Are Vector Stores?

A **vector store** stores document embeddings and allows **efficient similarity search**. After your documents are chunked and embedded, the vector store helps find which chunks are most relevant to a user's query by comparing vector similarity (typically cosine distance).

### Popular Options

| Name         | Pros                                                           | Cons                                        |
| ------------ | -------------------------------------------------------------- | ------------------------------------------- |
| **FAISS**    | Fast, local, well-supported, good for small to medium datasets | No persistence unless manually saved/loaded |
| **ChromaDB** | Persistent, local database-like feel                           | Slightly more setup overhead                |
| **Qdrant**   | High-performance, Rust backend, persistent                     | Requires running a server                   |

For this prototype, we’ll use **FAISS** for its simplicity and speed.

"""
from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[str], embeddings: List[List[float]]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        pass