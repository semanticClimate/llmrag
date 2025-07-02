# 🤝 Contributing to IPCC RAG System

**Thank you for your interest in contributing to the IPCC RAG System!**

This guide will help you get started with contributing to the project, whether you're a developer, researcher, or climate science enthusiast.

## 🎯 How You Can Help

### For Non-Developers
- 📝 **Report bugs** or suggest improvements
- 📚 **Test the system** with your research questions
- 📖 **Improve documentation** or write tutorials
- 🌍 **Share with colleagues** who might find it useful
- 💡 **Suggest new features** based on your needs

### For Developers
- 🔧 **Fix bugs** or add features
- 🧪 **Add tests** to ensure quality
- 📦 **Improve packaging** or deployment
- 🚀 **Optimize performance**
- 🔍 **Add new models** or capabilities

### For Researchers
- 📊 **Validate answers** against IPCC reports
- 🔬 **Test with domain-specific questions**
- 📈 **Suggest improvements** for scientific accuracy
- 🌐 **Help with multi-language support**

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/llmrag.git
cd llmrag

# Add the original repository as upstream
git remote add upstream https://github.com/originalusername/llmrag.git
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=llmrag

# Run specific test file
pytest tests/test_pipeline.py
```

## 📋 Development Workflow

### 1. Create a Feature Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

### 2. Make Your Changes
- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation as needed
- Keep commits small and focused

### 3. Test Your Changes
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

### 4. Commit Your Changes
```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new embedding model for better accuracy"

# Push to your fork
git push origin feature/your-feature-name
```

### 5. Create a Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template
5. Submit the PR

## 📝 Code Style Guidelines

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all functions
- Write docstrings for all classes and functions
- Keep functions small and focused (max 50 lines)
- Use meaningful variable names

### Example Code Style
```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ClimateData:
    """Represents climate data with temperature and uncertainty."""
    
    temperature: float
    uncertainty: float
    year: int
    source: str

def process_climate_data(data: List[ClimateData]) -> Optional[float]:
    """
    Process climate data and return average temperature.
    
    Args:
        data: List of climate data points
        
    Returns:
        Average temperature if data is valid, None otherwise
    """
    if not data:
        return None
    
    return sum(d.temperature for d in data) / len(data)
```

### File Organization
- Use absolute imports: `from llmrag.models import TransformersModel`
- Group imports: standard library, third-party, local
- Keep files focused on a single responsibility
- Use descriptive file names

### Testing Guidelines
- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common test setup
- Aim for >80% code coverage

## 🐛 Bug Reports

### Before Reporting
1. Check if the issue is already reported
2. Try to reproduce the issue
3. Check the troubleshooting guide
4. Test with different inputs

### Bug Report Template
```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Type '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 12.0]
- Python Version: [e.g. 3.9.7]
- System RAM: [e.g. 8GB]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### Before Requesting
1. Check if the feature is already planned
2. Consider if it fits the project's scope
3. Think about implementation complexity
4. Consider impact on existing functionality

### Feature Request Template
```markdown
**Feature Description**
A clear description of the feature you'd like.

**Use Case**
Why this feature would be useful.

**Proposed Implementation**
How you think it could be implemented (optional).

**Alternatives Considered**
Other ways to achieve the same goal.

**Additional Context**
Any other context about the feature request.
```

## 🔧 Common Development Tasks

### Adding a New Model
1. Create model class in `llmrag/models/`
2. Inherit from `BaseModel`
3. Implement required methods
4. Add tests in `tests/test_models.py`
5. Update documentation

### Adding a New Embedding Method
1. Create embedder class in `llmrag/embeddings/`
2. Inherit from `BaseEmbedder`
3. Implement `embed()` and `embed_batch()`
4. Add tests in `tests/test_embeddings.py`
5. Update configuration options

### Adding a New Vector Store
1. Create store class in `llmrag/retrievers/`
2. Inherit from `BaseVectorStore`
3. Implement required methods
4. Add tests in `tests/test_retrievers.py`
5. Update documentation

### Improving Documentation
1. Update relevant `.md` files
2. Add code examples
3. Include screenshots for UI changes
4. Update architecture diagrams if needed
5. Test all links and code examples

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_pipeline.py

# Run tests matching pattern
pytest -k "test_embedding"

# Run with coverage
pytest --cov=llmrag --cov-report=html
```

### Writing Tests
```python
import pytest
from unittest.mock import patch
from llmrag.models import TransformersModel

def test_transformers_model_initialization():
    """Test that TransformersModel initializes correctly."""
    model = TransformersModel("gpt2")
    assert model.model_name == "gpt2"

def test_transformers_model_generation():
    """Test text generation with TransformersModel."""
    model = TransformersModel("gpt2")
    result = model.generate("Hello world")
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.fixture
def sample_documents():
    """Fixture providing sample documents for testing."""
    return [
        Document(page_content="Climate change is real", metadata={"id": "1"}),
        Document(page_content="Global temperatures are rising", metadata={"id": "2"})
    ]

def test_rag_pipeline_with_documents(sample_documents):
    """Test RAG pipeline with sample documents."""
    pipeline = RAGPipeline()
    result = pipeline.process("What is climate change?", sample_documents)
    assert "answer" in result
    assert "sources" in result
```

## 📊 Performance Guidelines

### Code Optimization
- Profile code before optimizing
- Use appropriate data structures
- Avoid unnecessary computations
- Consider memory usage
- Test with realistic data sizes

### Memory Management
- Use generators for large datasets
- Clean up resources properly
- Monitor memory usage
- Consider batch processing
- Use appropriate model sizes

## 🔒 Security Guidelines

### Data Handling
- Don't log sensitive information
- Validate all inputs
- Use secure random number generation
- Follow principle of least privilege
- Keep dependencies updated

### Code Review Checklist
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Error handling appropriate
- [ ] No SQL injection vulnerabilities
- [ ] No path traversal issues

## 📈 Release Process

### Version Numbers
We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number updated
- [ ] Release notes written
- [ ] Dependencies checked

## 🎉 Recognition

### Contributors
All contributors will be:
- Listed in the README
- Mentioned in release notes
- Given credit in documentation
- Invited to join the project team

### Types of Contributions
- **Code**: Bug fixes, features, improvements
- **Documentation**: Guides, tutorials, examples
- **Testing**: Bug reports, test cases, validation
- **Community**: Support, feedback, promotion

## 📞 Getting Help

### Development Questions
- **GitHub Discussions**: For general questions
- **GitHub Issues**: For specific problems
- **Email**: For private or urgent matters

### Learning Resources
- [Python Documentation](https://docs.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Open Source Guide](https://opensource.guide/)

---

## 🚀 Ready to Contribute?

1. **Fork the repository**
2. **Set up your environment**
3. **Pick an issue** or create a new one
4. **Make your changes**
5. **Submit a pull request**

**Thank you for helping make the IPCC RAG System better! 🌍📚**

---

*This guide is part of the IPCC RAG System project. For more information, see the [README.md](README.md) and [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md).* 