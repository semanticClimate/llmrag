#!/usr/bin/env python3
"""
Streamlit Web Application for LLMRAG - IPCC Chapter RAG System

STUDENT GUIDE:
This file shows how to create a modern web application using Streamlit.
Streamlit is a Python library that makes it easy to build web apps for data science and AI.

Key Concepts:
- Web Application: A program that runs in a web browser
- User Interface (UI): The visual elements users interact with (buttons, forms, etc.)
- Session State: Data that persists during a user's session
- Components: Reusable UI elements (like buttons, text inputs, etc.)

Think of it like building a website with Python instead of HTML/CSS/JavaScript.
Streamlit handles all the web stuff for you, so you can focus on the Python logic.

This app provides:
1. A web interface for loading IPCC chapters
2. A chat interface for asking questions
3. Settings and export functionality
4. A modern, responsive design
"""

import streamlit as st  # Main Streamlit library for web apps
import json             # For working with JSON data
import time             # For timestamps and delays
from pathlib import Path  # Modern way to work with file paths
from typing import Dict, List, Optional
import os

# Import our main RAG system
from llmrag.chapter_rag import ChapterRAG, list_available_chapters, list_available_chapters_with_titles
from llmrag.utils.vector_store_manager import VectorStoreManager, print_vector_store_status


def get_chapter_size(chapter_path: str) -> str:
    """
    Get the approximate size of a chapter for display.
    
    Args:
        chapter_path: Path to the chapter (e.g., "wg1/chapter02")
        
    Returns:
        Human-readable size string (e.g., "1.2 MB", "850 KB")
    """
    try:
        html_file = Path(f"tests/ipcc/{chapter_path}/html_with_ids.html")
        if html_file.exists():
            size_bytes = html_file.stat().st_size
            if size_bytes > 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
            else:
                return f"{size_bytes / 1024:.0f} KB"
        else:
            return "Unknown"
    except:
        return "Unknown"


def init_session_state():
    """
    Initialize session state variables.
    
    STUDENT EXPLANATION:
    Session state is like a "memory" that persists during a user's visit to the website.
    It's like having a notepad that remembers things between page refreshes.
    
    We use session state to store:
    - The RAG system instance (so we don't reload it every time)
    - Current chapter and user information
    - Chat history (so conversations persist)
    - Model settings (which AI model to use)
    
    Think of it like a shopping cart that remembers what you put in it.
    """
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = None
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model_name' not in st.session_state:
        st.session_state.model_name = "gpt2-large"
    if 'device' not in st.session_state:
        st.session_state.device = "cpu"


def organize_chapters_by_working_group(chapters_with_titles):
    """
    Organize chapters by working group for better navigation.
    
    Args:
        chapters_with_titles: List of (path, title) tuples
        
    Returns:
        Dict with working groups as keys and lists of chapters as values
    """
    organized = {}
    
    for path, title in chapters_with_titles:
        # Extract working group from path (e.g., "wg1" from "wg1/chapter02")
        parts = path.split('/')
        if len(parts) >= 2:
            working_group = parts[0]  # e.g., "wg1"
            chapter_num = parts[1]    # e.g., "chapter02"
            
            if working_group not in organized:
                organized[working_group] = []
            
            # Truncate title if too long (with tooltip for full title)
            truncated_title = title[:60] + "..." if len(title) > 60 else title
            
            # Get chapter size
            chapter_size = get_chapter_size(path)
            
            organized[working_group].append({
                'path': path,
                'title': title,
                'truncated_title': truncated_title,
                'chapter_num': chapter_num,
                'size': chapter_size
            })
    
    # Sort chapters within each working group by size (smallest first) then by chapter number
    for wg in organized:
        organized[wg].sort(key=lambda x: (x['size'], x['chapter_num']))
    
    return organized


