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

This CLI provides four main functions:
1. list-chapters: See what documents are available
2. load-chapter: Load a document for a specific user
3. ask: Ask a question about a loaded document
4. interactive: Have a conversation with the system
"""

import argparse  # Python's built-in argument parsing library
import sys       # System-specific parameters and functions
import json      # For working with JSON data
from pathlib import Path  # Modern way to work with file paths
from typing import Optional

# Import our main RAG system
from llmrag.chapter_rag import ChapterRAG, list_available_chapters, list_available_chapters_with_titles


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
    load_parser.add_argument('--model-name', default='gpt2', help='HuggingFace model name')
    load_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to run model on')
    
    # Command 3: Ask questions
    ask_parser = subparsers.add_parser('ask', help='Ask a question about a chapter')
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.add_argument('--chapter', required=True, help='Chapter name (e.g., wg1/chapter04)')
    ask_parser.add_argument('--user-id', default='default', help='User identifier')
    ask_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    ask_parser.add_argument('--model-name', default='gpt2', help='HuggingFace model name')
    ask_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to run model on')
    ask_parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    
    # Command 4: Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    interactive_parser.add_argument('--chapter', required=True, help='Chapter name (e.g., wg1/chapter04)')
    interactive_parser.add_argument('--user-id', default='default', help='User identifier')
    interactive_parser.add_argument('--base-path', default='tests/ipcc', help='Base path to IPCC chapters')
    interactive_parser.add_argument('--model-name', default='gpt2', help='HuggingFace model name')
    interactive_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to run model on')
    
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


def load_chapter_command(chapter: str, user_id: str, base_path: str, model_name: str, device: str) -> None:
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
        # Create a RAG system and load the chapter
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        rag.load_chapter(chapter, user_id)
        print(f"✅ Chapter '{chapter}' loaded successfully for user '{user_id}'")
    except Exception as e:
        print(f"❌ Error loading chapter: {e}")
        sys.exit(1)


def ask_command(question: str, chapter: str, user_id: str, base_path: str, model_name: str, device: str, output_format: str) -> None:
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
        # Create RAG system and ask the question
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        result = rag.ask(question, chapter, user_id)
        
        # Format the output based on user preference
        if output_format == 'json':
            # JSON format is useful for programmatic access
            print(json.dumps(result, indent=2))
        else:
            # Text format is more human-readable
            print(f"\n🤔 Question: {question}")
            print(f"📖 Chapter: {result['chapter']}")
            print(f"👤 User: {result['user_id']}")
            print(f"\n💡 Answer: {result['answer']}")
            
            # Show the context (source documents) if available
            if result.get('context'):
                print(f"\n📄 Context:")
                for i, doc in enumerate(result['context'], 1):
                    print(f"  {i}. {doc.page_content[:200]}...")
                    if doc.metadata.get('paragraph_ids'):
                        print(f"     Paragraph IDs: {doc.metadata['paragraph_ids']}")
            
            # Show paragraph IDs for source tracking
            if result.get('paragraph_ids'):
                print(f"\n📍 Source Paragraph IDs: {result['paragraph_ids']}")
    except Exception as e:
        print(f"❌ Error asking question: {e}")
        sys.exit(1)


def interactive_mode(chapter: str, user_id: str, base_path: str, model_name: str, device: str) -> None:
    """
    Start interactive mode.
    
    STUDENT EXPLANATION:
    This function creates an interactive chat session. It's like having a conversation
    with a research assistant who has access to a specific book.
    
    The interactive mode:
    1. Loads the chapter once at the beginning
    2. Enters a loop where you can ask multiple questions
    3. Shows answers and sources for each question
    4. Continues until you type 'quit' or 'exit'
    
    This is useful for:
    - Exploring a document thoroughly
    - Asking follow-up questions
    - Having a natural conversation with the system
    """
    try:
        print(f"🚀 Starting interactive mode for chapter '{chapter}' (user: '{user_id}')")
        print("Loading chapter...")
        
        # Create RAG system and load the chapter
        rag = ChapterRAG(base_path=base_path, model_name=model_name, device=device)
        rag.load_chapter(chapter, user_id)
        
        print(f"✅ Chapter loaded! You can now ask questions.")
        print("Type 'quit' or 'exit' to end the session.")
        print("-" * 50)
        
        # Main interaction loop
        while True:
            try:
                # Get user input
                question = input("\n🤔 Your question: ").strip()
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                # Skip empty questions
                if not question:
                    continue
                
                # Process the question
                print("🤖 Thinking...")
                result = rag.ask(question, chapter, user_id)
                
                # Display the answer
                print(f"\n💡 Answer: {result['answer']}")
                
                # Show sources if available
                if result.get('context'):
                    print(f"\n📄 Sources:")
                    for i, doc in enumerate(result['context'], 1):
                        print(f"  {i}. {doc.page_content[:150]}...")
                        if doc.metadata.get('paragraph_ids'):
                            print(f"     IDs: {doc.metadata['paragraph_ids']}")
                
                # Show paragraph IDs for source tracking
                if result.get('paragraph_ids'):
                    print(f"\n📍 Source Paragraph IDs: {result['paragraph_ids']}")
                
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error starting interactive mode: {e}")
        sys.exit(1)


def main():
    """
    Main CLI entry point.
    
    STUDENT EXPLANATION:
    This is the main function that runs when someone executes the CLI.
    It's like the "front door" of our application.
    
    The main function:
    1. Sets up the argument parser (creates the menu)
    2. Parses the user's input (figures out what they want)
    3. Calls the appropriate function based on their choice
    4. Handles errors gracefully
    
    This pattern is common in CLI applications:
    - Parse arguments
    - Validate input
    - Execute the requested action
    - Handle errors
    """
    # Set up the argument parser
    parser = setup_parser()
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to the appropriate function based on the command
    if args.command == 'list-chapters':
        list_chapters(args.base_path, args.format)
    elif args.command == 'load-chapter':
        load_chapter_command(args.chapter, args.user_id, args.base_path, args.model_name, args.device)
    elif args.command == 'ask':
        ask_command(args.question, args.chapter, args.user_id, args.base_path, args.model_name, args.device, args.output_format)
    elif args.command == 'interactive':
        interactive_mode(args.chapter, args.user_id, args.base_path, args.model_name, args.device)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


# This is a Python idiom that means "only run this if the file is executed directly"
# It prevents the code from running if the file is imported as a module
if __name__ == '__main__':
    main() 