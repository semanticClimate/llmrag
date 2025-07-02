#!/usr/bin/env python3
"""
Example usage for IPCC Chapter RAG System
Shows how different users can load different chapters and ask questions.
"""

from chapter_manager import ChapterManager

def example_user_workflow():
    """Example of how a user would work with a specific chapter."""
    
    # Initialize the chapter manager
    manager = ChapterManager()
    
    # List available chapters
    print("📚 Available IPCC Chapters:")
    chapters = manager.list_available_chapters()
    for chapter in chapters:
        print(f"  - {chapter}")
    
    # Example: User Alice loads Chapter 4
    print("\n" + "="*50)
    print("👤 Alice's Workflow")
    print("="*50)
    
    user_id = "alice"
    chapter_path = "wg1/chapter04"
    
    # Load the chapter (this creates a separate collection for Alice)
    try:
        pipeline = manager.load_chapter(chapter_path, user_id)
        print(f"✅ Alice loaded {chapter_path}")
    except Exception as e:
        print(f"❌ Failed to load chapter: {e}")
        return
    
    # Alice asks questions about her chapter
    alice_queries = [
        "What are the main climate scenarios used in projections?",
        "How do CMIP6 models differ from CMIP5?",
        "What is the projected temperature increase by 2100?"
    ]
    
    for query in alice_queries:
        print(f"\n❓ Alice asks: {query}")
        try:
            result = manager.query_chapter(chapter_path, query, user_id)
            print(f"📝 Answer: {result['answer']}")
            print(f"🏷️  Source paragraphs: {result['paragraph_ids'][:3]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Example: User Bob loads the same chapter (gets his own collection)
    print("\n" + "="*50)
    print("👤 Bob's Workflow")
    print("="*50)
    
    user_id = "bob"
    
    # Bob loads the same chapter but gets his own isolated context
    try:
        pipeline = manager.load_chapter(chapter_path, user_id)
        print(f"✅ Bob loaded {chapter_path} (separate from Alice)")
    except Exception as e:
        print(f"❌ Failed to load chapter: {e}")
        return
    
    # Bob asks different questions
    bob_queries = [
        "How do climate models handle uncertainty?",
        "What are the Shared Socioeconomic Pathways?",
        "How does Arctic sea ice change in projections?"
    ]
    
    for query in bob_queries:
        print(f"\n❓ Bob asks: {query}")
        try:
            result = manager.query_chapter(chapter_path, query, user_id)
            print(f"📝 Answer: {result['answer']}")
            print(f"🏷️  Source paragraphs: {result['paragraph_ids'][:3]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Show what's loaded
    print("\n" + "="*50)
    print("📊 System Status")
    print("="*50)
    print(f"Loaded chapters: {manager.list_loaded_chapters()}")
    
    for chapter in manager.list_loaded_chapters():
        info = manager.get_chapter_info(chapter)
        print(f"  - {chapter}: {info['collection_name']} (User: {info['user_id']})")

def simple_query_example():
    """Simple example for quick testing."""
    manager = ChapterManager()
    
    # Quick query to a specific chapter
    chapter = "wg1/chapter04"
    query = "What are the main climate scenarios?"
    user_id = "test_user"
    
    print(f"🔍 Querying {chapter}: {query}")
    
    try:
        result = manager.query_chapter(chapter, query, user_id)
        print(f"📝 Answer: {result['answer']}")
        print(f"🏷️  Paragraph IDs: {result['paragraph_ids']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Choose an example:")
    print("1. Full user workflow demo")
    print("2. Simple query example")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        example_user_workflow()
    elif choice == "2":
        simple_query_example()
    else:
        print("Running simple example...")
        simple_query_example() 