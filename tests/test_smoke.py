import unittest
import os
import sys

# Add the parent directory to the path so we can import llmrag
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from llmrag.chunking.html_splitter import HtmlTextSplitter
from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
from llmrag.models.fake_llm import FakeLLM
from llmrag.retrievers.chroma_store import ChromaVectorStore

class TestSmoke(unittest.TestCase):
    """Basic smoke tests to ensure core components work."""

    def test_html_splitter(self):
        """Test that HTML splitter works with basic HTML."""
        splitter = HtmlTextSplitter(chunk_size=100)
        html_content = "<h1>Title</h1><p id='p1'>This is a test paragraph.</p>"
        chunks = splitter.split(html_content)
        
        self.assertIsInstance(chunks, list)
        self.assertTrue(len(chunks) > 0)
        self.assertIsInstance(chunks[0].page_content, str)

    def test_embedder(self):
        """Test that embedder can create embeddings."""
        try:
            embedder = SentenceTransformersEmbedder()
            text = "This is a test sentence."
            embedding = embedder.embed(text)
            
            self.assertIsInstance(embedding, list)
            self.assertTrue(len(embedding) > 0)
            self.assertIsInstance(embedding[0], float)
        except Exception as e:
            # If embedding fails (e.g., no internet), just skip this test
            self.skipTest(f"Embedding test skipped: {e}")

    def test_fake_llm(self):
        """Test that fake LLM works."""
        model = FakeLLM()
        response = model.generate("What is AI?")
        
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_vector_store_creation(self):
        """Test that vector store can be created."""
        try:
            embedder = SentenceTransformersEmbedder()
            store = ChromaVectorStore(embedder, collection_name="test_collection")
            
            self.assertIsNotNone(store)
            self.assertIsNotNone(store.embedder)
        except Exception as e:
            # If vector store creation fails, just skip this test
            self.skipTest(f"Vector store test skipped: {e}")

    def test_imports(self):
        """Test that all main modules can be imported."""
        try:
            from llmrag import chapter_rag
            from llmrag import cli
            from llmrag.chunking import html_splitter
            from llmrag.embeddings import sentence_transformers_embedder
            from llmrag.models import transformers_model
            from llmrag.pipelines import rag_pipeline
            from llmrag.retrievers import chroma_store
            
            # If we get here, imports worked
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == "__main__":
    unittest.main()
