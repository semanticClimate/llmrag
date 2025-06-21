def split_documents(text, chunk_size=100, overlap=20):
    """
    Splits a large text into overlapping chunks.

    Args:
        text (str): The input text to split.
        chunk_size (int): Size of each chunk.
        overlap (int): Number of overlapping characters between chunks.

    Returns:
        list[str]: List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
