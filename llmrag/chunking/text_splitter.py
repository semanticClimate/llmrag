"""Implements both a simple and recursive text splitter.
"""
from typing import List


class SimpleSplitter:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def split(self, text: str) -> List[str]:
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks


class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        separators = ["\n\n", "\n", ".", " ", ""]
        return self._recursive_split(text, separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        for sep in separators:
            if sep and sep in text:
                parts = text.split(sep)
                chunks = []
                chunk = ""
                for part in parts:
                    if len(chunk) + len(part) + len(sep) <= self.chunk_size:
                        chunk += part + sep
                    else:
                        chunks.append(chunk.strip())
                        chunk = part + sep
                if chunk:
                    chunks.append(chunk.strip())

                if self.chunk_overlap > 0:
                    overlapped_chunks = []
                    for i in range(0, len(chunks)):
                        start = max(i - 1, 0)
                        joined = " ".join(chunks[start:i + 1])
                        overlapped_chunks.append(joined)
                    return overlapped_chunks

                return chunks

        return [text]
