import unittest
import yaml
import os
from llmrag.embeddings import load_embedder
from llmrag.models import load_model
from llmrag.retrievers import load_vector_store
from llmrag.pipelines import RAGPipeline

class TestRAGPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_path = os.path.join(os.path.dirname(__file__), "data", "test_docs.yaml")
        with open(config_path, "r") as f:
            cls.test_config = yaml.safe_load(f)
        cls.model = load_model(cls.test_config["llm"])
        cls.embedder = load_embedder(cls.test_config["embedding"])
        cls.vector_store = load_vector_store(cls.test_config["vector_store"], cls.embedder)
        cls.vector_store.add_documents(cls.test_config["documents"])
        cls.pipeline = RAGPipeline(cls.model, cls.vector_store)

    def test_retrieve_and_generate(self):
        question = "What is AI?"
        response = self.pipeline.query(question)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_query(self):
        question = "What is photosynthesis?"
        answer = self.pipeline.query(question)
        self.assertIn("photosynthesis", answer.lower())


if __name__ == "__main__":
    unittest.main()
