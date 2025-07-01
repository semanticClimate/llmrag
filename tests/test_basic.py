import unittest

class TestBasic(unittest.TestCase):
    """Very basic tests that should always pass."""

    def test_basic_imports(self):
        """Test that basic imports work."""
        try:
            from llmrag.models.fake_llm import FakeLLM
            from llmrag.chunking.html_splitter import HtmlTextSplitter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Basic import failed: {e}")

    def test_fake_llm(self):
        """Test that fake LLM works."""
        from llmrag.models.fake_llm import FakeLLM
        model = FakeLLM()
        response = model.generate("What is AI?")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_html_splitter(self):
        """Test that HTML splitter works."""
        from llmrag.chunking.html_splitter import HtmlTextSplitter
        splitter = HtmlTextSplitter(chunk_size=100)
        html_content = "<h1>Title</h1><p id='p1'>This is a test paragraph.</p>"
        chunks = splitter.split(html_content)
        self.assertIsInstance(chunks, list)
        self.assertTrue(len(chunks) > 0)

    def test_simple_math(self):
        """Test that basic math works."""
        self.assertEqual(2 + 2, 4)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main() 