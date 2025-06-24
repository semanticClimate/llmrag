import os
import pytest

from llmrag.embeddings import SentenceTransformersEmbedder
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.retrievers.chroma_store import ChromaVectorStore

TEST_HTML = """<html>
    <body>
        <h1>Climate Change</h1>
        <p>Global temperatures are rising due to greenhouse gas emissions.</p>
        <h2>Evidence</h2>
        <p>Glaciers are retreating and sea levels are rising.</p>
        <h2>Future Projections</h2>
        <p>Models suggest continued warming over the next century.</p>
    </body>
</html>"""

@pytest.fixture
def temp_html_file(tmp_path):
    html_path = tmp_path / "sample.html"
    html_path.write_text(TEST_HTML, encoding="utf-8")
    return str(html_path)


def test_ingest_html_file(temp_html_file):
    collection_name = "test_html_ingestion"

    # Run ingestion
    ingest_html_file(temp_html_file, collection_name=collection_name)

    # Check that documents exist in vector store
    embedder = SentenceTransformersEmbedder()
    store = ChromaVectorStore(embedder=embedder, collection_name=collection_name)
    results = store.similarity_search("What are future climate projections?", top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0
    # assert any("Models suggest" in r for r in results)
    assert any("Models suggest" in r.page_content for r in results)

    # Cleanup: optionally remove the collection (if your ChromaVectorStore supports it)
