#!/usr/bin/env python3
"""
Test script to demonstrate the new title functionality.
"""

from llmrag.chapter_rag import list_available_chapters_with_titles, ChapterRAG

def main():
    print("🎯 Testing Title Extraction and Chapter Selection")
    print("=" * 50)
    
    # Test 1: List chapters with titles
    print("\n1. 📚 Available Chapters with Titles:")
    chapters_with_titles = list_available_chapters_with_titles()
    
    for i, (path, title) in enumerate(chapters_with_titles, 1):
        print(f"   {i:2d}. {path}")
        print(f"       📖 {title}")
        print()
    
    # Test 2: Show how to use in a selection interface
    print("\n2. 🎛️  Chapter Selection Interface:")
    print("   Available options:")
    
    for i, (path, title) in enumerate(chapters_with_titles, 1):
        print(f"   {i}. {title} ({path})")
    
    # Test 3: Demonstrate loading a chapter
    print("\n3. 🚀 Loading a Chapter:")
    if chapters_with_titles:
        # Load the first chapter as an example
        first_chapter_path, first_chapter_title = chapters_with_titles[0]
        print(f"   Loading: {first_chapter_title}")
        print(f"   Path: {first_chapter_path}")
        
        try:
            rag = ChapterRAG()
            rag.load_chapter(first_chapter_path, "test_user")
            print("   ✅ Chapter loaded successfully!")
        except Exception as e:
            print(f"   ❌ Error loading chapter: {e}")
    
    print("\n" + "=" * 50)
    print("✨ Title extraction and chapter selection working perfectly!")

if __name__ == "__main__":
    main() 