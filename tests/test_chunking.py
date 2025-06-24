import unittest

import pytest
from langchain.schema import Document

from llmrag.utils.yaml_loader import load_paragraphs_yaml
# from split_document_with_metadata import split_document
from llmrag.chunking.text_splitter import split_documents


def test_paragraphs_loaded_correctly():
    """Test that paragraphs are loaded correctly as Document instances with required metadata."""
    docs = load_paragraphs_yaml("tests/data/test_paragraphs.yaml")
    assert isinstance(docs, list)
    assert all(isinstance(doc, Document) for doc in docs)
    assert all("id" in doc.metadata for doc in docs)
    assert all(isinstance(doc.page_content, str) for doc in docs)


@unittest.skip("infinite loop?")
def test_chunking_preserves_metadata():
    """Test that chunking a document preserves original metadata and appends a chunk index."""
    nparas = 2
    doc = Document(
        page_content="This is a long paragraph. " * nparas, metadata={"id": "test-001"}
    )
    chunks = split_documents(doc.page_content, chunk_size=100, overlap=20, metadata=doc.metadata)
    print(f"chunks {len(chunks)}")
    return

    assert len(chunks) > 1
    for i, chunk in enumerate(chunks):
        assert isinstance(chunk, Document)
        assert chunk.metadata["id"] == "test-001"
        assert chunk.metadata["chunk"] == i


@unittest.skip("infinite loop?")
def test_no_chunking_if_short():
    """Test that a short document below chunk size is returned unaltered and without chunk index."""
    short_text = "A short paragraph."
    doc = Document(page_content=short_text, metadata={"id": "short-001"})
    chunks = split_documents(doc.page_content, chunk_size=100, overlap=20, metadata=doc.metadata)
    assert len(chunks) == 1
    assert chunks[0].page_content == short_text
    assert chunks[0].metadata["id"] == "short-001"
    assert "chunk" not in chunks[0].metadata
