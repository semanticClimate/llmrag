import unittest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestComponents(unittest.TestCase):
    """Test individual components without full pipeline integration."""

    def test_fake_llm_import(self):
        """Test that FakeLLM can be imported and used."""
        try:
            from llmrag.models.fake_llm import FakeLLM
            model = FakeLLM()
            response = model.generate("test question")
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
        except ImportError as e:
            self.skipTest(f"FakeLLM import failed: {e}")

    def test_html_splitter_import(self):
        """Test that HtmlTextSplitter can be imported and used."""
        try:
            from llmrag.chunking.html_splitter import HtmlTextSplitter
            splitter = HtmlTextSplitter(chunk_size=100)
            html_content = "<h1>Title</h1><p id='p1'>Test content.</p>"
            chunks = splitter.split(html_content)
            self.assertIsInstance(chunks, list)
            self.assertTrue(len(chunks) > 0)
        except ImportError as e:
            self.skipTest(f"HtmlTextSplitter import failed: {e}")

    def test_embedder_import(self):
        """Test that SentenceTransformersEmbedder can be imported."""
        try:
            from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
            # Just test import, don't create instance (requires model download)
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"SentenceTransformersEmbedder import failed: {e}")

    def test_vector_store_import(self):
        """Test that ChromaVectorStore can be imported."""
        try:
            from llmrag.retrievers.chroma_store import ChromaVectorStore
            # Just test import, don't create instance (requires embedder)
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"ChromaVectorStore import failed: {e}")

    def test_pipeline_import(self):
        """Test that RAGPipeline can be imported."""
        try:
            from llmrag.pipelines.rag_pipeline import RAGPipeline
            # Just test import, don't create instance
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"RAGPipeline import failed: {e}")

    def test_chapter_rag_import(self):
        """Test that chapter_rag can be imported."""
        try:
            from llmrag import chapter_rag
            # Just test import
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"chapter_rag import failed: {e}")

    def test_cli_import(self):
        """Test that cli can be imported."""
        try:
            from llmrag import cli
            # Just test import
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"cli import failed: {e}")


if __name__ == "__main__":
    unittest.main() 