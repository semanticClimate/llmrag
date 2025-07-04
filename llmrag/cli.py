#!/usr/bin/env python3
"""
Command Line Interface for LLMRAG - IPCC Chapter RAG System

STUDENT GUIDE:
This file shows how to create a professional command-line interface (CLI) for your Python application.
A CLI allows users to interact with your program from the terminal/command prompt.

Key Concepts:
- argparse: Python's built-in library for parsing command-line arguments
- Subcommands: Different actions (like 'list-chapters', 'ask', etc.)
- Help text: Documentation that appears when users type --help
- Error handling: Graceful ways to handle mistakes and problems

Think of it like creating a menu system for a restaurant:
- Main menu (program name)
- Different categories (subcommands)
- Specific dishes (arguments)
- Descriptions (help text)

This CLI provides multiple functions:
1. list-chapters: See what documents are available
2. load-chapter: Load a document for a specific user
3. ask: Ask a question about a loaded document
4. interactive: Have a conversation with the system
5. vector-store: Manage vector store collections
6. test: Run performance and quality tests
7. benchmark: Performance benchmarking
"""

import argparse  # Python's built-in argument parsing library
import sys       # System-specific parameters and functions
import json      # For working with JSON data
import time      # For timing operations
from pathlib import Path  # Modern way to work with file paths
from typing import Optional

# Import our main RAG system
from llmrag.chapter_rag import ChapterRAG, list_available_chapters, list_available_chapters_with_titles
from llmrag.utils.vector_store_manager import VectorStoreManager


def setup_parser() -> argparse.ArgumentParser:
    """
    Set up the argument parser with all commands.
    
    STUDENT EXPLANATION:
    This function creates the "menu system" for our CLI. It defines:
    - What commands are available
    - What arguments each command needs
    - Help text for each option
    - Examples of how to use the commands
    
    Think of it like designing a restaurant menu with categories and descriptions.
    """
    # Create the main parser (like the restaurant name and description)
    parser = argparse.ArgumentParser(
        description="LLMRAG - IPCC Chapter RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Preserves formatting in help text
        epilog="""
Examples:
  # List available chapters with titles
  python -m llmrag.cli list-chapters
  
  # Load a chapter for a user
  python -m llmrag.cli load-chapter wg1/chapter04 --user-id alice
  
  # Ask a question about a chapter
  python -m llmrag.cli ask "What are the main findings about temperature trends?" --chapter wg1/chapter04 --user-id alice
  
  # Interactive mode
  python -m llmrag.cli interactive --chapter wg1/chapter04 --user-id alice
  
  # Vector store management
  python -m llmrag.cli vector-store status
  python -m llmrag.cli vector-store list
  python -m llmrag.cli vector-store cleanup
  
  # Performance testing
  python -m llmrag.cli test performance --chapter wg1/chapter04
  python -m llmrag.cli test quality --chapter wg1/chapter04
  
  # Benchmarking
  python -m llmrag.cli benchmark --chapters wg1/chapter04,wg1/chapter02
        """
    )
    
    # Create subparsers for different commands (like menu categories)
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command 1: List chapters
    list_parser = subparsers.add_parser('list-chapters', help='List available IPCC chapters with titles')
    list_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    list_parser.add_argument('--format', choices=['simple', 'detailed'], default='detailed', 
                           help='Output format (simple: just paths, detailed: paths with titles)')
    
    # Command 2: Load chapter
    load_parser = subparsers.add_parser('load-chapter', help='Load a chapter for a user')
    load_parser.add_argument('chapter', help='Chapter name (e.g., wg1/chapter04)')
    load_parser.add_argument('--user-id', default='default', help='User identifier')
    load_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    load_parser.add_argument('--model-name', default='gpt2-large', 
                           help='HuggingFace model name (default: gpt2-large)')
    load_parser.add_argument('--device', default='auto', 
                           help='Device to run model on (auto, cpu, mps, cuda) (default: auto)')
    load_parser.add_argument('--force', action='store_true', help='Force re-ingestion even if cached')
    
    # Command 3: Ask questions
    ask_parser = subparsers.add_parser('ask', help='Ask a question about a chapter')
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.add_argument('--chapter', required=True, help='Chapter name (e.g., wg1/chapter04)')
    ask_parser.add_argument('--user-id', default='default', help='User identifier')
    ask_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    ask_parser.add_argument('--model-name', default='gpt2-large', 
                           help='HuggingFace model name (default: gpt2-large)')
    ask_parser.add_argument('--device', default='auto', 
                           help='Device to run model on (auto, cpu, mps, cuda) (default: auto)')
    ask_parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    ask_parser.add_argument('--show-context', action='store_true', help='Show retrieved context')
    ask_parser.add_argument('--show-sources', action='store_true', help='Show source paragraph IDs')
    
    # Command 4: Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    interactive_parser.add_argument('--chapter', required=True, help='Chapter name (e.g., wg1/chapter04)')
    interactive_parser.add_argument('--user-id', default='default', help='User identifier')
    interactive_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    interactive_parser.add_argument('--model-name', default='gpt2-large',
                                   choices=['gpt2', 'gpt2-medium', 'gpt2-large', 'distilgpt2', 'microsoft/DialoGPT-medium'],
                                   help='HuggingFace model name (gpt2-large recommended for better quality)')
    interactive_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to run model on')
    
    # Command 5: Vector store management
    vector_parser = subparsers.add_parser('vector-store', help='Manage vector store collections')
    vector_subparsers = vector_parser.add_subparsers(dest='vector_command', help='Vector store commands')
    
    # Vector store status
    status_parser = vector_subparsers.add_parser('status', help='Show vector store status')
    
    # Vector store list
    list_parser = vector_subparsers.add_parser('list', help='List all collections')
    list_parser.add_argument('--detailed', action='store_true', help='Show detailed collection info')
    
    # Vector store cleanup
    cleanup_parser = vector_subparsers.add_parser('cleanup', help='Clean up old collections')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without doing it')
    cleanup_parser.add_argument('--older-than', type=int, default=7, help='Delete collections older than N days')
    
    # Vector store delete
    delete_parser = vector_subparsers.add_parser('delete', help='Delete a specific collection')
    delete_parser.add_argument('collection', help='Collection name to delete')
    
    # Command 6: Testing
    test_parser = subparsers.add_parser('test', help='Run tests and benchmarks')
    test_subparsers = test_parser.add_subparsers(dest='test_command', help='Test commands')
    
    # Performance test
    perf_parser = test_subparsers.add_parser('performance', help='Test caching performance')
    perf_parser.add_argument('--chapter', default='wg1/chapter04', help='Chapter to test')
    perf_parser.add_argument('--user-id', default='test_user', help='User ID for testing')
    perf_parser.add_argument('--model-name', default='gpt2-medium', help='Model to use for testing')
    
    # Quality test
    quality_parser = test_subparsers.add_parser('quality', help='Test answer quality')
    quality_parser.add_argument('--chapter', default='wg1/chapter04', help='Chapter to test')
    quality_parser.add_argument('--user-id', default='quality_test', help='User ID for testing')
    quality_parser.add_argument('--model-name', default='gpt2-large', help='Model to use for testing')
    
    # Command 7: Benchmarking
    benchmark_parser = subparsers.add_parser('benchmark', help='Run comprehensive benchmarks')
    benchmark_parser.add_argument('--chapters', help='Comma-separated list of chapters to benchmark')
    benchmark_parser.add_argument('--model-name', default='gpt2-medium', help='Model to use for benchmarking')
    benchmark_parser.add_argument('--output', help='Output file for benchmark results (JSON)')
    
    return parser


