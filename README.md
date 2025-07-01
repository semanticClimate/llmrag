# IPCC RAG System 🌍📚

**A Local Retrieval-Augmented Generation (RAG) System for IPCC Climate Reports**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 🎯 What is this?

This system helps researchers, policymakers, and students quickly find and understand information from IPCC (Intergovernmental Panel on Climate Change) reports. Think of it as a **smart research assistant** that can:

- 📖 **Load IPCC chapters** from your computer
- 🔍 **Answer questions** about climate science
- 📍 **Show you exactly where** information comes from (paragraph IDs)
- 🤖 **Run entirely on your computer** (no internet needed after setup)

## 🚀 Quick Start (5 minutes)

### 1. Install Python
First, make sure you have Python installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: Usually pre-installed, or use [Homebrew](https://brew.sh)
- **Linux**: `sudo apt install python3 python3-pip`

### 2. Download and Setup
```bash
# Download the project
git clone https://github.com/yourusername/llmrag.git
cd llmrag

# Install required packages
pip install -r requirements.txt
```

### 3. Try it out!
```bash
# Start the web interface
streamlit run streamlit_app.py

# Or use the command line
python -m llmrag.cli list-chapters
python -m llmrag.cli ask "What are the main findings about temperature trends?" --chapter wg1/chapter02
```

## 📚 Learning Resources

### For Beginners
- **What is RAG?**: [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- **Climate Science**: [IPCC FAQ](https://www.ipcc.ch/about/faq/)
- **Python Basics**: [Python.org Tutorial](https://docs.python.org/3/tutorial/)

### For Researchers
- **RAG Systems**: [Retrieval-Augmented Generation Paper](https://arxiv.org/abs/2005.11401)
- **Vector Databases**: [ChromaDB Documentation](https://docs.trychroma.com/)
- **Embeddings**: [Sentence Transformers Guide](https://www.sbert.net/)

### For Developers
- **Streamlit**: [Streamlit Documentation](https://docs.streamlit.io/)
- **HuggingFace**: [Transformers Tutorial](https://huggingface.co/docs/transformers/tutorials)
- **Vector Search**: [FAISS Tutorial](https://github.com/facebookresearch/faiss/wiki)

## 🎮 How to Use

### Web Interface (Recommended for beginners)
1. Run `streamlit run streamlit_app.py`
2. Open your browser to `http://localhost:8501`
3. Select a chapter and start asking questions!

### Command Line (For power users)
```bash
# See available chapters
python -m llmrag.cli list-chapters

# Ask a question
python -m llmrag.cli ask "What causes global warming?" --chapter wg1/chapter02

# Interactive mode
python -m llmrag.cli interactive --chapter wg1/chapter02
```

### Python Code (For developers)
```python
from llmrag.chapter_rag import ask_chapter

# Ask a question about a chapter
result = ask_chapter(
    question="What are the main climate change impacts?",
    chapter_name="wg1/chapter02"
)

print(f"Answer: {result['answer']}")
print(f"Sources: {result['paragraph_ids']}")
```

## 📁 What's Included

```
llmrag/
├── 📖 IPCC Chapters          # Climate report data
├── 🤖 RAG System            # Question answering engine
├── 🌐 Web Interface         # User-friendly browser app
├── 💻 Command Line Tools    # Power user interface
├── 🔧 Processing Pipeline   # Data preparation tools
└── 📊 Documentation         # Guides and tutorials
```

## 🛠️ System Components

### Core RAG System
- **Document Loading**: Processes IPCC HTML chapters
- **Text Chunking**: Breaks documents into searchable pieces
- **Vector Search**: Finds relevant information quickly
- **Answer Generation**: Creates coherent responses
- **Source Tracking**: Shows exactly where answers come from

### User Interfaces
- **Streamlit Web App**: Beautiful, interactive interface
- **Command Line**: Fast, scriptable interface
- **Python API**: For integration with other tools

### Data Processing
- **HTML Cleaning**: Removes formatting, keeps content
- **Paragraph IDs**: Tracks information sources
- **Semantic Chunking**: Keeps related information together

## 🔬 Technical Details

### Models Used
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Language Model**: GPT-2 Large (774M parameters)
- **Vector Database**: ChromaDB (local storage)

### Performance
- **Speed**: Answers in 2-5 seconds
- **Accuracy**: Based on IPCC content only
- **Memory**: ~2GB RAM for full system
- **Storage**: ~500MB for all chapters

## 🤝 Contributing

We welcome contributions! Here's how to help:

### For Non-Developers
- 📝 **Report bugs** or suggest improvements
- 📚 **Test the system** with your research questions
- 📖 **Improve documentation** or write tutorials
- 🌍 **Share with colleagues** who might find it useful

### For Developers
- 🔧 **Fix bugs** or add features
- 🧪 **Add tests** to ensure quality
- 📦 **Improve packaging** or deployment
- 🚀 **Optimize performance**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **IPCC**: For providing the climate science reports
- **HuggingFace**: For the language models and tools
- **ChromaDB**: For the vector database
- **Streamlit**: For the web interface framework
- **Open Source Community**: For all the amazing tools we build upon

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/llmrag/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/llmrag/discussions)
- **Email**: your.email@example.com

## 📈 Roadmap

- [ ] **More IPCC Chapters**: Add WG2 and WG3 reports
- [ ] **Better Models**: Upgrade to larger language models
- [ ] **Multi-language**: Support for non-English reports
- [ ] **Collaborative Features**: Share questions and answers
- [ ] **Mobile App**: iOS and Android versions

---

**Made with ❤️ for climate science research**

## 🚀 Quickstart for Collaborators

### Prerequisites
- Python 3.9 or higher (Python 3.12 recommended)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/semanticClimate/llmrag.git
cd llmrag
```

### 2. Set Up Virtual Environment

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -e .
pip install -r requirements.txt
```

### 4. Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
coverage run --source=llmrag -m pytest tests/
coverage report -m
```

### 5. Test IPCC HTML Ingestion (New Feature)
```bash
python test_ipcc_ingestion.py
```

This will:
- Ingest the IPCC Chapter 4 HTML file with paragraph IDs
- Test the RAG pipeline with climate-related queries
- Show which paragraph IDs were used to generate answers

## 🔧 Features

### HTML Ingestion with Paragraph ID Tracking
The system now supports ingesting HTML documents and tracking paragraph IDs for source attribution:

- **HTML Splitter**: Extracts text while preserving paragraph IDs from HTML elements
- **RAG Pipeline**: Returns paragraph IDs used in generating answers
- **Test Script**: `test_ipcc_ingestion.py` demonstrates the feature with IPCC content

### Example Output
```
Query: What are the main scenarios used in climate projections?
Answer: [Generated answer]
Paragraph IDs found: ['4.1_p3', '4.3.2.2_p2']
```

## 🐛 Troubleshooting

### Windows-Specific Issues
- **Virtual Environment**: Make sure to use the correct activation script for your shell
- **Dependencies**: If you encounter issues with `lxml` or `transformers`, try:
  ```bash
  pip install lxml transformers
  ```
- **DLL Errors**: Ensure you have the latest Python and pip versions

### General Issues
- **Python Version**: We recommend Python 3.12. Some libraries may have compatibility issues with older versions
- **Virtual Environment**: *ALWAYS USE A VIRTUAL ENVIRONMENT* to avoid conflicts
- **NumPy Conflicts**: If you have NumPy in your global environment, it may cause issues. Use a clean virtual environment

## 📁 Project Structure

```
llmrag/
├── llmrag/                    # Main package
│   ├── chunking/             # Text splitting (including HTML)
│   ├── embeddings/           # Embedding models
│   ├── models/               # LLM models
│   ├── pipelines/            # RAG pipeline
│   └── retrievers/           # Vector stores
├── tests/                    # Test suite
│   └── ipcc/                # IPCC test data
├── test_ipcc_ingestion.py   # IPCC ingestion test script
└── requirements.txt          # Dependencies
```

## 📝 Development

For chat history and development notes, see:
- `./project.md` - Project documentation
- `./all_code.py` - Development history (Messy)

## 🧪 Testing

The test suite includes:
- Unit tests for all components
- Integration tests for the RAG pipeline
- HTML ingestion tests with paragraph ID tracking
- IPCC content tests

Run tests with:
```bash
python -m pytest tests/ -v
```

Expected result:
```
=========================================== 10 passed in 27.61s ============================================
```

# TEST
```
git clone https://github.com/semanticClimate/llmrag/
```
Then
```cd llmrag```

setup and activate a virtual environment
(on Mac:
```
python3.12 -m venv venv
source venv/bin/activate
```
run the tests - should take about 0.5 min
```
pip install -r requirements.txt
coverage run --source=llmrag -m unittest discover -s tests
coverage report -m
```

result:
```
..Device set to use cpu
..Retrieved: [('Paris is the capital of France.', 0.2878604531288147)]
.Retrieved: [('Paris is the capital of France.', 0.37026578187942505)]
.
----------------------------------------------------------------------
Ran 6 tests in 20.267s

OK
```

to print the coverage:

```
 coverage report -m
```

# BUGS

We run on Python 3.12. This can cause problems with some libraries, such as NumPy. Although `numpy` is not included in `llmrag` at present it may be in your environment. *ALWAYS USE A VIRTUAL ENVIRONMENT*

