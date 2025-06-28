from typing import List
from lxml import html
from langchain.schema import Document

class HtmlTextSplitter:
    """
    A text splitter that processes HTML content and splits it into chunks based on semantic elements.
    
    This splitter extracts text from HTML headings (h1-h6) and paragraphs, then combines
    them into chunks of specified size while preserving semantic structure.
    
    Attributes:
        chunk_size (int): The maximum size (in characters) for each text chunk.
                          Defaults to 500 characters.
    """
    
    def __init__(self, chunk_size: int = 500):
        """
        Initialize the HTML text splitter.
        
        Args:
            chunk_size (int): The maximum size in characters for each text chunk.
                             Defaults to 500.
        """
        self.chunk_size = chunk_size

    def split(self, html_content: str) -> List[Document]:
        """
        Split HTML content into chunks based on semantic elements.
        
        This method parses the HTML content and extracts text from headings (h1-h6)
        and paragraphs. It then combines these elements into chunks that respect
        the specified chunk size while maintaining semantic coherence.
        
        Args:
            html_content (str): The HTML content to be split into chunks.
                               Should be valid HTML markup.
        
        Returns:
            List[Document]: A list of Document objects, where each Document contains:
                - page_content: The text chunk
                - metadata: A dictionary containing:
                    - chunk_index: The chunk's position in the sequence
                    - paragraph_ids: List of paragraph IDs from the HTML elements
                    - element_types: List of element types (h1, h2, p, etc.)
        
        Example:
            >>> splitter = HtmlTextSplitter(chunk_size=300)
            >>> html = '<h1>Title</h1><p id="p1">Some text here.</p><h2>Subtitle</h2>'
            >>> chunks = splitter.split(html)
            >>> len(chunks)
            1
            >>> chunks[0].page_content
            'Title Some text here. Subtitle'
            >>> chunks[0].metadata['paragraph_ids']
            ['p1']
        """
        tree = html.fromstring(html_content)
        elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p')

        chunks = []
        current_chunk = ""
        current_paragraph_ids = []
        current_element_types = []
        
        for element in elements:
            text = element.text_content().strip()
            if not text:
                continue

            # Extract element ID if present
            element_id = element.get('id')
            element_type = element.tag
            
            if len(current_chunk) + len(text) + 1 <= self.chunk_size:
                current_chunk += (" " + text) if current_chunk else text
                if element_id:
                    current_paragraph_ids.append(element_id)
                current_element_types.append(element_type)
            else:
                # Create document for current chunk
                metadata = {
                    "chunk_index": len(chunks),
                    "paragraph_ids": ",".join(current_paragraph_ids) if current_paragraph_ids else "",
                    "element_types": ",".join(current_element_types) if current_element_types else ""
                }
                chunks.append(Document(page_content=current_chunk, metadata=metadata))
                
                # Start new chunk
                current_chunk = text
                current_paragraph_ids = [element_id] if element_id else []
                current_element_types = [element_type]

        # Add the last chunk if it exists
        if current_chunk:
            metadata = {
                "chunk_index": len(chunks),
                "paragraph_ids": ",".join(current_paragraph_ids) if current_paragraph_ids else "",
                "element_types": ",".join(current_element_types) if current_element_types else ""
            }
            chunks.append(Document(page_content=current_chunk, metadata=metadata))

        return chunks

