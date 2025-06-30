#!/usr/bin/env python3
"""
Simple test script for the streamlined Chapter RAG system.
"""

import llmrag

def test_simple_usage():
    """Test the simple usage patterns for Jupyter notebooks."""
    
    print("🧪 Testing Simple Chapter RAG Usage")
    print("=" * 50)
    
    # Test 1: List chapters
    print("\n1. Listing available chapters:")
    chapters = llmrag.list_available_chapters()
    for chapter in chapters:
        print(f"   - {chapter}")
    
    # Test 2: Quick question
    print("\n2. Quick question test:")
    try:
        result = llmrag.ask_chapter(
            "What are the main climate scenarios?",
            "wg1/chapter04",
            "test_user1"
        )
        print(f"   ✅ Answer: {result['answer'][:100]}...")
        print(f"   ✅ Paragraph IDs: {result['paragraph_ids'][:3]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Load chapter and ask multiple questions
    print("\n3. Load chapter and ask multiple questions:")
    try:
        rag = llmrag.load_chapter("wg1/chapter04", "test_user2")
        
        questions = [
            "How do CMIP6 models differ from CMIP5?",
            "What is the projected temperature increase?"
        ]
        
        for question in questions:
            result = rag.ask(question, "wg1/chapter04", "test_user2")
            print(f"   ❓ {question}")
            print(f"   📝 {result['answer'][:80]}...")
            print()
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_simple_usage() 