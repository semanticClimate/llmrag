"""
Simple Chapter RAG System for IPCC Reports
Designed for Jupyter/Colab tutorials with shared chapters and isolated user sandboxes.

STUDENT GUIDE:
This file shows how to build a complete RAG (Retrieval-Augmented Generation) system.
A RAG system combines:
1. Document storage and retrieval (like a smart library)
2. Language models (like ChatGPT) to generate answers
3. User management (so different people can use it safely)

Think of it like a research assistant that:
- Has access to a library of documents (IPCC reports)
- Can find relevant information when you ask questions
- Gives each researcher their own workspace
- Tracks where information comes from (paragraph IDs)

Key Concepts:
- RAG Pipeline: The complete system that processes questions and generates answers
- Vector Store: A database that stores documents as "vectors" (mathematical representations)
- Embeddings: Converting text into numbers that capture meaning
- User Isolation: Each user gets their own space to avoid conflicts
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path  # Modern way to work with file paths in Python
from lxml import html  # For parsing HTML to extract titles

# Import our custom components
from llmrag.ingestion.ingest_html import ingest_html_file  # Loads HTML files into the system
from llmrag.embeddings import SentenceTransformersEmbedder  # Converts text to vectors
from llmrag.retrievers import ChromaVectorStore  # Database for storing and searching documents
from llmrag.models.transformers_model import TransformersModel  # Language model for generating answers
from llmrag.pipelines.rag_pipeline import RAGPipeline  # Orchestrates the whole process


def normalize_chapter_name(chapter_path: str) -> Tuple[str, int, int]:
    """
    Normalize chapter name for bibliographic sorting.
    
    STUDENT EXPLANATION:
    This function converts chapter paths like "wg1/chapter04" or "wg2/Chapter15" 
    into a standardized format for proper sorting. It extracts:
    1. Working group number (1 or 2)
    2. Chapter number (with leading zeros)
    3. Original path for reference
    
    This ensures chapters are sorted correctly: wg1/chapter02, wg1/chapter04, wg1/chapter08, etc.
    
    Args:
        chapter_path: Chapter path like "wg1/chapter04" or "wg2/Chapter15"
        
    Returns:
        Tuple of (normalized_path, working_group, chapter_number)
    """
    # Extract working group and chapter number
    match = re.match(r'wg(\d+)/(?:chapter|Chapter)(\d+)', chapter_path, re.IGNORECASE)
    if match:
        working_group = int(match.group(1))
        chapter_num = int(match.group(2))
        
        # Create normalized path with leading zeros
        normalized = f"wg{working_group}/chapter{chapter_num:02d}"
        return normalized, working_group, chapter_num
    
    # Fallback for non-standard names
    return chapter_path, 0, 0


def resolve_corpus_path(base_path: str, corpus_url: str = None) -> str:
    """
    Resolve corpus path, supporting both local filesystem and URLs.
    
    STUDENT EXPLANATION:
    This function handles different corpus sources:
    1. Local filesystem paths (e.g., "/data/ipcc", "./corpus")
    2. Remote URLs (e.g., "https://example.com/ipcc")
    3. Relative paths (e.g., "tests/ipcc")
    
    Args:
        base_path: Base path to corpus (local or URL)
        corpus_url: Optional URL override for remote access
        
    Returns:
        Resolved corpus path
    """
    if corpus_url:
        # Use provided URL
        return corpus_url.rstrip('/')
    elif base_path.startswith(('http://', 'https://')):
        # Already a URL
        return base_path.rstrip('/')
    else:
        # Local filesystem path
        return str(Path(base_path).resolve())


def get_chapter_url(corpus_path: str, chapter_path: str) -> str:
    """
    Generate URL for a specific chapter using real IPCC URLs.
    
    Args:
        corpus_path: Base corpus path (URL or local path)
        chapter_path: Chapter path (e.g., "wg1/chapter02")
        
    Returns:
        Full URL to the chapter
    """
    if corpus_path.startswith(('http://', 'https://')):
        return f"{corpus_path}/{chapter_path}"
    else:
        # Generate real IPCC URL based on chapter path
        match = re.match(r'wg(\d+)/(?:chapter|Chapter)(\d+)', chapter_path, re.IGNORECASE)
        if match:
            wg_num = match.group(1)
            chapter_num = match.group(2)
            # IPCC URL format: https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-4/
            return f"https://www.ipcc.ch/report/ar6/wg{wg_num}/chapter/chapter-{chapter_num}/"
        else:
            # Fallback for non-standard chapter names
            return f"https://www.ipcc.ch/report/ar6/{chapter_path}/"


def sort_chapters_bibliographically(chapters_with_titles: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Sort chapters in bibliographic order (WG1 first, then WG2, with chapter numbers sorted).
    
    STUDENT EXPLANATION:
    This function sorts chapters in the proper order for IPCC reports:
    1. Working Group 1 (Physical Science Basis) chapters first
    2. Working Group 2 (Impacts, Adaptation, Vulnerability) chapters second
    3. Within each working group, chapters sorted by number
    
    Args:
        chapters_with_titles: List of (chapter_path, title) tuples
        
    Returns:
        Sorted list of (chapter_path, title) tuples
    """
    # Normalize and sort chapters
    normalized_chapters = []
    for chapter_path, title in chapters_with_titles:
        normalized_path, wg, chapter_num = normalize_chapter_name(chapter_path)
        normalized_chapters.append((normalized_path, title, wg, chapter_num, chapter_path))
    
    # Sort by working group, then by chapter number
    normalized_chapters.sort(key=lambda x: (x[2], x[3]))
    
    # Return original paths with titles, but in sorted order
    return [(original_path, title) for _, title, _, _, original_path in normalized_chapters]