def list_chapters(base_path: str, format_type: str = 'detailed') -> None:
    """
    List available chapters with titles.
    
    STUDENT EXPLANATION:
    This function shows users what chapters (documents) are available in the system.
    It's like showing someone the library catalog so they can see what books are available.
    
    Now it also shows the actual titles of the chapters, making it much easier to
    understand what each chapter is about.
    
    Error handling: If something goes wrong, we print an error message and exit gracefully.
    """
    try:
        if format_type == 'detailed':
            # Get chapters with titles
            chapters_with_titles = list_available_chapters_with_titles()
            if chapters_with_titles:
                print("📚 Available IPCC Chapters:")
                print()
                for i, (chapter_path, title) in enumerate(chapters_with_titles, 1):
                    print(f"  {i:2d}. {chapter_path}")
                    print(f"      📖 {title}")
                    print()
            else:
                print("❌ No chapters found. Make sure you have IPCC chapters in the tests/ipcc directory.")
        else:
            # Simple format (just paths)
            chapters = list_available_chapters()
            if chapters:
                print("📚 Available IPCC Chapters:")
                for chapter in chapters:
                    print(f"  • {chapter}")
            else:
                print("❌ No chapters found. Make sure you have IPCC chapters in the tests/ipcc directory.")
    except Exception as e:
        print(f"❌ Error listing chapters: {e}")
        sys.exit(1)  # Exit with error code 1 (indicating failure)


