"""
Vector Store Manager for IPCC RAG System
Utilities for managing and inspecting cached vector stores.
"""

import os
import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional

class VectorStoreManager:
    """
    Manages and inspects existing ChromaDB vector stores.
    """
    
    def __init__(self, chroma_path: str = "./chroma_db"):
        self.chroma_path = Path(chroma_path)
        self.client = None
        
        if self.chroma_path.exists():
            self.client = chromadb.PersistentClient(
                path=str(self.chroma_path),
                settings=Settings(anonymized_telemetry=False)
            )
    
    def list_collections(self) -> List[Dict]:
        """
        List all available collections with their metadata.
        
        Returns:
            List of dictionaries with collection info
        """
        if not self.client:
            return []
        
        collections = []
        try:
            for collection in self.client.list_collections():
                count = collection.count()
                collections.append({
                    "name": collection.name,
                    "count": count,
                    "metadata": collection.metadata or {}
                })
        except Exception as e:
            print(f"Error listing collections: {e}")
        
        return collections
    
    def get_collection_info(self, collection_name: str) -> Optional[Dict]:
        """
        Get detailed information about a specific collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection details or None if not found
        """
        if not self.client:
            return None
        
        try:
            collection = self.client.get_collection(collection_name)
            count = collection.count()
            
            # Get a sample of documents to understand content
            sample_results = collection.get(limit=5)
            
            return {
                "name": collection_name,
                "count": count,
                "sample_documents": sample_results["documents"][:3] if sample_results["documents"] else [],
                "sample_metadata": sample_results["metadatas"][:3] if sample_results["metadatas"] else []
            }
        except Exception as e:
            print(f"Error getting collection info for {collection_name}: {e}")
            return None
    
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection.
        
        Args:
            collection_name: Name of the collection to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.delete_collection(collection_name)
            print(f"✅ Deleted collection: {collection_name}")
            return True
        except Exception as e:
            print(f"❌ Error deleting collection {collection_name}: {e}")
            return False
    
    def cleanup_old_collections(self, days_old: int = 7) -> List[str]:
        """
        Clean up old collections (placeholder for future implementation).
        
        Args:
            days_old: Age threshold for cleanup
            
        Returns:
            List of deleted collection names
        """
        # TODO: Implement cleanup based on collection metadata
        print(f"⚠️  Cleanup functionality not yet implemented")
        return []
    
    def get_storage_info(self) -> Dict:
        """
        Get information about vector store storage.
        
        Returns:
            Dictionary with storage statistics
        """
        if not self.chroma_path.exists():
            return {"exists": False, "size_mb": 0, "collections": 0}
        
        # Calculate directory size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.chroma_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        
        collections = self.list_collections()
        
        return {
            "exists": True,
            "size_mb": round(total_size / (1024 * 1024), 2),
            "collections": len(collections),
            "total_documents": sum(c["count"] for c in collections)
        }

def print_vector_store_status():
    """
    Utility function to print current vector store status.
    """
    manager = VectorStoreManager()
    
    print("🔍 Vector Store Status")
    print("=" * 50)
    
    storage_info = manager.get_storage_info()
    if not storage_info["exists"]:
        print("❌ No vector store found at ./chroma_db")
        return
    
    print(f"📁 Storage: {storage_info['size_mb']} MB")
    print(f"📚 Collections: {storage_info['collections']}")
    print(f"📄 Total Documents: {storage_info['total_documents']}")
    print()
    
    collections = manager.list_collections()
    if collections:
        print("📋 Available Collections:")
        for coll in collections:
            print(f"  • {coll['name']}: {coll['count']} documents")
    else:
        print("❌ No collections found")

if __name__ == "__main__":
    print_vector_store_status() 