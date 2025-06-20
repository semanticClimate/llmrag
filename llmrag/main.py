import yaml
import argparse
import logging
import sys
import unittest
import webbrowser
import os
import coverage

from llmrag.models import load_model
from llmrag.embeddings import load_embedder
from llmrag.retrievers import load_vector_store
from llmrag.pipelines import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    cov = coverage.Coverage(source=["llmrag"])
    cov.start()

    logger.info("Running test suite...\n")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('llmrag/tests')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory="htmlcov")

    html_path = os.path.abspath("htmlcov/index.html")
    logger.info(f"Opening coverage report: {html_path}")
    webbrowser.open(f"file://{html_path}")

    if not result.wasSuccessful():
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run RAG chatbot or tests")
    parser.add_argument("--config", default="configs/default.yaml", help="Path to config YAML")
    parser.add_argument("--test", action="store_true", help="Run tests and exit")
    args = parser.parse_args()

    if args.test:
        run_tests()
        return

    config = yaml.safe_load(open(args.config))

    logger.info("Loading model...")
    model = load_model(config["llm"])

    logger.info("Loading embedder...")
    embedder = load_embedder(config["embedding"])

    logger.info("Initializing vector store...")
    retriever = load_vector_store(config["vector_store"], embedder)

    pipeline = RAGPipeline(model=model, retriever=retriever)

    logger.info("RAG Chatbot System Ready. Type your question below (type 'exit' to quit):\n")
    while True:
        query = input("Enter Query (exit or quit to finish): ")
        if query.lower() in ["exit", "quit"]:
            break
        response = pipeline.query(query)
        print("Bot:", response)

if __name__ == "__main__":
    main()
