import os
from pathlib import Path
from langchain_core.documents import Document
from llmrag.models import load_model
from llmrag.embeddings import load_embedder
from llmrag.retrievers import load_vector_store

def load_documents_from_file(file_path: str) -> list[Document]:
    ext = Path(file_path).suffix.lower()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return [Document(page_content=content, metadata={"source": file_path, "format": ext[1:]})]

def load_documents_from_dir(directory: str) -> list[Document]:
    documents = []
    for root, _, files in os.walk(directory):
        for fname in files:
            if fname.lower().endswith((".txt", ".html", ".htm")):
                path = os.path.join(root, fname)
                documents.extend(load_documents_from_file(path))
    return documents

def build_pipeline(model_name: str, embedding_model: str, vector_store_type: str, documents: list[Document]):
    model = load_model({"model_name": model_name, "device": "cpu"})
    embedder = load_embedder({"model_name": embedding_model, "device": "cpu"})
    vector_store = load_vector_store({"type": vector_store_type}, embedder)

    if documents:
        vector_store.add_documents(documents)

    from llmrag.pipelines.rag_pipeline import RAGPipeline
    return RAGPipeline(model=model, vector_store=vector_store)
