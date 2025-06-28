# llmrag

LLM-RAG system built by PMR and ChatGPT allowing for flexible usage.

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