class ChapterRAG:
    """
    Simple RAG system for IPCC chapters.
    Each user gets their own sandbox but shares the same chapter content.
    
    STUDENT EXPLANATION:
    This class is the main controller for our RAG system. It manages:
    - Loading chapters (documents) into the system
    - Creating separate workspaces for different users
    - Processing questions and generating answers
    - Keeping track of which chapters are loaded for which users
    
    Why "sandbox"? Think of it like giving each student their own desk in a library.
    They can all access the same books, but they have their own workspace and notes.
    """
    
    def __init__(self, base_path: str = "tests/ipcc", model_name: str = "gpt2-large", device: str = "auto", corpus_url: str = None):
        """
        Initialize the Chapter RAG system.
        
        STUDENT NOTE:
        This is the constructor - it sets up the basic configuration when we create
        a new ChapterRAG object. Think of it like setting up a new research workspace.
        
        We now use gpt2-large by default (774M parameters) which provides much better
        answer quality while still being manageable on CPU with sufficient RAM.
        
        Args:
            base_path: Path to IPCC chapters directory (local path or URL)
            model_name: HuggingFace model name (which AI model to use for generating answers)
            device: Device to run model on ("auto", "cpu", "mps", or "cuda")
            corpus_url: Optional URL override for remote corpus access
        """
        # Resolve corpus path (supports local filesystem and URLs)
        self.corpus_path = resolve_corpus_path(base_path, corpus_url)
        
        # For local paths, convert to Path object for easier file operations
        if not self.corpus_path.startswith(('http://', 'https://')):
            self.base_path = Path(self.corpus_path)
        else:
            self.base_path = None  # Remote corpus
            
        self.pipelines: Dict[str, RAGPipeline] = {}  # Store RAG pipelines for each user+chapter combination
        self.model_name = model_name
        
        # Auto-detect best device with robust fallback
        if device == "auto":
            self.device = self._get_safe_device()
        else:
            self.device = device
        
    def _get_safe_device(self) -> str:
        """
        Get a safe device setting, defaulting to CPU if GPU is not available or problematic.
        """
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                # Check macOS version for MPS compatibility
                import platform
                if platform.system() == "Darwin":
                    # Parse macOS version
                    version_str = platform.mac_ver()[0]
                    try:
                        major, minor = map(int, version_str.split('.')[:2])
                        if major >= 14 or (major == 13 and minor >= 0):
                            return "mps"
                    except:
                        pass
                return "cpu"
            else:
                return "cpu"
        except Exception as e:
            print(f"⚠️  Device detection failed: {e}, defaulting to CPU")
            return "cpu"
        
    def _extract_chapter_title(self, html_file_path: Path) -> str:
        """
        Extract the title from an HTML file.
        
        STUDENT EXPLANATION:
        This method reads an HTML file and tries to find its title. It looks for:
        1. <title> tags in the HTML head
        2. <h1> tags (main headings)
        3. Falls back to a default title if none found
        
        This is like reading the cover of a book to find its title.
        
        Args:
            html_file_path: Path to the HTML file
            
        Returns:
            The extracted title or a default title
        """
        try:
            # Read the HTML file
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse the HTML
            tree = html.fromstring(html_content)
            
            # Try to find title in <title> tag first
            title_elements = tree.xpath('//title')
            if title_elements:
                title = title_elements[0].text_content().strip()
                if title:
                    return title
            
            # Try to find title in <h1> tag
            h1_elements = tree.xpath('//h1')
            if h1_elements:
                title = h1_elements[0].text_content().strip()
                if title:
                    return title
            
            # Try to find title in <h2> tag
            h2_elements = tree.xpath('//h2')
            if h2_elements:
                title = h2_elements[0].text_content().strip()
                if title:
                    return title
            
            # Fallback: use filename as title
            return html_file_path.stem.replace('_', ' ').title()
            
        except Exception as e:
            # If anything goes wrong, use a default title
            return f"Chapter {html_file_path.stem}"
        
    def load_chapter(self, chapter_name: str, user_id: str = "default") -> None:
        """
        Load a specific chapter for a user.
        
        STUDENT EXPLANATION:
        This method loads an IPCC chapter into the RAG system. Here's what happens:
        
        1. **Find the chapter**: Looks for the HTML file in the tests/ipcc directory
        2. **Check if already loaded**: Avoids reloading the same chapter for the same user
        3. **Process the chapter**: Converts HTML to text chunks and stores them in a vector database
        4. **Set up the pipeline**: Creates all the components needed to answer questions
        
        The key innovation here is user isolation - each user gets their own copy of the chapter
        so they can't interfere with each other's work.
        
        Args:
            chapter_name: Chapter name (e.g., "wg1/chapter04")
            user_id: User identifier for isolation
        """
        # Create a unique key for this user+chapter combination
        key = f"{chapter_name}_{user_id}"
        
        # Check if this chapter is already loaded for this user
        if key in self.pipelines:
            print(f"📚 Chapter {chapter_name} already loaded for user {user_id}")
            return
        
        # Find the HTML file for this chapter
        html_file = None
        possible_paths = [
            self.base_path / chapter_name / "html_with_ids.html",
            self.base_path / chapter_name / "gatsby.html",
            self.base_path / chapter_name / "de_gatsby.html"
        ]
        
        for path in possible_paths:
            if path.exists():
                html_file = path
                break
        
        if html_file is None:
            # Try case-insensitive matching for chapter directories
            chapter_dir = self.base_path / chapter_name
            if not chapter_dir.exists():
                # Look for case variations
                parent_dir = chapter_dir.parent
                chapter_name_only = chapter_dir.name
                for subdir in parent_dir.iterdir():
                    if subdir.is_dir() and subdir.name.lower() == chapter_name_only.lower():
                        # Found a case variation, check for HTML files
                        for html_path in [subdir / "html_with_ids.html", subdir / "gatsby.html", subdir / "de_gatsby.html"]:
                            if html_path.exists():
                                html_file = html_path
                                break
                        if html_file:
                            break
        
        if html_file is None:
            raise FileNotFoundError(f"Could not find HTML file for chapter {chapter_name}")
        
        # Create user-specific collection name
        # This ensures each user gets their own isolated space
        collection_name = f"ipcc_{chapter_name.replace('/', '_')}_{user_id}"
        
        print(f"📖 Loading {chapter_name} for user {user_id}...")
        
        # Ingest the chapter with caching - this processes the HTML and stores it in the vector database
        # The improved ingestion will check if the collection already exists and skip if it does
        ingest_html_file(str(html_file), collection_name=collection_name, force_reingest=False)
        
        # Create pipeline with real model
        # This sets up all the components needed to answer questions
        embedder = SentenceTransformersEmbedder()  # Converts text to vectors
        retriever = ChromaVectorStore(embedder=embedder, collection_name=collection_name)  # Database for searching
        llm = TransformersModel(model_name=self.model_name, device=self.device)  # AI model for generating answers
        pipeline = RAGPipeline(vector_store=retriever, model=llm)  # Orchestrates everything
        
        # Store pipeline for this user+chapter combination
        self.pipelines[key] = pipeline
        
        print(f"✅ Chapter loaded successfully!")
    
    def ask(self, question: str, chapter_name: str, user_id: str = "default") -> Dict:
        """
        Ask a question about a specific chapter.
        
        STUDENT EXPLANATION:
        This is where the magic happens! Here's what happens when you ask a question:
        
        1. The system converts your question into a vector (mathematical representation)
        2. It searches the vector database for the most similar text chunks
        3. It takes those relevant chunks and sends them to the AI model
        4. The AI model generates an answer based on the provided context
        5. It returns the answer along with information about where it came from
        
        Think of it like:
        - You ask a librarian a question
        - They search the library catalog for relevant books
        - They read the relevant pages and summarize the information
        - They give you the answer and tell you which books they used
        
        Args:
            question: The question to ask
            chapter_name: Chapter name (e.g., "wg1/chapter04")
            user_id: User identifier
            
        Returns:
            Dictionary with answer, context, and paragraph IDs
        """
        # Create a unique key for this user+chapter combination
        key = f"{chapter_name}_{user_id}"
        
        # If this chapter isn't loaded for this user yet, load it automatically
        if key not in self.pipelines:
            self.load_chapter(chapter_name, user_id)
        
        # Get the pipeline for this user+chapter
        pipeline = self.pipelines[key]
        
        # Run the question through the RAG pipeline
        result = pipeline.run(question)
        
        # Add metadata to help track what happened
        result["chapter"] = chapter_name
        result["user_id"] = user_id
        
        return result
    
    def list_chapters(self) -> List[str]:
        """
        List available chapters.
        
        STUDENT NOTE:
        This method scans the base directory to find all available chapters.
        It's like looking at the library catalog to see what books are available.
        """
        chapters = []
        if self.base_path.exists():
            # Look for chapter directories (both "chapter" and "Chapter")
            for working_group in self.base_path.glob("wg*"):
                if working_group.is_dir():
                    for chapter_dir in working_group.iterdir():
                        if chapter_dir.is_dir() and chapter_dir.name.lower().startswith("chapter"):
                            chapters.append(str(chapter_dir.relative_to(self.base_path)))
        return sorted(chapters)
    
    def list_chapters_with_titles(self) -> List[Tuple[str, str]]:
        """
        List available chapters with their titles, sorted bibliographically.
        
        STUDENT EXPLANATION:
        This method returns both chapter paths and their human-readable titles,
        sorted in the proper order for IPCC reports:
        1. Working Group 1 (Physical Science Basis) chapters first
        2. Working Group 2 (Impacts, Adaptation, Vulnerability) chapters second
        3. Within each working group, chapters sorted by number
        
        It's like having a library catalog that shows both the call number and the book title,
        organized in the standard order.
        
        Returns:
            List of tuples: (chapter_path, chapter_title) sorted bibliographically
        """
        chapters_with_titles = []
        
        if self.base_path and self.base_path.exists():
            # Local filesystem corpus
            for working_group in self.base_path.glob("wg*"):
                if working_group.is_dir():
                    for chapter_dir in working_group.iterdir():
                        if chapter_dir.is_dir() and chapter_dir.name.lower().startswith("chapter"):
                            chapter_path = str(chapter_dir.relative_to(self.base_path))
                            
                            # Find HTML file to extract title
                            html_files = list(chapter_dir.glob("*.html"))
                            if html_files:
                                title = self._extract_chapter_title(html_files[0])
                            else:
                                title = f"Chapter {chapter_path.split('/')[-1]}"
                            
                            chapters_with_titles.append((chapter_path, title))
        elif self.corpus_path.startswith(('http://', 'https://')):
            # Remote corpus - for now, return basic structure
            # In a full implementation, this would fetch the directory listing from the URL
            print(f"🌐 Remote corpus detected: {self.corpus_path}")
            print("📝 Note: Remote corpus listing not yet implemented")
            # For now, return empty list - would need to implement HTTP directory listing
            pass
        
        # Sort chapters bibliographically
        return sort_chapters_bibliographically(chapters_with_titles)


