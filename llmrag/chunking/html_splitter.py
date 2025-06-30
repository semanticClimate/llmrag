"""
HTML Text Splitter for RAG Systems

STUDENT GUIDE:
This file shows how to process HTML documents for RAG (Retrieval-Augmented Generation).
RAG systems need to break large documents into smaller "chunks" that can be:
1. Stored in a database (vector store)
2. Searched when someone asks a question
3. Used to generate answers

Think of it like cutting a long book into index cards - each card has a piece of text
that can be found and used to answer questions.

Key Concepts:
- HTML: A markup language for web pages (like <h1>Title</h1>)
- Chunking: Breaking text into smaller pieces
- Metadata: Extra information about each chunk (like paragraph IDs for source tracking)
- Document: A standard format used by RAG systems to store text + metadata
"""

from typing import List  # Python type hints - helps catch errors early
from lxml import html    # Library for parsing HTML (like reading a web page)
from langchain.schema import Document  # Standard format for RAG documents


class HtmlTextSplitter:
    """
    A text splitter that processes HTML content and splits it into chunks based on semantic elements.
    
    STUDENT EXPLANATION:
    This class is like a smart document cutter. It takes HTML content (like a web page)
    and cuts it into smaller pieces while keeping related information together.
    
    Why do we need this?
    - Large documents are too big to process all at once
    - We want to keep related information together (like a heading with its paragraph)
    - We need to track where each piece came from (paragraph IDs for source tracking)
    
    This splitter extracts text from HTML headings (h1-h6) and paragraphs, then combines
    them into chunks of specified size while preserving semantic structure.
    
    Attributes:
        chunk_size (int): The maximum size (in characters) for each text chunk.
                          Defaults to 500 characters.
    """
    
    def __init__(self, chunk_size: int = 500):
        """
        Initialize the HTML text splitter.
        
        STUDENT NOTE:
        This is the constructor - it runs when we create a new HtmlTextSplitter object.
        It sets up the basic configuration (how big each chunk should be).
        
        Args:
            chunk_size (int): The maximum size in characters for each text chunk.
                             Defaults to 500.
        """
        self.chunk_size = chunk_size

    def split(self, html_content: str) -> List[Document]:
        """
        Split HTML content into chunks based on semantic elements.
        
        STUDENT EXPLANATION:
        This is the main method that does the actual work. Here's what it does step by step:
        
        1. Takes HTML content as input (like a web page)
        2. Finds all headings (h1-h6) and paragraphs (p) in the HTML
        3. Groups them together into chunks that fit within the size limit
        4. Keeps track of which paragraph IDs are in each chunk (for source tracking)
        5. Returns a list of Document objects (the standard RAG format)
        
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
        # Parse the HTML string into a tree structure we can navigate
        tree = html.fromstring(html_content)
        
        # Find all headings (h1-h6) and paragraphs (p) in the HTML
        # This uses XPath, which is like a query language for HTML
        elements = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p')

        # Initialize variables to build our chunks
        chunks = []  # Will hold all our final chunks
        current_chunk = ""  # The text we're building for the current chunk
        current_paragraph_ids = []  # IDs of paragraphs in current chunk
        current_element_types = []  # Types of elements (h1, p, etc.) in current chunk
        
        # Loop through each element (heading or paragraph) we found
        for element in elements:
            # Extract just the text content, removing extra whitespace
            text = element.text_content().strip()
            if not text:  # Skip empty elements
                continue

            # Extract element ID if present (for source tracking)
            element_id = element.get('id')
            element_type = element.tag  # What type of element (h1, p, etc.)
            
            # Check if adding this text would make the chunk too big
            if len(current_chunk) + len(text) + 1 <= self.chunk_size:
                # Add to current chunk
                current_chunk += (" " + text) if current_chunk else text
                if element_id:
                    current_paragraph_ids.append(element_id)
                current_element_types.append(element_type)
            else:
                # Current chunk is full, save it and start a new one
                metadata = {
                    "chunk_index": len(chunks),
                    "paragraph_ids": ",".join(current_paragraph_ids) if current_paragraph_ids else "",
                    "element_types": ",".join(current_element_types) if current_element_types else ""
                }
                chunks.append(Document(page_content=current_chunk, metadata=metadata))
                
                # Start new chunk with current element
                current_chunk = text
                current_paragraph_ids = [element_id] if element_id else []
                current_element_types = [element_type]

        # Don't forget the last chunk if it exists
        if current_chunk:
            metadata = {
                "chunk_index": len(chunks),
                "paragraph_ids": ",".join(current_paragraph_ids) if current_paragraph_ids else "",
                "element_types": ",".join(current_element_types) if current_element_types else ""
            }
            chunks.append(Document(page_content=current_chunk, metadata=metadata))

        return chunks

