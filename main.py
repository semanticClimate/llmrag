# import yaml
# import argparse
# import logging
# import sys
# import unittest
# import webbrowser
# import os
# import coverage
#
# from llmrag.models import load_model
# from llmrag.embeddings import load_embedder
# from llmrag.retrievers import load_vector_store
# from llmrag.pipelines import RAGPipeline
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# def run_tests():
#     cov = coverage.Coverage(source=["llmrag"])
#     cov.start()
#
#     logger.info("Running test suite...\n")
#     test_loader = unittest.TestLoader()
#     test_suite = test_loader.discover('llmrag/tests')
#     runner = unittest.TextTestRunner(verbosity=2)
#     result = runner.run(test_suite)
#
#     cov.stop()
#     cov.save()
#     cov.report()
#     cov.html_report(directory="htmlcov")
#
#     html_path = os.path.abspath("htmlcov/index.html")
#     logger.info(f"Opening coverage report: {html_path}")
#     webbrowser.open(f"file://{html_path}")
#
#     if not result.wasSuccessful():
#         sys.exit(1)
#
# def main():
#     import toml
#     import os
#
#     def get_version():
#         pyproject_path = os.path.join(os.path.dirname(__file__), "pyproject.toml")
#         data = toml.load(pyproject_path)
#         return data["project"]["version"]
#
#     print(f"Running LLMRAG version {get_version()}")
#
#     parser = argparse.ArgumentParser(description="Run RAG chatbot or tests")
#     parser.add_argument("--config", default="configs/default.yaml", help="Path to config YAML")
#     parser.add_argument("--test", action="store_true", help="Run tests and exit")
#     args = parser.parse_args()
#
#     if args.test:
#         run_tests()
#         return
#
#     config = yaml.safe_load(open(args.config))
#
#     logger.info("Loading model...")
#     model = load_model(config["llm"])
#
#     logger.info("Loading embedder...")
#     embedder = load_embedder(config["embedding"])
#
#     logger.info("Initializing vector store...")
#     vector_store = load_vector_store(config["vector_store"], embedder)
#
#     pipeline = RAGPipeline(model=model, vector_store=vector_store)
#
#     logger.info("RAG Chatbot System Ready. Type your question below (type 'exit' to quit):\n")
#     while True:
#         query = input("Enter Query (exit or quit to finish): ")
#         if query.lower() in ["exit", "quit"]:
#             break
#         response = pipeline.query(query)
#         print("Bot:", response)
#
# if __name__ == "__main__":
#     main()

import argparse
from pathlib import Path

from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
from llmrag.retrievers.chroma_store import ChromaVectorStore
from llmrag.models.transformers_model import TransformersModel
from llmrag.pipelines.rag_pipeline import RAGPipeline

import tomllib


def get_version():
    """Extracts version from pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]
    except Exception:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Run an LLM-RAG pipeline on an HTML file.")
    parser.add_argument("--html", required=True, help="Path to the input HTML file.")
    parser.add_argument("--query", required=True, help="User query to ask the system.")
    parser.add_argument("--collection", default="html_collection", help="Name of the vector store collection.")
    parser.add_argument("--version", action="store_true", help="Show version and exit.")
    args = parser.parse_args()

    if args.version:
        print(f"LLM-RAG Version: {get_version()}")
        return

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"[ERROR] HTML file not found: {args.html}")
        return

    # Step 1: Ingest
    print("[INFO] Ingesting HTML...")
    ingest_html_file(str(html_path), collection_name=args.collection)

    # Step 2: Initialize RAG components
    embedder = SentenceTransformersEmbedder()
    retriever = ChromaVectorStore(embedder=embedder, collection_name=args.collection)
    model = TransformersModel()  # Optionally choose your model here
    pipeline = RAGPipeline(vector_store=retriever, model=model)

    # Step 3: Run query
    print(f"[INFO] Asking: {args.query}")
    result = pipeline.run(args.query)

    # Step 4: Display result
    print("\n=== Answer ===")
    print(result["answer"])
    print("\n=== Context Snippets ===")
    for i, doc in enumerate(result["context"]):
        print(f"[{i+1}] {doc.page_content.strip()[:300]}...")

if __name__ == "__main__":
    main()
