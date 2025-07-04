import os
from llmrag.chunking.html_splitter import HtmlTextSplitter
from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
from llmrag.retrievers.chroma_store import ChromaVectorStore
import chromadb
from chromadb.config import Settings

def ingest_html_file(file_path: str, collection_name: str = "html_docs", chunk_size: int = 500, force_reingest: bool = False):
    """
    Ingests an HTML file into a Chroma vector store with caching support.

    Args:
        file_path (str): Path to the HTML file.
        collection_name (str): Name of the Chroma collection.
        chunk_size (int): Character size of each chunk.
        force_reingest (bool): Force re-ingestion even if collection exists.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"HTML file not found: {file_path}")

    # Check if collection already exists and has data
    if not force_reingest:
        try:
            client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            collection = client.get_collection(collection_name)
            count = collection.count()
            if count > 0:
                print(f"[Cache] Found existing collection '{collection_name}' with {count} documents. Skipping ingestion.")
                return
        except Exception:
            # Collection doesn't exist, proceed with ingestion
            pass

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

    # Step 2: Embed chunks with progress tracking
    print(f"[Ingest] Generating embeddings for {len(chunks)} chunks...")
    embedder = SentenceTransformersEmbedder()
    
    # Process embeddings in batches for better progress tracking
    batch_size = 50
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_embeddings = embedder.embed(batch)
        all_embeddings.extend(batch_embeddings)
        progress = min(100, int((i + len(batch)) / len(chunks) * 100))
        print(f"[Ingest] Embedding progress: {progress}% ({i + len(batch)}/{len(chunks)})")

    # Step 3: Store in Chroma
    print(f"[Ingest] Storing {len(chunks)} chunks in Chroma collection '{collection_name}'...")
    store = ChromaVectorStore(collection_name=collection_name, embedder=embedder)
    store.add_documents(chunks)
    store.persist()

    print(f"[Ingest] Successfully ingested {len(chunks)} chunks into Chroma collection '{collection_name}'")
