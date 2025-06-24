import logging
import shutil
import tempfile
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from langchain.schema import Document

from llmrag.retrievers.base_vector_store import BaseVectorStore

logger = logging.getLogger(__name__)

class ChromaVectorStore(BaseVectorStore):
    def __init__(self, embedder, collection_name="rag_collection", persist=True):
        self.embedder = embedder
        self.collection_name = collection_name
        self.should_persist = persist

        if self.should_persist:
            self.chroma_path = "./chroma_db"
        else:
            # Use a temporary directory for test
            self._temp_dir = tempfile.mkdtemp()
            self.chroma_path = self._temp_dir

        self.client = chromadb.PersistentClient(
            path=self.chroma_path,
            settings=Settings(anonymized_telemetry=False)
        )
        self.docs = []
        self.collection = self.client.get_or_create_collection(self.collection_name)

    def persist(self):
        if self.should_persist and hasattr(self.client, "persist"):
            self.client.persist()
    # =================

    def similarity_search(self, query: str, top_k: int = 3):
        """
        Compatibility method for tests expecting a `similarity_search` method.
        Internally calls the `retrieve()` method.

        Args:
            query (str): The user query.
            top_k (int): Number of top results to return.

        Returns:
            List[Document]: Top matching documents.
        """
        return self.retrieve(query, top_k)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        if self.collection is None:
            raise ValueError("No collection initialized.")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "distances"]
        )

        docs = results["documents"][0]
        distances = results["distances"][0]
        return list(zip(docs, distances))

    def add_texts(self, texts: list[str]):
        embeddings = self.embedder.embed_documents(texts)
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids)

    def cleanup(self):
        # Only cleanup if it was a temp dir
        if not self.should_persist and hasattr(self, "_temp_dir"):
            shutil.rmtree(self._temp_dir, ignore_errors=True)


    def add_documents(self, docs: list[Document]):
        for i, doc in enumerate(docs):
            logger.info(f"doc_type {type(doc)}")
            self.collection.add(
                documents=[doc.page_content],
                metadatas=[doc.metadata],
                ids=[f"doc-{len(self.collection.get()['ids']) + i}"]
            )


    def retrieve(self, query: str, top_k=4) -> list[Document]:
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return [
            Document(
                page_content=text,
                metadata=meta if meta is not None else {}
            )
            for text, meta in zip(results["documents"][0], results["metadatas"][0])
        ]