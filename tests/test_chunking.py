import unittest
from llmrag.chunking import split_documents

class TestChunking(unittest.TestCase):
    def test_split_documents(self):
        text = "abcdefghijklmnopqrstuvwxyz"
        chunks = split_documents(text, chunk_size=10, overlap=2)
        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1][:2], "ij")  # Overlap check