def load_chapter_command(chapter: str, user_id: str, base_path: str, model_name: str, device: str, force: bool = False) -> None:
    """
    Load a chapter for a user.
    
    STUDENT EXPLANATION:
    This function loads a specific chapter for a specific user. It's like:
    - Taking a book from the library shelf
    - Setting up a reading desk for a specific person
    - Preparing the book so it can be searched and used
    
    The loading process involves:
    1. Processing the HTML file into chunks
    2. Converting chunks to vectors (embeddings)
    3. Storing them in a database
    4. Setting up the AI model for answering questions
    """
    try:
        print(f"📖 Loading chapter '{chapter}' for user '{user_id}'...")
        start_time = time.time()
        
        # Create a RAG system and load the chapter
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        rag.load_chapter(chapter, user_id)
        
        load_time = time.time() - start_time
        print(f"✅ Chapter '{chapter}' loaded successfully for user '{user_id}' in {load_time:.2f} seconds")
    except Exception as e:
        print(f"❌ Error loading chapter: {e}")
        sys.exit(1)


def ask_command(question: str, chapter: str, user_id: str, base_path: str, model_name: str, device: str, 
                output_format: str, show_context: bool = False, show_sources: bool = False) -> None:
    """
    Ask a question about a chapter.
    
    STUDENT EXPLANATION:
    This function processes a question and generates an answer. It's like:
    - You ask a librarian a question
    - They search through the books for relevant information
    - They read the relevant passages and summarize the answer
    - They tell you the answer and which books they used
    
    The process involves:
    1. Converting the question to a vector
    2. Searching the vector database for similar text
    3. Sending relevant text to the AI model
    4. Generating an answer based on the context
    5. Returning the answer with source information
    """
    try:
        print(f"🤖 Processing question: {question}")
        start_time = time.time()
        
        # Create RAG system and ask the question
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        result = rag.ask(question, chapter, user_id)
        
        response_time = time.time() - start_time
        
        if output_format == 'json':
            # JSON output for programmatic use
            output_data = {
                "question": question,
                "chapter": chapter,
                "user_id": user_id,
                "answer": result['answer'],
                "response_time": response_time,
                "paragraph_ids": result.get('paragraph_ids', []),
                "context_count": len(result.get('context', []))
            }
            print(json.dumps(output_data, indent=2))
        else:
            # Human-readable output
            print(f"\n📝 Answer ({response_time:.2f}s):")
            print("=" * 60)
            print(result['answer'])
            print("=" * 60)
            
            if show_sources and result.get('paragraph_ids'):
                print(f"\n📄 Sources: {', '.join(result['paragraph_ids'][:5])}")
                if len(result['paragraph_ids']) > 5:
                    print(f"   ... and {len(result['paragraph_ids']) - 5} more")
            
            if show_context and result.get('context'):
                print(f"\n🔍 Retrieved Context ({len(result['context'])} chunks):")
                for i, doc in enumerate(result['context'][:3], 1):
                    print(f"\n[{i}] {doc.page_content[:200]}...")
                if len(result['context']) > 3:
                    print(f"\n... and {len(result['context']) - 3} more chunks")
        
    except Exception as e:
        print(f"❌ Error asking question: {e}")
        sys.exit(1)


def vector_store_command(command: str, **kwargs) -> None:
    """Handle vector store management commands."""
    manager = VectorStoreManager()
    
    if command == 'status':
        print("🔍 Vector Store Status")
        print("=" * 50)
        
        storage_info = manager.get_storage_info()
        if not storage_info["exists"]:
            print("❌ No vector store found at ./chroma_db")
            return
        
        print(f"📁 Storage: {storage_info['size_mb']} MB")
        print(f"📚 Collections: {storage_info['collections']}")
        print(f"📄 Total Documents: {storage_info['total_documents']}")
        
    elif command == 'list':
        collections = manager.list_collections()
        if collections:
            print("📋 Available Collections:")
            for coll in collections:
                print(f"  • {coll['name']}: {coll['count']} documents")
                
                if kwargs.get('detailed'):
                    info = manager.get_collection_info(coll['name'])
                    if info and info.get('sample_documents'):
                        print(f"    Sample: {info['sample_documents'][0][:100]}...")
        else:
            print("❌ No collections found")
            
    elif command == 'cleanup':
        collections = manager.list_collections()
        if not collections:
            print("❌ No collections to clean up")
            return
            
        print(f"🧹 Cleanup Analysis:")
        print(f"Found {len(collections)} collections")
        
        if kwargs.get('dry_run'):
            print("🔍 Dry run - no collections will be deleted")
            for coll in collections:
                print(f"  Would delete: {coll['name']} ({coll['count']} documents)")
        else:
            deleted_count = 0
            for coll in collections:
                if manager.delete_collection(coll['name']):
                    deleted_count += 1
            print(f"✅ Deleted {deleted_count} collections")
            
    elif command == 'delete':
        collection_name = kwargs.get('collection')
        if manager.delete_collection(collection_name):
            print(f"✅ Deleted collection: {collection_name}")
        else:
            print(f"❌ Failed to delete collection: {collection_name}")


