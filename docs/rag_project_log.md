# 📘 RAG Chatbot Project Log

## 🗓️ Session Start: June 18, 2025

---

## 🧠 Project Overview

This project aims to build a **modular, open-source Retrieval-Augmented Generation (RAG) chatbot system** in Python. The system is designed to:

- Support **multiple local LLMs** (like Mistral, LLaMA) via Hugging Face Transformers or other local tools
- Be **fully deployable on a PC** (with or without GPU)
- Use **swappable components** for models, embeddings, vector stores, and context pipelines
- Include a **command-line interface**, and optionally a web-based UI later

---

## ✅ User Preferences

- **Model source**: Local (Hugging Face / Ollama)
- **Hardware**: Mac with GPU (Apple Silicon)
- **Chunking first**, then embeddings
- Clear step-by-step approach with **detailed explanations**

---

## 📁 File: `main.py`

Entrypoint of the chatbot system. Dynamically loads components and loops for user input.

```python
"""
This is the foundational structure of a modular, reusable RAG (Retrieval-Augmented Generation) system.
It supports different LLMs, embedding models, and vector stores for local or hybrid chatbot applications.
This system is designed to be lightweight, open-source, and fully deployable on a standard PC.

Conversation notes:
- User wants a reusable, modular RAG chatbot system in Python.
- Must support multiple models and components (LLM, embeddings, vector store).
- Must be deployable on a PC without relying on the cloud.
- Prefer open-source libraries like FAISS, ChromaDB, llama.cpp, HuggingFace Transformers.
- This file documents the outline and purpose of the project for later expansion.
"""

from models import load_model
from embeddings import load_embedder
from retrievers import load_vector_store
from pipelines import RAGPipeline
from chunking import split_documents
import yaml

def main(config_path="configs/default.yaml"):
    config = yaml.safe_load(open(config_path))

    model = load_model(config["llm"])
    embedder = load_embedder(config["embedding"])
    retriever = load_vector_store(config["vector_store"], embedder)

    pipeline = RAGPipeline(model=model, retriever=retriever)

    print("RAG Chatbot System Ready. Type your question below:\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = pipeline.query(query)
        print("Bot:", response)

if __name__ == "__main__":
    main()
```

---

## 📁 Module: `models/`

### `base_model.py`

Defines a clean interface for all language models.

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Given a prompt, return a generated response.
        """
        pass
```

### `transformers_model.py`

Loads a Hugging Face Transformers model for local generation.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from .base_model import BaseModel

class TransformersModel(BaseModel):
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1", device: str = "cpu"):
        print(f"Loading model: {model_name} on {device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto" if device != "cpu" else None,
            torch_dtype="auto"
        )
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if device == "cuda" else -1)

    def generate(self, prompt: str) -> str:
        result = self.pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)
        return result[0]["generated_text"][len(prompt):].strip()
```

### `__init__.py`

Simple loader function based on config.

```python
from .transformers_model import TransformersModel

def load_model(config):
    model_type = config.get("type", "transformers")
    if model_type == "transformers":
        return TransformersModel(
            model_name=config.get("model_name", "mistralai/Mistral-7B-Instruct-v0.1"),
            device=config.get("device", "cpu")
        )
    else:
        raise NotImplementedError(f"Model type {model_type} not implemented.")
```

---

## 📁 Module: `chunking/`

### `text_splitter.py`

Implements both a simple and recursive text splitter.

```python
from typing import List

class SimpleSplitter:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def split(self, text: str) -> List[str]:
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        separators = ["\n\n", "\n", ".", " ", ""]
        return self._recursive_split(text, separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        for sep in separators:
            if sep and sep in text:
                parts = text.split(sep)
                chunks = []
                chunk = ""
                for part in parts:
                    if len(chunk) + len(part) + len(sep) <= self.chunk_size:
                        chunk += part + sep
                    else:
                        chunks.append(chunk.strip())
                        chunk = part + sep
                if chunk:
                    chunks.append(chunk.strip())

                if self.chunk_overlap > 0:
                    overlapped_chunks = []
                    for i in range(0, len(chunks)):
                        start = max(i - 1, 0)
                        joined = " ".join(chunks[start:i + 1])
                        overlapped_chunks.append(joined)
                    return overlapped_chunks

                return chunks

        return [text]
```

### `__init__.py`

Loader for chunker method based on config.

```python
from .text_splitter import RecursiveCharacterTextSplitter, SimpleSplitter

def split_documents(text: str, config: dict):
    method = config.get("method", "recursive")
    chunk_size = config.get("chunk_size", 500)
    chunk_overlap = config.get("chunk_overlap", 50)

    if method == "recursive":
        splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap)
    else:
        splitter = SimpleSplitter(chunk_size)

    return splitter.split(text)
```

---

## 📁 Module: `embeddings/`

### `base_embedder.py`

```python
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
```

### `sentence_transformers_embedder.py`

```python
from .base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer
from typing import List

class SentenceTransformersEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        print(f"Loading embedding model: {model_name} on {device}")
        self.model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode(query, convert_to_numpy=True).tolist()
```

### `__init__.py`

```python
from .sentence_transformers_embedder import SentenceTransformersEmbedder

def load_embedder(config):
    embed_type = config.get("type", "sentence-transformers")
    if embed_type == "sentence-transformers":
        return SentenceTransformersEmbedder(
            model_name=config.get("model_name", "all-MiniLM-L6-v2"),
            device=config.get("device", "cpu")
        )
    else:
        raise NotImplementedError(f"Embedder type {embed_type} not implemented.")
```

---

## 📁 Module: `retrievers/`

### What Are Vector Stores?

A **vector store** stores document embeddings and allows **efficient similarity search**. After your documents are chunked and embedded, the vector store helps find which chunks are most relevant to a user's query by comparing vector similarity (typically cosine distance).

### Popular Options

| Name         | Pros                                                           | Cons                                        |
| ------------ | -------------------------------------------------------------- | ------------------------------------------- |
| **FAISS**    | Fast, local, well-supported, good for small to medium datasets | No persistence unless manually saved/loaded |
| **ChromaDB** | Persistent, local database-like feel                           | Slightly more setup overhead                |
| **Qdrant**   | High-performance, Rust backend, persistent                     | Requires running a server                   |

For this prototype, we’ll use **FAISS** for its simplicity and speed.

### `base_vector_store.py`

```python
from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[str], embeddings: List[List[float]]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        pass
```

### `faiss_store.py`

```python
from .base_vector_store import BaseVectorStore
import faiss
import numpy as np
from typing import List, Tuple

class FAISSVectorStore(BaseVectorStore):
    def __init__(self):
        self.index = None
        self.documents = []

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
```

### `__init__.py`

```python
from .faiss_store import FAISSVectorStore

def load_vector_store(config, embedder):
    store_type = config.get("type", "faiss")
    if store_type == "faiss":
        store = FAISSVectorStore()

        if "documents" in config:
            texts = config["documents"]
            embeddings = embedder.embed_documents(texts)
            store.add_documents(texts, embeddings)

        return store
    else:
        raise NotImplementedError(f"Vector store type {store_type} not implemented.")
```

### ✅ Example Config Snippet

```yaml
vector_store:
  type: faiss
  documents: ["This is an example doc.", "Another one here."]
```

---

## 🔹 Next Step

Build the **RAG pipeline**:

- Combine model + retriever
- Format prompt with retrieved docs
- Handle user queries

