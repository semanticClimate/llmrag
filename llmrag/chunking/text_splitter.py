from langchain.schema import Document

from langchain.schema import Document

def split_documents(text, chunk_size=100, overlap=20, metadata=None):
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        # Merge original metadata with chunk index
        chunk_metadata = dict(metadata or {})
        chunk_metadata["chunk_index"] = chunk_index
        chunks.append(Document(page_content=chunk_text, metadata=chunk_metadata))
        chunk_index += 1
        start = end - overlap  # slide window with overlap

    return chunks