def test_performance(chapter: str, user_id: str, model_name: str) -> None:
    """Test caching performance."""
    print("🚀 Testing Caching Performance")
    print("=" * 50)
    
    try:
        rag = ChapterRAG(model_name=model_name, device="cpu")
        
        print(f"📖 Testing with chapter: {chapter}")
        print(f"👤 User ID: {user_id}")
        print()
        
        # First load (should be slow)
        print("🔄 First load (should process and cache)...")
        start_time = time.time()
        rag.load_chapter(chapter, user_id)
        first_load_time = time.time() - start_time
        print(f"⏱️  First load time: {first_load_time:.2f} seconds")
        print()
        
        # Second load (should be fast due to caching)
        print("🔄 Second load (should use cache)...")
        start_time = time.time()
        rag.load_chapter(chapter, user_id)
        second_load_time = time.time() - start_time
        print(f"⏱️  Second load time: {second_load_time:.2f} seconds")
        print()
        
        # Calculate improvement
        if first_load_time > 0:
            improvement = ((first_load_time - second_load_time) / first_load_time) * 100
            print(f"📈 Performance improvement: {improvement:.1f}% faster on second load")
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")


def test_quality(chapter: str, user_id: str, model_name: str) -> None:
    """Test answer quality."""
    print("🎯 Testing Answer Quality")
    print("=" * 50)
    
    try:
        rag = ChapterRAG(model_name=model_name, device="cpu")
        rag.load_chapter(chapter, user_id)
        
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
            result = rag.ask(question, chapter, user_id)
            response_time = time.time() - start_time
            
            print(f"🤖 Answer ({response_time:.2f}s):")
            print(result['answer'][:300] + "..." if len(result['answer']) > 300 else result['answer'])
            
            if result.get('paragraph_ids'):
                print(f"📄 Sources: {', '.join(result['paragraph_ids'][:3])}...")
            
    except Exception as e:
        print(f"❌ Quality test failed: {e}")


def benchmark_chapters(chapters: str, model_name: str, output_file: str = None) -> None:
    """Run comprehensive benchmarks."""
    print("🏁 Running Chapter Benchmarks")
    print("=" * 50)
    
    chapter_list = [c.strip() for c in chapters.split(',')]
    results = []
    
    for chapter in chapter_list:
        print(f"\n📊 Benchmarking {chapter}...")
        
        try:
            rag = ChapterRAG(model_name=model_name, device="cpu")
            
            # Load time
            start_time = time.time()
            rag.load_chapter(chapter, "benchmark_user")
            load_time = time.time() - start_time
            
            # Query time
            test_question = "What are the main findings of this chapter?"
            start_time = time.time()
            result = rag.ask(test_question, chapter, "benchmark_user")
            query_time = time.time() - start_time
            
            chapter_result = {
                "chapter": chapter,
                "load_time": load_time,
                "query_time": query_time,
                "answer_length": len(result['answer']),
                "context_chunks": len(result.get('context', [])),
                "sources": len(result.get('paragraph_ids', []))
            }
            
            results.append(chapter_result)
            
            print(f"  ⏱️  Load time: {load_time:.2f}s")
            print(f"  ⚡ Query time: {query_time:.2f}s")
            print(f"  📝 Answer length: {len(result['answer'])} chars")
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results.append({
                "chapter": chapter,
                "error": str(e)
            })
    
    # Summary
    print(f"\n📈 Benchmark Summary:")
    print(f"Chapters tested: {len(chapter_list)}")
    successful = [r for r in results if 'error' not in r]
    if successful:
        avg_load = sum(r['load_time'] for r in successful) / len(successful)
        avg_query = sum(r['query_time'] for r in successful) / len(successful)
        print(f"Average load time: {avg_load:.2f}s")
        print(f"Average query time: {avg_query:.2f}s")
    
    # Save results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Results saved to {output_file}")


