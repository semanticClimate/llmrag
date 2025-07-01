# 🔧 IPCC RAG System - Developer Guide

**Technical documentation for developers, researchers, and contributors**

## 🎯 Who is this guide for?

- **Software Developers** who want to contribute code
- **Data Scientists** who want to understand the system architecture
- **Researchers** who want to modify or extend the system
- **DevOps Engineers** who want to deploy the system
- **Students** learning about RAG systems and NLP

## 🏗️ System Architecture

### High-Level Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   RAG Pipeline  │───▶│   Response      │
│   (Questions)   │    │                 │    │   + Sources     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Vector Store   │
                       │   (ChromaDB)    │
                       └─────────────────┘
```

### Core Components

#### 1. Document Processing Pipeline
```python
# HTML → Chunks → Embeddings → Vector Store
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.chunking.html_splitter import HtmlTextSplitter
from llmrag.embeddings.sentence_transformers_embedder import SentenceTransformersEmbedder
```

#### 2. RAG Pipeline
```python
# Query → Embedding → Retrieval → Generation
from llmrag.pipelines.rag_pipeline import RAGPipeline
from llmrag.retrievers.chroma_store import ChromaVectorStore
from llmrag.models.transformers_model import TransformersModel
```

#### 3. User Interfaces
- **Streamlit App**: `streamlit_app.py`
- **CLI**: `llmrag/cli.py`
- **Python API**: `llmrag/chapter_rag.py`

## 🚀 Development Setup

### Prerequisites
- Python 3.8+
- Git
- 4GB+ RAM (8GB+ recommended)
- GPU (optional, for faster inference)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/llmrag.git
cd llmrag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Development Tools
```bash
# Run tests
pytest

# Run linting
flake8 llmrag/

# Run type checking
mypy llmrag/

# Format code
black llmrag/
```

## 📁 Project Structure

```
llmrag/
├── llmrag/                    # Main package
│   ├── __init__.py
│   ├── chapter_rag.py         # High-level API
│   ├── cli.py                 # Command-line interface
│   ├── chunking/              # Text chunking
│   │   ├── html_splitter.py   # HTML processing
│   │   └── text_splitter.py   # Generic text processing
│   ├── embeddings/            # Vector embeddings
│   │   ├── base_embedder.py   # Abstract base class
│   │   └── sentence_transformers_embedder.py
│   ├── generators/            # Text generation
│   │   └── local_generator.py
│   ├── ingestion/             # Document ingestion
│   │   └── ingest_html.py
│   ├── models/                # Language models
│   │   ├── base_model.py      # Abstract base class
│   │   ├── fake_llm.py        # Mock model for testing
│   │   └── transformers_model.py
│   ├── pipelines/             # RAG pipelines
│   │   └── rag_pipeline.py
│   ├── retrievers/            # Vector stores
│   │   ├── base_vector_store.py
│   │   ├── chroma_store.py
│   │   └── faiss_store.py
│   └── utils/                 # Utilities
│       ├── pipeline_setup.py
│       └── yaml_loader.py
├── tests/                     # Test suite
│   ├── test_chunking.py
│   ├── test_embedder.py
│   ├── test_pipeline.py
│   └── data/                  # Test data
├── docs/                      # Documentation
│   ├── architecture.dot
│   └── pipeline_flow.dot
├── streamlit_app.py           # Web interface
├── requirements.txt           # Dependencies
└── README.md                  # Project overview
```

## 🔧 Core Concepts

### 1. RAG (Retrieval-Augmented Generation)

RAG combines two main components:
- **Retrieval**: Find relevant documents/chunks
- **Generation**: Create coherent answers

```python
# Basic RAG workflow
query = "What causes global warming?"
relevant_chunks = vector_store.retrieve(query, top_k=4)
answer = language_model.generate(query, context=relevant_chunks)
```

### 2. Vector Embeddings

Convert text to numerical vectors for similarity search:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Climate change is real")
# Result: [0.1, -0.3, 0.7, ...] (384-dimensional vector)
```

### 3. Vector Similarity Search

Find similar documents using cosine similarity:
```python
# Find most similar chunks to query
query_embedding = embedder.embed(query)
similar_chunks = vector_store.similarity_search(query_embedding, k=4)
```

### 4. Text Chunking

Break documents into searchable pieces:
```python
splitter = HtmlTextSplitter(chunk_size=500)
chunks = splitter.split(html_content)
# Each chunk preserves paragraph IDs for source tracking
```

## 🛠️ Extending the System

### Adding New Embedding Models

