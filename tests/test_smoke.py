import os
import pytest

from llmrag.embeddings import SentenceTransformersEmbedder
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.models.fake_llm import FakeLLM
from llmrag.pipelines.rag_pipeline import RAGPipeline
from llmrag.retrievers import ChromaVectorStore

SAMPLE_HTML = """<html>
    <body>
        <h1>Intro to LLMs</h1>
        <p>Large language models are used in AI to generate and understand text.</p>
        <h2>Applications</h2>
        <p>They are used in chatbots, translation, and summarization tools.</p>
    </body>
</html>
"""

@pytest.fixture
def html_file(tmp_path):
    html_path = tmp_path / "llm_test.html"
    html_path.write_text(SAMPLE_HTML, encoding="utf-8")
    return str(html_path)

def test_end_to_end_smoke(html_file):
    collection_name = "smoke_test_collection"

    # Step 1: Ingest
    ingest_html_file(html_file, collection_name=collection_name)

    # Step 2: Retrieve & Generate
    embedder = SentenceTransformersEmbedder()
    retriever = ChromaVectorStore(embedder=embedder, collection_name=collection_name)
    llm = FakeLLM()  # or whatever real/placeholder LLM you are testing with
    pipeline = RAGPipeline(vector_store=retriever, model=llm)
    # pipeline = RAGPipeline(collection_name=collection_name)
    result = pipeline.run("What are large language models used for?")

    # Step 3: Assert basic output
    assert "answer" in result
    assert "context" in result
    assert isinstance(result["answer"], str)
    assert isinstance(result["context"], list)
    assert len(result["context"]) > 0