# Convenience functions for Jupyter notebooks
# These are helper functions that make it easier to use the system in notebooks

def load_chapter(chapter_name: str, user_id: str = "default", model_name: str = "gpt2-large", device: str = "auto", base_path: str = "tests/ipcc", corpus_url: str = None) -> ChapterRAG:
    """
    Load a chapter and return a ChapterRAG instance.
    
    STUDENT NOTE:
    This is a convenience function that combines creating a ChapterRAG object
    and loading a chapter in one step. It's designed to be easy to use in
    Jupyter notebooks or interactive sessions.
    
    Args:
        chapter_name: Chapter name (e.g., "wg1/chapter02")
        user_id: User identifier
        model_name: HuggingFace model name
        device: Device to run model on
        base_path: Base path to corpus (local path or URL)
        corpus_url: Optional URL override for remote corpus access
        
    Returns:
        ChapterRAG instance ready for questions
    """
    rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device, corpus_url=corpus_url)
    rag.load_chapter(chapter_name, user_id)
    return rag


def ask_chapter(question: str, chapter_name: str, user_id: str = "default", model_name: str = "gpt2-large", device: str = "auto", base_path: str = "tests/ipcc", corpus_url: str = None) -> Dict:
    """
    Quick function to ask a question about a chapter.
    
    STUDENT NOTE:
    This is the simplest way to use the system - just one function call!
    It creates a ChapterRAG object, loads the chapter, asks the question,
    and returns the answer. Perfect for quick experiments.
    
    Args:
        question: The question to ask
        chapter_name: Chapter name (e.g., "wg1/chapter02")
        user_id: User identifier
        model_name: HuggingFace model name
        device: Device to run model on
        base_path: Base path to corpus (local path or URL)
        corpus_url: Optional URL override for remote corpus access
        
    Returns:
        Dictionary with answer and metadata
    """
    rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device, corpus_url=corpus_url)
    return rag.ask(question, chapter_name, user_id)


def list_available_chapters(base_path: str = "tests/ipcc", corpus_url: str = None) -> List[str]:
    """
    List all available IPCC chapters.
    
    STUDENT NOTE:
    This is a simple helper function that just lists what chapters are available.
    Useful for exploring what data you have access to.
    
    Args:
        base_path: Base path to corpus (local path or URL)
        corpus_url: Optional URL override for remote corpus access
        
    Returns:
        List of chapter paths
    """
    rag = ChapterRAG(base_path=base_path, corpus_url=corpus_url)
    return rag.list_chapters()


def list_available_chapters_with_titles(base_path: str = "tests/ipcc", corpus_url: str = None) -> List[Tuple[str, str]]:
    """
    List all available IPCC chapters with their titles.
    
    STUDENT NOTE:
    This function returns both chapter paths and human-readable titles.
    Useful for creating better user interfaces.
    
    Args:
        base_path: Base path to corpus (local path or URL)
        corpus_url: Optional URL override for remote corpus access
        
    Returns:
        List of (chapter_path, title) tuples
    """
    rag = ChapterRAG(base_path=base_path, corpus_url=corpus_url)
    return rag.list_chapters_with_titles() 