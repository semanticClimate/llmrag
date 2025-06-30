#!/usr/bin/env python3
"""
Chapter Manager for IPCC RAG System
Handles loading and managing different IPCC chapters for multi-user scenarios.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.embeddings import SentenceTransformersEmbedder
from llmrag.retrievers import ChromaVectorStore
from llmrag.models.fake_llm import FakeLLM
from llmrag.pipelines.rag_pipeline import RAGPipeline

class ChapterManager:
    """
    Manages multiple IPCC chapters for multi-user RAG scenarios.
    Each chapter gets its own vector store collection.
    """
    
    def __init__(self, base_data_path: str = "tests/ipcc"):
        """
        Initialize the chapter manager.
        
        Args:
            base_data_path: Path to the directory containing IPCC chapters
        """
        self.base_data_path = Path(base_data_path)
        self.loaded_chapters: Dict[str, RAGPipeline] = {}
        self.chapter_metadata: Dict[str, Dict] = {}
        
    def list_available_chapters(self) -> List[str]:
        """List all available IPCC chapters."""
        chapters = []
        if self.base_data_path.exists():
            for chapter_dir in self.base_data_path.glob("wg*/chapter*"):
                chapters.append(str(chapter_dir.relative_to(self.base_data_path)))
        return sorted(chapters)
    
    def load_chapter(self, chapter_path: str, user_id: Optional[str] = None) -> RAGPipeline:
        """
        Load a specific IPCC chapter and create a RAG pipeline for it.
        
        Args:
            chapter_path: Path to the chapter (e.g., "wg1/chapter04")
            user_id: Optional user identifier for collection naming
            
        Returns:
            RAGPipeline configured for this chapter
        """
        full_path = self.base_data_path / chapter_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Chapter not found: {chapter_path}")
        
        # Find HTML file in the chapter directory
        html_files = list(full_path.glob("*.html"))
        if not html_files:
            raise FileNotFoundError(f"No HTML files found in {chapter_path}")
        
        html_file = html_files[0]  # Use the first HTML file found
        
        # Create unique collection name
        collection_name = f"ipcc_{chapter_path.replace('/', '_')}"
        if user_id:
            collection_name += f"_{user_id}"
        
        print(f"Loading chapter: {chapter_path}")
        print(f"HTML file: {html_file}")
        print(f"Collection: {collection_name}")
        
        # Ingest the HTML file
        try:
            ingest_html_file(str(html_file), collection_name=collection_name)
            print(f"✅ Ingested {chapter_path}")
        except Exception as e:
            print(f"❌ Ingestion failed: {e}")
            raise
        
        # Set up the pipeline
        try:
            embedder = SentenceTransformersEmbedder()
            retriever = ChromaVectorStore(embedder=embedder, collection_name=collection_name)
            llm = FakeLLM()
            pipeline = RAGPipeline(vector_store=retriever, model=llm)
            
            # Store the pipeline
            self.loaded_chapters[chapter_path] = pipeline
            
            # Store metadata
            self.chapter_metadata[chapter_path] = {
                "html_file": str(html_file),
                "collection_name": collection_name,
                "user_id": user_id,
                "loaded_at": str(Path(html_file).stat().st_mtime)
            }
            
            print(f"✅ Pipeline ready for {chapter_path}")
            return pipeline
            
        except Exception as e:
            print(f"❌ Pipeline setup failed: {e}")
            raise
    
    def get_chapter_pipeline(self, chapter_path: str) -> Optional[RAGPipeline]:
        """Get an already loaded chapter pipeline."""
        return self.loaded_chapters.get(chapter_path)
    
    def query_chapter(self, chapter_path: str, query: str, user_id: Optional[str] = None) -> Dict:
        """
        Query a specific chapter. Loads it if not already loaded.
        
        Args:
            chapter_path: Path to the chapter
            query: The query to ask
            user_id: Optional user identifier
            
        Returns:
            Query result with answer, context, and paragraph IDs
        """
        # Load chapter if not already loaded
        if chapter_path not in self.loaded_chapters:
            self.load_chapter(chapter_path, user_id)
        
        pipeline = self.loaded_chapters[chapter_path]
        result = pipeline.run(query)
        
        # Add chapter context to result
        result["chapter_path"] = chapter_path
        result["user_id"] = user_id
        
        return result
    
    def list_loaded_chapters(self) -> List[str]:
        """List currently loaded chapters."""
        return list(self.loaded_chapters.keys())
    
    def get_chapter_info(self, chapter_path: str) -> Optional[Dict]:
        """Get metadata for a loaded chapter."""
        return self.chapter_metadata.get(chapter_path)

def demo_multi_chapter_usage():
    """Demonstrate multi-chapter, multi-user usage."""
    manager = ChapterManager()
    
    print("📚 Available chapters:")
    chapters = manager.list_available_chapters()
    for chapter in chapters:
        print(f"  - {chapter}")
    
    print("\n" + "="*60)
    print("🎯 MULTI-CHAPTER DEMO")
    print("="*60)
    
    # Simulate different users loading different chapters
    users = [
        ("Alice", "wg1/chapter04"),
        ("Bob", "wg1/chapter04"),  # Same chapter, different user
    ]
    
    queries = [
        "What are the main climate scenarios?",
        "How do CMIP6 models differ from CMIP5?",
        "What is the projected temperature increase by 2100?"
    ]
    
    for user_id, chapter_path in users:
        print(f"\n👤 User: {user_id}")
        print(f"📖 Chapter: {chapter_path}")
        print("-" * 40)
        
        for query in queries:
            try:
                result = manager.query_chapter(chapter_path, query, user_id)
                print(f"❓ Query: {query}")
                print(f"📝 Answer: {result['answer'][:100]}...")
                print(f"🏷️  Paragraph IDs: {result['paragraph_ids'][:3]}...")  # Show first 3
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                break

if __name__ == "__main__":
    demo_multi_chapter_usage() 