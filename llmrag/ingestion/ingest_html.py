import os
from llmrag.chunking.html_splitter import HtmlTextSplitter
from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
from llmrag.retrievers.chroma_store import ChromaVectorStore

def ingest_html_file(file_path: str, collection_name: str = "html_docs", chunk_size: int = 500):
    """
    Ingests an HTML file into a Chroma vector store.

    Args:
        file_path (str): Path to the HTML file.
        collection_name (str): Name of the Chroma collection.
        chunk_size (int): Character size of each chunk.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"HTML file not found: {file_path}")

    print(f"[Ingest] Reading HTML file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Step 1: Chunk HTML into text segments
    print(f"[Ingest] Splitting HTML into chunks (size: {chunk_size} chars)...")
    splitter = HtmlTextSplitter(chunk_size=chunk_size)
    chunks = splitter.split(html_content)
    if not chunks:
        raise ValueError("No content extracted from the HTML file.")

    print(f"[Ingest] Extracted {len(chunks)} chunks from {file_path}")

    # Step 2: Embed chunks
    print(f"[Ingest] Generating embeddings for {len(chunks)} chunks...")
    embedder = SentenceTransformersEmbedder()
    embeddings = embedder.embed(chunks)

    # Step 3: Store in Chroma
    print(f"[Ingest] Storing {len(chunks)} chunks in Chroma collection '{collection_name}'...")
    store = ChromaVectorStore(collection_name=collection_name, embedder=embedder)
    store.add_documents(chunks)
    store.persist()

    print(f"[Ingest] Successfully ingested {len(chunks)} chunks into Chroma collection '{collection_name}'")
