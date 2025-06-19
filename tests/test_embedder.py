import unittest
from llmrag.embeddings import load_embedder

class TestEmbedder(unittest.TestCase):
    def test_embedding_shape(self):
        embedder = load_embedder({"model_name": "all-MiniLM-L6-v2", "device": "cpu"})
        embeddings = embedder.embed(["Test sentence", "Another one"])
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), len(embeddings[1]))

