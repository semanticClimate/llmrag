"""
LLMRAG - Local RAG pipeline with chunking, embedding, and retrieval
"""

# Import the main chapter RAG functionality
from .chapter_rag import ChapterRAG, load_chapter, ask_chapter, list_available_chapters

# Import other key components
from .chunking.html_splitter import HtmlTextSplitter
from .embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
from .models.fake_llm import FakeLLM
from .pipelines.rag_pipeline import RAGPipeline

__all__ = [
    'ChapterRAG',
    'load_chapter', 
    'ask_chapter',
    'list_available_chapters',
    'HtmlTextSplitter',
    'SentenceTransformersEmbedder',
    'FakeLLM',
    'RAGPipeline'
]