def get_safe_device():
    """
    Get a safe device setting, defaulting to CPU if GPU is not available.
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
    except:
        return "cpu"


def load_chapter_interface():
    """
    Interface for loading chapters with improved cascading menu.
    
    STUDENT EXPLANATION:
    This function creates the web interface for loading chapters. It's like creating
    a form where users can:
    - Select which chapter they want to load using cascading menus
    - Enter their user ID
    - Choose which AI model to use
    - Click a button to load everything
    
    Streamlit components used:
    - st.header(): Creates a title
    - st.selectbox(): Creates a dropdown menu
    - st.text_input(): Creates a text field
    - st.button(): Creates a clickable button
    - st.spinner(): Shows a loading animation
    - st.success()/st.error(): Shows success/error messages
    """
    st.header("📖 Load IPCC Chapter")
    
    # Get available chapters with titles
    try:
        chapters_with_titles = list_available_chapters_with_titles()
        if not chapters_with_titles:
            st.error("❌ No chapters found. Make sure you have IPCC chapters in the tests/ipcc directory.")
            return
    except Exception as e:
        st.error(f"❌ Error loading chapters: {e}")
        return
    
    # Organize chapters by working group
    organized_chapters = organize_chapters_by_working_group(chapters_with_titles)
    
    # Chapter selection with cascading menus
    st.subheader("Select Chapter")
    
    # First level: Working Group selection
    working_groups = sorted(organized_chapters.keys())
    selected_wg = st.selectbox(
        "Working Group:",
        working_groups,
        help="Select the IPCC Working Group"
    )
    
    if selected_wg:
        # Second level: Chapter selection within working group
        chapters_in_wg = organized_chapters[selected_wg]
        
        # Create options with truncated titles, chapter numbers, and sizes
        chapter_options = []
        chapter_paths = []
        
        for chapter in chapters_in_wg:
            # Format: "Chapter 02 (850 KB): Truncated Title..."
            option_text = f"Chapter {chapter['chapter_num'].replace('chapter', '')} ({chapter['size']}): {chapter['truncated_title']}"
            chapter_options.append(option_text)
            chapter_paths.append(chapter['path'])
        
        selected_chapter_index = st.selectbox(
            "Chapter:",
            range(len(chapter_options)),
            format_func=lambda i: chapter_options[i] if i < len(chapter_options) else "",
            help="Select a chapter (hover for full title). Smaller chapters load faster for testing."
        )
        
        # Show full title and size as tooltip/info
        if selected_chapter_index < len(chapters_in_wg):
            selected_chapter_info = chapters_in_wg[selected_chapter_index]
            st.info(f"📖 **Full Title:** {selected_chapter_info['title']}  \n📊 **Size:** {selected_chapter_info['size']}")
            selected_chapter = selected_chapter_info['path']
        else:
            selected_chapter = None
    else:
        selected_chapter = None
    
    # User ID input field
    user_id = st.text_input(
        "User ID:",
        value="default",
        help="Enter a unique identifier for your session"
    )
    
    # Model configuration in two columns (side by side)
    col1, col2 = st.columns(2)
    
    with col1:
        # Model selection dropdown
        model_name = st.selectbox(
            "Model", 
            ["gpt2-large", "gpt2-medium", "gpt2", "distilgpt2"], 
            index=0,
            help="Select the language model to use for generating answers"
        )
    
    with col2:
        # Device selection with smart defaults
        safe_device = get_safe_device()
        device_options = ["auto", "cpu", "mps", "cuda"]
        
        # Set default index based on safe device
        default_device_index = device_options.index(safe_device) if safe_device in device_options else 1
        
        device = st.selectbox(
            "Device", 
            device_options,
            index=default_device_index,
            help=f"Select the device to run the model on (auto = best available, current best: {safe_device})"
        )
    
    # Load button
    if st.button("🚀 Load Chapter", type="primary"):
        if not selected_chapter or not user_id:
            st.error("Please select a chapter and enter a user ID.")
            return
        
        # Show loading spinner while processing
        with st.spinner("Loading chapter..."):
            try:
                # Create progress bar for loading
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                status_text.text("Initializing RAG system...")
                progress_bar.progress(10)
                
                # Create RAG system and load chapter
                rag = ChapterRAG(model_name=model_name, device=device)
                
                status_text.text("Loading chapter content...")
                progress_bar.progress(30)
                
                rag.load_chapter(selected_chapter, user_id)
                
                status_text.text("Finalizing setup...")
                progress_bar.progress(90)
                
                # Store in session state (persistent memory)
                st.session_state.rag_system = rag
                st.session_state.current_chapter = selected_chapter
                st.session_state.current_user = user_id
                st.session_state.model_name = model_name
                st.session_state.device = device
                
                progress_bar.progress(100)
                status_text.text("Complete!")
                
                st.success(f"✅ Chapter loaded successfully for user '{user_id}'!")
                st.rerun()  # Refresh the page to show the chat interface
                
            except Exception as e:
                st.error(f"❌ Error loading chapter: {e}")


def chat_interface():
    """
    Interface for chatting with the loaded chapter.
    
    STUDENT EXPLANATION:
    This function creates a chat interface similar to ChatGPT or other chat apps.
    It includes:
    - Display of chat history (previous questions and answers)
    - A chat input field for new questions
    - Expandable sections showing source information
    - Real-time processing with loading indicators
    
    Streamlit components used:
    - st.chat_message(): Creates chat bubbles
    - st.chat_input(): Creates a chat input field
    - st.expander(): Creates collapsible sections
    - st.write(): Displays text content
    """
    if not st.session_state.rag_system:
        st.warning("⚠️ Please load a chapter first.")
        return
    
    # Get chapter title for display
    try:
        chapters_with_titles = list_available_chapters_with_titles()
        chapter_title = None
        for path, title in chapters_with_titles:
            if path == st.session_state.current_chapter:
                chapter_title = title
                break
    except:
        chapter_title = st.session_state.current_chapter
    
    # Display chapter information
    if chapter_title:
        st.header(f"💬 Chat with: {chapter_title}")
        st.caption(f"Chapter: {st.session_state.current_chapter}")
    else:
        st.header(f"💬 Chat with {st.session_state.current_chapter}")
    
    st.info(f"👤 User: {st.session_state.current_user} | 🤖 Model: {st.session_state.model_name} | 💻 Device: {st.session_state.device}")
    
    # Display chat history
    for i, (question, answer, metadata) in enumerate(st.session_state.chat_history):
        # User message bubble
        with st.chat_message("user"):
            st.write(question)
        
        # Assistant message bubble
        with st.chat_message("assistant"):
            st.write(answer)
            
            # Show metadata in expander (collapsible section)
            with st.expander("📄 View Sources"):
                if metadata.get('context'):
                    st.write("**Context Sources:**")
                    for j, doc in enumerate(metadata['context'], 1):
                        st.write(f"{j}. {doc.page_content[:200]}...")
                        if doc.metadata.get('paragraph_ids'):
                            st.write(f"   **IDs:** {doc.metadata['paragraph_ids']}")
                
                if metadata.get('paragraph_ids'):
                    st.write(f"**Source Paragraph IDs:** {metadata['paragraph_ids']}")
    
    # Chat input field
    if prompt := st.chat_input("Ask a question about the chapter..."):
        # Add user message to chat
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response from RAG system
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    # Create progress indicators
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Update progress
                    status_text.text("Searching for relevant content...")
                    progress_bar.progress(25)
                    
                    # Ask the question
                    result = st.session_state.rag_system.ask(
                        prompt, 
                        st.session_state.current_chapter, 
                        st.session_state.current_user
                    )
                    
                    status_text.text("Generating answer...")
                    progress_bar.progress(75)
                    
                    st.write(result['answer'])
                    
                    status_text.text("Complete!")
                    progress_bar.progress(100)
                    
                    # Store in chat history
                    metadata = {
                        'context': result.get('context', []),
                        'paragraph_ids': result.get('paragraph_ids', ''),
                        'chapter': result.get('chapter', ''),
                        'user_id': result.get('user_id', '')
                    }
                    st.session_state.chat_history.append((prompt, result['answer'], metadata))
                    
                    # Show sources in expander
                    with st.expander("📄 View Sources"):
                        if result.get('context'):
                            st.write("**Context Sources:**")
                            for i, doc in enumerate(result['context'], 1):
                                st.write(f"{i}. {doc.page_content[:200]}...")
                                if doc.metadata.get('paragraph_ids'):
                                    st.write(f"   **IDs:** {doc.metadata['paragraph_ids']}")
                        
                        if result.get('paragraph_ids'):
                            st.write(f"**Source Paragraph IDs:** {result['paragraph_ids']}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def settings_interface():
    """
    Interface for settings and system information.
    
    STUDENT EXPLANATION:
    This function creates a settings page where users can:
    - View current system information
    - Clear their session (like logging out)
    - Export their chat history as a JSON file
    
    This is like a "user preferences" or "account settings" page in other apps.
    """
    st.header("⚙️ Settings & System Info")
    
    # System Information
    st.subheader("System Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Python Version", "3.12+")
        st.metric("Framework", "LLM-RAG")
    
    with col2:
        st.metric("Model", st.session_state.get('model_name', 'gpt2-large'))
        st.metric("Device", st.session_state.get('device', 'auto'))
    
    # Vector Store Management
    st.subheader("📚 Vector Store Management")
    
    manager = VectorStoreManager()
    storage_info = manager.get_storage_info()
    
    if storage_info["exists"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Storage Size", f"{storage_info['size_mb']} MB")
        with col2:
            st.metric("Collections", storage_info['collections'])
        with col3:
            st.metric("Total Documents", storage_info['total_documents'])
        
        # Show collections
        collections = manager.list_collections()
        if collections:
            st.write("**Cached Collections:**")
            for coll in collections:
                st.write(f"• {coll['name']}: {coll['count']} documents")
            
            # Cleanup options
            st.write("**Storage Management:**")
            if st.button("🗑️ Clear All Cached Data", type="secondary"):
                deleted_count = 0
                for coll in collections:
                    if manager.delete_collection(coll['name']):
                        deleted_count += 1
                st.success(f"Deleted {deleted_count} collections")
                st.rerun()
        else:
            st.info("No collections found")
    else:
        st.info("No vector store found. Chapters will be processed on first load.")
    
    # Session Management
    st.subheader("🔄 Session Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Session", type="secondary"):
            st.session_state.clear()
            st.success("Session reset successfully!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    # Model Configuration
    st.subheader("🤖 Model Configuration")
    
    model_name = st.selectbox(
        "Model",
        ["gpt2-large", "gpt2-medium", "gpt2"],
        index=0,
        help="Larger models provide better quality but use more memory"
    )
    
    device = st.selectbox(
        "Device",
        ["auto", "cpu", "cuda", "mps"],
        index=0,
        help="Device to run the model on"
    )
    
    if st.button("💾 Save Model Settings"):
        st.session_state.model_name = model_name
        st.session_state.device = device
        st.success("Model settings saved!")
    
    # Performance Tips
    st.subheader("💡 Performance Tips")
    st.info("""
    **For better performance:**
    - Use `gpt2-large` for best answer quality
    - Use `gpt2-medium` for good balance of speed and quality
    - Use `gpt2` for fastest responses
    - First chapter load takes longer (processing), subsequent loads are cached
    - Each user gets isolated sessions
    """)


def main():
    """
    Main application function.
    
    STUDENT EXPLANATION:
    This is the main function that runs the entire application. It:
    1. Sets up the page configuration
    2. Initializes session state
    3. Creates the navigation sidebar
    4. Shows the appropriate interface based on user selection
    
    Think of it like the "main menu" of a video game - it's where everything starts.
    """
    # Page configuration
    st.set_page_config(
        page_title="LLMRAG - IPCC Chapter RAG System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("📚 LLMRAG System")
    st.sidebar.markdown("IPCC Chapter RAG System")
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigation",
        ["📖 Load Chapter", "💬 Chat", "⚙️ Settings & Info"],
        index=0 if not st.session_state.rag_system else 1
    )
    
    # Display appropriate interface based on selection
    if page == "📖 Load Chapter":
        load_chapter_interface()
    elif page == "💬 Chat":
        chat_interface()
    elif page == "⚙️ Settings & Info":
        settings_interface()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Team Testing Mode**")
    st.sidebar.markdown("Use smaller chapters first for faster testing.")


if __name__ == "__main__":
    main()
