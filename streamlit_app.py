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

# Import our main RAG system
from llmrag.chapter_rag import ChapterRAG, list_available_chapters, list_available_chapters_with_titles


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
        # Normalize path separators for cross-platform compatibility
        path = path.replace("\\", "/")  # Ensure paths use forward slashes
        
        # Extract working group from path (e.g., "wg1" from "wg1/chapter02")
        parts = path.split('/')
        if len(parts) >= 2:
            working_group = parts[0]  # e.g., "wg1"
            chapter_num = parts[1]    # e.g., "chapter02"
            
            if working_group not in organized:
                organized[working_group] = []
            
            # Truncate title if too long (with tooltip for full title)
            truncated_title = title[:60] + "..." if len(title) > 60 else title
            
            organized[working_group].append({
                'path': path,
                'title': title,
                'truncated_title': truncated_title,
                'chapter_num': chapter_num
            })
    
    # Sort chapters within each working group
    for wg in organized:
        organized[wg].sort(key=lambda x: x['chapter_num'])
    
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
        st.write("Debug Info: Ensure the `list_available_chapters_with_titles` function is returning valid data.")
        st.write("Debug Info: Check if the directory exists and contains valid files.")
        return
    
    # Validate chapter data format
    if not isinstance(chapters_with_titles, list) or not all(isinstance(item, tuple) and len(item) == 2 for item in chapters_with_titles):
        st.error("❌ Invalid chapter data format. Expected a list of (path, title) tuples.")
        st.write(f"Debug Info: Received data: {chapters_with_titles}")
        return
    
    # Organize chapters by working group
    try:
        organized_chapters = organize_chapters_by_working_group(chapters_with_titles)
    except Exception as e:
        st.error(f"❌ Error organizing chapters: {e}")
        st.write("Debug Info: Ensure chapter paths are correctly formatted.")
        return
    
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
        
        # Create options with truncated titles and chapter numbers
        chapter_options = []
        chapter_paths = []
        
        for chapter in chapters_in_wg:
            # Format: "Chapter 02: Truncated Title..."
            option_text = f"Chapter {chapter['chapter_num'].replace('chapter', '')}: {chapter['truncated_title']}"
            chapter_options.append(option_text)
            chapter_paths.append(chapter['path'])
        
        selected_chapter_index = st.selectbox(
            "Chapter:",
            range(len(chapter_options)),
            format_func=lambda i: chapter_options[i] if i < len(chapter_options) else "",
            help="Select a chapter (hover for full title)"
        )
        
        # Show full title as tooltip/info
        if selected_chapter_index < len(chapters_in_wg):
            selected_chapter_info = chapters_in_wg[selected_chapter_index]
            st.info(f"📖 **Full Title:** {selected_chapter_info['title']}")
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
                # Create RAG system and load chapter
                rag = ChapterRAG(model_name=model_name, device=device)
                rag.load_chapter(selected_chapter, user_id)
                
                # Store in session state (persistent memory)
                st.session_state.rag_system = rag
                st.session_state.current_chapter = selected_chapter
                st.session_state.current_user = user_id
                st.session_state.model_name = model_name
                st.session_state.device = device
                
                st.success(f"✅ Chapter loaded successfully for user '{user_id}'!")
                st.rerun()  # Refresh the page to show the chat interface
                
            except Exception as e:
                st.error(f"❌ Error loading chapter: {e}")
                st.write("Debug Info: Ensure the chapter path and user ID are valid.")


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
                    # Ask the question
                    result = st.session_state.rag_system.ask(
                        prompt, 
                        st.session_state.current_chapter, 
                        st.session_state.current_user
                    )
                    
                    st.write(result['answer'])
                    
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
    st.header("⚙️ Settings & Info")
    
    # System information display
    st.subheader("System Information")
    
    # Get chapter title for display
    if st.session_state.current_chapter:
        try:
            chapters_with_titles = list_available_chapters_with_titles()
            chapter_title = None
            for path, title in chapters_with_titles:
                if path == st.session_state.current_chapter:
                    chapter_title = title
                    break
        except:
            chapter_title = None
        
        if chapter_title:
            st.write(f"**Current Chapter:** {chapter_title}")
            st.caption(f"Path: {st.session_state.current_chapter}")
        else:
            st.write(f"**Current Chapter:** {st.session_state.current_chapter}")
    else:
        st.write("**Current Chapter:** None")
    
    st.write(f"**Current User:** {st.session_state.current_user or 'None'}")
    st.write(f"**Model:** {st.session_state.model_name}")
    st.write(f"**Device:** {st.session_state.device}")
    
    # Clear session button
    if st.button("🗑️ Clear Session"):
        st.session_state.rag_system = None
        st.session_state.current_chapter = None
        st.session_state.current_user = None
        st.session_state.chat_history = []
        st.success("Session cleared!")
        st.rerun()
    
    # Export chat history
    if st.session_state.chat_history:
        st.subheader("Export Chat History")
        
        # Prepare chat data for export
        chat_data = {
            'chapter': st.session_state.current_chapter,
            'user_id': st.session_state.current_user,
            'model': st.session_state.model_name,
            'device': st.session_state.device,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'chat_history': [
                {
                    'question': q,
                    'answer': a,
                    'paragraph_ids': m.get('paragraph_ids', ''),
                    'chapter': m.get('chapter', ''),
                    'user_id': m.get('user_id', '')
                }
                for q, a, m in st.session_state.chat_history
            ]
        }
        
        # Create download button
        st.download_button(
            label="📥 Download Chat History (JSON)",
            data=json.dumps(chat_data, indent=2),
            file_name=f"chat_history_{st.session_state.current_chapter}_{st.session_state.current_user}_{time.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def main():
    """
    Main Streamlit application.
    
    STUDENT EXPLANATION:
    This is the main function that sets up the entire web application.
    It's like the "blueprint" for the entire website.
    
    The main function:
    1. Configures the page (title, icon, layout)
    2. Initializes session state (persistent memory)
    3. Creates the sidebar navigation
    4. Routes to the appropriate page based on user selection
    5. Adds footer information
    
    This pattern is common in web applications:
    - Set up the page
    - Create navigation
    - Handle user interactions
    - Display appropriate content
    """
    # Configure the page
    st.set_page_config(
        page_title="LLMRAG - IPCC Chapter RAG System",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state (persistent memory)
    init_session_state()
    
    # Create sidebar (navigation panel on the left)
    st.sidebar.title("📚 LLMRAG")
    st.sidebar.markdown("IPCC Chapter RAG System")
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigation:",
        ["Load Chapter", "Chat", "Settings"],
        index=0 if not st.session_state.rag_system else 1
    )
    
    # Route to appropriate page based on selection
    if page == "Load Chapter":
        load_chapter_interface()
    elif page == "Chat":
        chat_interface()
    elif page == "Settings":
        settings_interface()
    
    # Footer information
    st.sidebar.markdown("---")
    st.sidebar.markdown("**About:**")
    st.sidebar.markdown("LLMRAG is a Retrieval-Augmented Generation system for IPCC reports.")
    st.sidebar.markdown("Each user gets their own sandbox while sharing the same chapter content.")


# This is a Python idiom that means "only run this if the file is executed directly"
# It prevents the code from running if the file is imported as a module
if __name__ == "__main__":
    main()
