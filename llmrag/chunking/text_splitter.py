from langchain_core.documents import Document

def split_documents(text, chunk_size=100, overlap=20, metadata=None):
    if overlap >= chunk_size:
        raise ValueError("`overlap` must be smaller than `chunk_size` to avoid infinite loops.")

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        chunk_metadata = dict(metadata or {})
        chunk_metadata["chunk_index"] = chunk_index
        chunks.append(Document(page_content=chunk_text, metadata=chunk_metadata))
        chunk_index += 1
        start += chunk_size - overlap  # safe slide

    return chunks