```python
# llmrag/embeddings/custom_embedder.py
from llmrag.embeddings.base_embedder import BaseEmbedder

class CustomEmbedder(BaseEmbedder):
    def __init__(self, model_name: str):
        self.model = load_custom_model(model_name)
    
    def embed(self, text: str) -> List[float]:
        return self.model.encode(text)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts)
```

### Adding New Language Models

```python
# llmrag/models/custom_model.py
from llmrag.models.base_model import BaseModel

class CustomModel(BaseModel):
    def __init__(self, model_name: str):
        self.model = load_custom_model(model_name)
    
    def generate(self, prompt: str, **kwargs) -> str:
        return self.model.generate(prompt, **kwargs)
```

### Adding New Vector Stores

```python
# llmrag/retrievers/custom_store.py
from llmrag.retrievers.base_vector_store import BaseVectorStore

class CustomVectorStore(BaseVectorStore):
    def __init__(self, embedder, **kwargs):
        super().__init__(embedder)
        self.store = initialize_custom_store(**kwargs)
    
    def add_documents(self, documents: List[Document]):
        embeddings = self.embedder.embed_batch([doc.page_content for doc in documents])
        self.store.add(embeddings, documents)
    
    def retrieve(self, query: str, top_k: int = 4) -> List[Document]:
        query_embedding = self.embedder.embed(query)
        return self.store.search(query_embedding, top_k)
```

### Adding New Chunking Strategies

```python
# llmrag/chunking/custom_splitter.py
from llmrag.chunking.text_splitter import TextSplitter

class CustomSplitter(TextSplitter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def split(self, text: str) -> List[Document]:
        # Implement custom chunking logic
        chunks = self.custom_chunking_algorithm(text)
        return [Document(page_content=chunk, metadata={}) for chunk in chunks]
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pipeline.py

# Run with coverage
pytest --cov=llmrag

# Run with verbose output
pytest -v
```

### Writing Tests
```python
# tests/test_custom_component.py
import pytest
from llmrag.custom_component import CustomComponent

def test_custom_component():
    component = CustomComponent()
    result = component.process("test input")
    assert result == "expected output"

def test_custom_component_with_mock():
    with patch('llmrag.custom_component.external_service') as mock_service:
        mock_service.return_value = "mocked response"
        component = CustomComponent()
        result = component.process("test input")
        assert result == "mocked response"
```

### Test Data
- Use `tests/data/` for test files
- Keep test data small and focused
- Use fixtures for common test setup

## 📊 Performance Optimization

### Profiling
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    result = expensive_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### Memory Optimization
```python
# Use generators for large datasets
def chunk_generator(documents):
    for doc in documents:
        yield process_document(doc)

# Batch processing
def process_in_batches(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield process_batch(batch)
```

### GPU Acceleration
```python
# Enable GPU for transformers
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Enable MPS for Apple Silicon
if torch.backends.mps.is_available():
    device = torch.device("mps")
```

## 🚀 Deployment

### Local Deployment
```bash
# Production setup
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 streamlit_app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
```

### Cloud Deployment
- **Heroku**: Use `Procfile` and `runtime.txt`
- **AWS**: Use EC2 or Lambda
- **Google Cloud**: Use App Engine or Cloud Run
- **Azure**: Use App Service

## 🔍 Debugging

### Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_function():
    logger.debug("Starting function")
    # Your code here
    logger.debug("Function completed")
```

### Error Handling
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error occurred: {e}")
    # Handle specific error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle general error
```

### Debug Mode
```python
# Enable debug mode
import os
os.environ['DEBUG'] = 'true'

# In your code
if os.getenv('DEBUG'):
    print(f"Debug: {variable}")
```

## 📚 Learning Resources

### RAG Systems
- [Retrieval-Augmented Generation Paper](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [HuggingFace RAG Guide](https://huggingface.co/docs/transformers/tasks/rag)

### Vector Databases
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FAISS Tutorial](https://github.com/facebookresearch/faiss/wiki)
- [Pinecone Guide](https://docs.pinecone.io/)

### NLP and Embeddings
- [Sentence Transformers](https://www.sbert.net/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [spaCy Tutorial](https://spacy.io/usage)

### Testing and Development
- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing Guide](https://realpython.com/python-testing/)
- [GitHub Actions](https://docs.github.com/en/actions)

## 🤝 Contributing

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

### Commit Messages
```
feat: add new embedding model
fix: resolve memory leak in chunking
docs: update installation instructions
test: add tests for custom splitter
```

---

## 🎉 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Email**: For private or urgent matters
- **Documentation**: Check the docs folder for detailed guides

**Happy coding! 🚀** 