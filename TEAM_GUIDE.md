# LLMRAG Team Guide

## Overview

LLMRAG is a Retrieval-Augmented Generation system for IPCC reports. It allows users to ask questions about specific chapters and get AI-generated answers based on the chapter content.

## Quick Start

### 1. Installation

**Prerequisites:**
- Python 3.12+ (recommended) or Python 3.8+
- 8GB+ RAM (16GB+ recommended)
- 5GB+ free disk space

**Installation Steps:**

```bash
# Clone the repository
git clone <repository-url>
cd llmrag

# Create virtual environment
python -m venv venv_py312
source venv_py312/bin/activate  # On Windows: venv_py312\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 2. Running the Application

```bash
# Activate virtual environment
source venv_py312/bin/activate

# Run Streamlit app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### 1. Load a Chapter
- Select a Working Group (e.g., WG1, WG2)
- Choose a chapter from the dropdown
- Enter a User ID (for session isolation)
- Select model and device settings
- Click "Load Chapter"

### 2. Ask Questions
- Navigate to the "Chat" tab
- Type your question in the chat input
- View the AI-generated answer
- Click "View Sources" to see the source paragraphs

### 3. Export Results
- Go to "Settings" tab
- Click "Download Chat History" to export as JSON

## Troubleshooting

### Common Issues

#### 1. Python Version Errors
**Error:** `'type' object is not subscriptable`
**Solution:** Use Python 3.12+ or ensure you're in the correct virtual environment

```bash
python --version  # Should show 3.12+
which python     # Should point to venv_py312
```

#### 2. MPS Device Errors (macOS)
**Error:** `isin_Tensor_Tensor_out only works on floating types on MPS`
**Solution:** The app now defaults to CPU on macOS < 14.0. You can also manually select "cpu" in the device dropdown.

#### 3. ChromaDB Errors
**Error:** `Error reading from metadata segment reader`
**Solution:** Clear the database and restart:

```bash
rm -rf chroma_db/
streamlit run streamlit_app.py
```

#### 4. Memory Issues
**Error:** Out of memory errors
**Solution:** 
- Use smaller models (gpt2-medium instead of gpt2-large)
- Ensure you have sufficient RAM
- Close other applications

#### 5. Missing Dependencies
**Error:** `ModuleNotFoundError`
**Solution:** Reinstall dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

### Performance Tips

1. **Model Selection:**
   - `gpt2-large`: Best quality, requires more RAM
   - `gpt2-medium`: Good balance of quality and speed
   - `distilgpt2`: Fastest, smaller memory footprint

2. **Device Selection:**
   - `auto`: Automatically selects best available device
   - `cpu`: Most compatible, works everywhere
   - `cuda`: NVIDIA GPU (fastest if available)
   - `mps`: Apple Silicon GPU (macOS 14.0+)

3. **Chapter Loading:**
   - First load takes longer (processing and embedding)
   - Subsequent loads are faster
   - Each user gets isolated sessions

## System Requirements

### Minimum Requirements
- **OS:** Windows 10+, macOS 10.15+, or Linux
- **Python:** 3.8+ (3.12+ recommended)
- **RAM:** 8GB
- **Storage:** 5GB free space
- **Network:** Internet connection for model downloads

### Recommended Requirements
- **OS:** macOS 14.0+ (for MPS support)
- **Python:** 3.12+
- **RAM:** 16GB+
- **Storage:** 10GB free space
- **GPU:** NVIDIA GPU (for CUDA) or Apple Silicon (for MPS)

## File Structure

```
llmrag/
├── streamlit_app.py          # Main web application
├── llmrag/                   # Core RAG system
│   ├── chapter_rag.py        # Main RAG orchestrator
│   ├── chunking/             # Text processing
│   ├── embeddings/           # Vector embeddings
│   ├── retrievers/           # Vector database
│   ├── generators/           # Language models
│   └── pipelines/            # RAG pipeline
├── tests/ipcc/               # IPCC chapter data
│   ├── wg1/                  # Working Group 1 chapters
│   └── wg2/                  # Working Group 2 chapters
├── chroma_db/                # Vector database (auto-created)
└── requirements.txt          # Python dependencies
```

## Development Notes

### Key Features
- **Section-specific retrieval:** Can answer questions about specific sections (e.g., "10.1")
- **Multi-user support:** Each user gets isolated sessions
- **Source tracking:** Shows which paragraphs were used for answers
- **Export functionality:** Download chat history as JSON

### Architecture
- **Chunking:** HTML documents split into semantic chunks
- **Embeddings:** Text converted to vectors using SentenceTransformers
- **Retrieval:** Similarity search in ChromaDB vector database
- **Generation:** GPT-2 models for answer generation

### Future Improvements
- Persistent ChromaDB storage
- Chapter conversion caching
- Multiple Streamlit process support
- Better title extraction for sections
- Advanced query understanding

## Support

For issues or questions:
1. Check this troubleshooting guide
2. Review the error messages carefully
3. Ensure you're using the correct Python version
4. Try clearing the database and restarting
5. Contact the development team with specific error details

## Testing

To test the system:

```bash
# Run basic tests
python test_section_retrieval.py

# Test UI improvements
python test_ui_improvements.py

# Test with specific chapter
python -c "
from llmrag.chapter_rag import ChapterRAG
rag = ChapterRAG(device='cpu')
rag.load_chapter('wg1/chapter10')
result = rag.ask('What is the title of section 10.1?', 'wg1/chapter10')
print(result['answer'])
"
```

## Known Limitations

1. **Model Quality:** GPT-2 models may not always provide perfect answers
2. **Memory Usage:** Large models require significant RAM
3. **Processing Time:** First chapter load takes time for processing
4. **Device Compatibility:** MPS support limited on older macOS versions
5. **Chapter Coverage:** Currently supports WG1 and WG2 chapters

## Updates

The system is actively being improved. Check for updates regularly and review the changelog for new features and bug fixes. 