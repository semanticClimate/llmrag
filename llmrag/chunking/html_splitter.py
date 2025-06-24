from typing import List
from lxml import html
from langchain.schema import Document

class HtmlTextSplitter:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def split(self, html_content: str) -> List[str]:
        tree = html.fromstring(html_content)
        elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p')

        chunks = []
        current_chunk = ""
        for element in elements:
            text = element.text_content().strip()
            if not text:
                continue

            if len(current_chunk) + len(text) + 1 <= self.chunk_size:
                current_chunk += (" " + text) if current_chunk else text
            else:
                chunks.append(current_chunk)
                current_chunk = text

        if current_chunk:
            chunks.append(current_chunk)

        return [Document(page_content=chunk, metadata={"chunk_index": i}) for i, chunk in enumerate(chunks)]