def interactive_mode(chapter: str, user_id: str, base_path: str, model_name: str, device: str) -> None:
    """
    Start interactive mode for conversation with the RAG system.
    
    STUDENT EXPLANATION:
    This function creates an interactive chat session. It's like:
    - Having a conversation with a knowledgeable librarian
    - You can ask multiple questions in a row
    - The system remembers the context of your conversation
    - You can explore different aspects of the document
    
    This is great for:
    - Exploring a document in depth
    - Testing different types of questions
    - Getting a feel for how the system works
    - Debugging and development
    """
    try:
        print(f"🤖 Starting interactive mode for chapter '{chapter}'")
        print(f"👤 User: {user_id}")
        print(f"🤖 Model: {model_name}")
        print(f"💻 Device: {device}")
        print()
        print("💡 Type 'quit', 'exit', or 'q' to end the session")
        print("💡 Type 'help' for available commands")
        print("💡 Type 'status' to see current session info")
        print("=" * 60)
        
        # Create RAG system and load chapter
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        rag.load_chapter(chapter, user_id)
        
        # Track conversation
        conversation_count = 0
        total_time = 0
        
        while True:
            try:
                # Get user input
                user_input = input("\n❓ You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"\n👋 Goodbye! Processed {conversation_count} questions in {total_time:.2f} seconds")
                    break
                elif user_input.lower() == 'help':
                    print("\n📚 Available Commands:")
                    print("  help     - Show this help message")
                    print("  status   - Show session statistics")
                    print("  quit/q   - Exit interactive mode")
                    print("  <question> - Ask a question about the chapter")
                    continue
                elif user_input.lower() == 'status':
                    print(f"\n📊 Session Status:")
                    print(f"  Chapter: {chapter}")
                    print(f"  User: {user_id}")
                    print(f"  Questions asked: {conversation_count}")
                    print(f"  Total time: {total_time:.2f} seconds")
                    if conversation_count > 0:
                        print(f"  Average time per question: {total_time/conversation_count:.2f} seconds")
                    continue
                elif not user_input:
                    continue
                
                # Process the question
                conversation_count += 1
                print(f"\n🤖 Processing question {conversation_count}...")
                
                start_time = time.time()
                result = rag.ask(user_input, chapter, user_id)
                response_time = time.time() - start_time
                total_time += response_time
                
                # Display the answer
                print(f"\n📝 Answer ({response_time:.2f}s):")
                print("-" * 40)
                print(result['answer'])
                print("-" * 40)
                
                # Show sources if available
                if result.get('paragraph_ids'):
                    print(f"📄 Sources: {', '.join(result['paragraph_ids'][:3])}")
                    if len(result['paragraph_ids']) > 3:
                        print(f"   ... and {len(result['paragraph_ids']) - 3} more")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Interrupted! Processed {conversation_count} questions in {total_time:.2f} seconds")
                break
            except Exception as e:
                print(f"❌ Error processing question: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Error starting interactive mode: {e}")
        sys.exit(1)


def main():
    """
    Main function that parses arguments and calls the appropriate function.
    
    STUDENT EXPLANATION:
    This is the "main function" - the entry point of our program. It:
    1. Sets up the argument parser (creates the menu)
    2. Parses the user's input (figures out what they want)
    3. Calls the appropriate function (serves the right dish)
    4. Handles errors gracefully (apologizes if something goes wrong)
    
    This is like the restaurant manager who:
    - Greets customers
    - Takes their order
    - Makes sure the kitchen prepares the right food
    - Handles any problems that come up
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Route to the appropriate function based on the command
        if args.command == 'list-chapters':
            list_chapters(args.base_path, args.format)
            
        elif args.command == 'load-chapter':
            load_chapter_command(args.chapter, args.user_id, args.base_path, 
                               args.model_name, args.device, args.force)
            
        elif args.command == 'ask':
            ask_command(args.question, args.chapter, args.user_id, args.base_path,
                       args.model_name, args.device, args.output_format, 
                       args.show_context, args.show_sources)
            
        elif args.command == 'interactive':
            interactive_mode(args.chapter, args.user_id, args.base_path,
                           args.model_name, args.device)
            
        elif args.command == 'vector-store':
            if args.vector_command == 'status':
                vector_store_command('status')
            elif args.vector_command == 'list':
                vector_store_command('list', detailed=args.detailed)
            elif args.vector_command == 'cleanup':
                vector_store_command('cleanup', dry_run=args.dry_run, older_than=args.older_than)
            elif args.vector_command == 'delete':
                vector_store_command('delete', collection=args.collection)
            else:
                print("❌ Unknown vector-store command. Use --help for options.")
                
        elif args.command == 'test':
            if args.test_command == 'performance':
                test_performance(args.chapter, args.user_id, args.model_name)
            elif args.test_command == 'quality':
                test_quality(args.chapter, args.user_id, args.model_name)
            else:
                print("❌ Unknown test command. Use --help for options.")
                
        elif args.command == 'benchmark':
            benchmark_chapters(args.chapters, args.model_name, args.output)
            
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 