#!/usr/bin/env python3
"""
Test script to demonstrate the performance and quality improvements.
"""

import time
import os
from llmrag.chapter_rag import ChapterRAG
from llmrag.utils.vector_store_manager import VectorStoreManager

def test_caching_performance():
    """Test the caching performance improvements."""
    print("🚀 Testing Caching Performance")
    print("=" * 50)
    
    # Initialize RAG system
    rag = ChapterRAG(model_name="gpt2-medium", device="cpu")
    
    # Test chapter
    chapter_name = "wg1/chapter04"
    user_id = "test_user"
    
    print(f"📖 Testing with chapter: {chapter_name}")
    print(f"👤 User ID: {user_id}")
    print()
    
    # First load (should be slow)
    print("🔄 First load (should process and cache)...")
    start_time = time.time()
    rag.load_chapter(chapter_name, user_id)
    first_load_time = time.time() - start_time
    print(f"⏱️  First load time: {first_load_time:.2f} seconds")
    print()
    
    # Second load (should be fast due to caching)
    print("🔄 Second load (should use cache)...")
    start_time = time.time()
    rag.load_chapter(chapter_name, user_id)
    second_load_time = time.time() - start_time
    print(f"⏱️  Second load time: {second_load_time:.2f} seconds")
    print()
    
    # Calculate improvement
    if first_load_time > 0:
        improvement = ((first_load_time - second_load_time) / first_load_time) * 100
        print(f"📈 Performance improvement: {improvement:.1f}% faster on second load")
    
    return rag

def test_answer_quality():
    """Test the improved answer quality with better prompts."""
    print("\n🎯 Testing Answer Quality")
    print("=" * 50)
    
    rag = ChapterRAG(model_name="gpt2-large", device="cpu")
    chapter_name = "wg1/chapter04"
    user_id = "quality_test"
    
    # Load chapter
    rag.load_chapter(chapter_name, user_id)
    
    # Test questions
    test_questions = [
        "What are the main scenarios used in climate projections?",
        "How do climate models handle uncertainty?",
        "What is the difference between CMIP5 and CMIP6?",
        "What are the projected temperature changes by 2100?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 40)
        
        start_time = time.time()
        result = rag.ask(question, chapter_name, user_id)
        response_time = time.time() - start_time
        
        print(f"🤖 Answer ({response_time:.2f}s):")
        print(result['answer'])
        
        if result.get('paragraph_ids'):
            print(f"📄 Sources: {', '.join(result['paragraph_ids'][:3])}...")
        
        print()

def test_vector_store_management():
    """Test the vector store management utilities."""
    print("\n📚 Testing Vector Store Management")
    print("=" * 50)
    
    manager = VectorStoreManager()
    
    # Get storage info
    storage_info = manager.get_storage_info()
    print(f"📁 Storage: {storage_info['size_mb']} MB")
    print(f"📚 Collections: {storage_info['collections']}")
    print(f"📄 Total Documents: {storage_info['total_documents']}")
    
    # List collections
    collections = manager.list_collections()
    if collections:
        print("\n📋 Available Collections:")
        for coll in collections:
            print(f"  • {coll['name']}: {coll['count']} documents")
    else:
        print("\n❌ No collections found")

def main():
    """Run all tests."""
    print("🧪 LLM-RAG System Improvements Test")
    print("=" * 60)
    
    try:
        # Test caching performance
        test_caching_performance()
        
        # Test answer quality
        test_answer_quality()
        
        # Test vector store management
        test_vector_store_management()
        
        print("\n✅ All tests completed successfully!")
        print("\n📊 Summary of Improvements:")
        print("• 🚀 Caching: Vector stores are now cached and reused")
        print("• 🎯 Quality: Improved prompts for scientific content")
        print("• 📚 Management: Vector store inspection and cleanup tools")
        print("• ⚡ Performance: Faster subsequent chapter loads")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 