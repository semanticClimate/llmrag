import argparse
import os
from llmrag.models import load_model
from llmrag.embeddings import load_embedder
from llmrag.retrievers import load_vector_store
from llmrag.pipelines.rag_pipeline import RAGPipeline
from langchain_core.documents import Document
from pathlib import Path

from llmrag.utils.pipeline_setup import (
    load_documents_from_file,
    load_documents_from_dir,
    build_pipeline
)

def load_documents_from_file(file_path: str) -> list[Document]:
    """Load a text or HTML file as a Document with metadata."""
    ext = Path(file_path).suffix.lower()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return [Document(page_content=content, metadata={"source": file_path, "format": ext[1:]})]


def parse_args():
    parser = argparse.ArgumentParser(description="Run a CLI RAG pipeline")

    parser.add_argument("--query", type=str, help="The input query to answer")
    parser.add_argument("--context_file", type=str, help="A single file to load as context")
    parser.add_argument("--context_dir", type=str, help="Directory of documents to load as context")

    parser.add_argument("--model_name", type=str, default="gpt2", help="Name of the LLM to use")
    parser.add_argument("--embedding_model", type=str, default="all-MiniLM-L6-v2", help="Sentence transformer model")
    parser.add_argument("--vector_store_type", type=str, default="chroma", help="Vector store type: chroma or faiss")

    return parser.parse_args()


def main():
    args = parse_args()

    print("📦 Loading model...")
    model = load_model({"model_name": args.model_name, "device": "cpu"})

    print("🔗 Loading embedder...")
    embedder = load_embedder({"model_name": args.embedding_model, "device": "cpu"})

    print(f"🗃️  Loading vector store: {args.vector_store_type}")
    vector_store = load_vector_store({"type": args.vector_store_type}, embedder)

    # Load documents
    documents = []
    if args.doc_file:
        documents.extend(load_documents_from_file(args.doc_file))

    if args.doc_dir:
        for root, _, files in os.walk(args.doc_dir):
            for fname in files:
                if fname.lower().endswith((".txt", ".html", ".htm")):
                    file_path = os.path.join(root, fname)
                    documents.extend(load_documents_from_file(file_path))

    pipeline = build_pipeline(args.model_name, args.embedding_model, args.vector_store_type, documents)

    if documents:
        print(f"📚 Adding {len(documents)} documents to vector store...")
        vector_store.add_documents(documents)

    # Run pipeline
    pipeline = RAGPipeline(model=model, vector_store=vector_store)

    if args.query:
        print(f"❓ Running query: {args.query}")
        answer = pipeline.query(args.query)
        print(f"\n💡 Answer: {answer}")
    else:
        print("⚠️  No query provided. Use --query to ask a question.")


if __name__ == "__main__":
    main()
