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

# --- main.py ---
import yaml
from llmrag.models import load_model
from llmrag.embeddings import load_embedder
from llmrag.retrievers import load_vector_store
from llmrag.pipelines import RAGPipeline


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

