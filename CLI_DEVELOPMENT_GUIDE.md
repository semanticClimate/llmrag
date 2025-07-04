# CLI Development Guide

**LLM-RAG Command Line Interface for Development and Testing**

## 🚀 Quick Start

The CLI provides a powerful command-line interface for development, testing, and automation of the LLM-RAG system.

### Basic Usage

```bash
# Show all available commands
python -m llmrag.cli --help

# List available chapters
python -m llmrag.cli list-chapters

# Ask a question
python -m llmrag.cli ask "What are climate scenarios?" --chapter wg1/chapter04

# Interactive mode
python -m llmrag.cli interactive --chapter wg1/chapter04
```

## 📚 Available Commands

### 1. Chapter Management

#### List Chapters
```bash
# Simple list
python -m llmrag.cli list-chapters --format simple

# Detailed list with titles
python -m llmrag.cli list-chapters --format detailed
```

#### Load Chapter
```bash
# Basic load
python -m llmrag.cli load-chapter wg1/chapter04 --user-id developer

# With custom model and device
python -m llmrag.cli load-chapter wg1/chapter04 \
  --user-id developer \
  --model-name gpt2-large \
  --device cpu

# Force re-ingestion (ignore cache)
python -m llmrag.cli load-chapter wg1/chapter04 --force
```

### 2. Question Answering

#### Single Question
```bash
# Basic question
python -m llmrag.cli ask "What are the main findings?" --chapter wg1/chapter04

# With detailed output
python -m llmrag.cli ask "What are the main findings?" \
  --chapter wg1/chapter04 \
  --show-context \
  --show-sources

# JSON output for automation
python -m llmrag.cli ask "What are the main findings?" \
  --chapter wg1/chapter04 \
  --output-format json
```

#### Interactive Mode
```bash
# Start interactive session
python -m llmrag.cli interactive --chapter wg1/chapter04 --user-id developer

# Available commands in interactive mode:
# - help: Show available commands
# - status: Show session statistics
# - quit/q: Exit session
```

### 3. Vector Store Management

#### Status and Information
```bash
# Show overall status
python -m llmrag.cli vector-store status

# List all collections
python -m llmrag.cli vector-store list

# Detailed collection info
python -m llmrag.cli vector-store list --detailed
```

#### Cleanup and Maintenance
```bash
# Dry run cleanup (see what would be deleted)
python -m llmrag.cli vector-store cleanup --dry-run

# Actually clean up old collections
python -m llmrag.cli vector-store cleanup

# Delete specific collection
python -m llmrag.cli vector-store delete collection_name
```

### 4. Testing and Benchmarking

#### Performance Testing
```bash
# Test caching performance
python -m llmrag.cli test performance --chapter wg1/chapter04

# With custom parameters
python -m llmrag.cli test performance \
  --chapter wg1/chapter04 \
  --user-id perf_test \
  --model-name gpt2-medium
```

#### Quality Testing
```bash
# Test answer quality
python -m llmrag.cli test quality --chapter wg1/chapter04

# With custom model
python -m llmrag.cli test quality \
  --chapter wg1/chapter04 \
  --model-name gpt2-large
```

#### Comprehensive Benchmarking
```bash
# Benchmark multiple chapters
python -m llmrag.cli benchmark --chapters wg1/chapter04,wg1/chapter02

# Save results to file
python -m llmrag.cli benchmark \
  --chapters wg1/chapter04,wg1/chapter02 \
  --output benchmark_results.json
```

## 🔧 Development Workflows

### 1. Model Development

```bash
# Test different models
python -m llmrag.cli ask "Test question" --chapter wg1/chapter04 --model-name gpt2
python -m llmrag.cli ask "Test question" --chapter wg1/chapter04 --model-name gpt2-medium
python -m llmrag.cli ask "Test question" --chapter wg1/chapter04 --model-name gpt2-large

# Compare performance
python -m llmrag.cli benchmark --chapters wg1/chapter04 --model-name gpt2-medium
python -m llmrag.cli benchmark --chapters wg1/chapter04 --model-name gpt2-large
```

### 2. Prompt Engineering

```bash
# Test different questions to evaluate prompt quality
python -m llmrag.cli interactive --chapter wg1/chapter04 --user-id prompt_dev

# Use JSON output for analysis
python -m llmrag.cli ask "What are climate scenarios?" \
  --chapter wg1/chapter04 \
  --output-format json > test_result.json
```

### 3. Performance Optimization

```bash
# Test caching effectiveness
python -m llmrag.cli test performance --chapter wg1/chapter04

# Monitor vector store usage
python -m llmrag.cli vector-store status

# Clean up when needed
python -m llmrag.cli vector-store cleanup --dry-run
```

### 4. Quality Assurance

```bash
# Run quality tests
python -m llmrag.cli test quality --chapter wg1/chapter04

# Test with different chapters
python -m llmrag.cli test quality --chapter wg1/chapter02
python -m llmrag.cli test quality --chapter wg2/chapter05
```

## 📊 Output Formats

### Text Output (Default)
```
📝 Answer (2.34s):
============================================================
The IPCC uses four main scenarios for climate projections...

📄 Sources: 4.1_p3, references_p657, references_p658...
```

### JSON Output
```json
{
  "question": "What are climate scenarios?",
  "chapter": "wg1/chapter04",
  "user_id": "developer",
  "answer": "The IPCC uses four main scenarios...",
  "response_time": 2.34,
  "paragraph_ids": ["4.1_p3", "references_p657"],
  "context_count": 4
}
```

## 🛠️ Advanced Usage

### Automation Scripts

```bash
#!/bin/bash
# Example: Test multiple chapters

chapters=("wg1/chapter04" "wg1/chapter02" "wg2/chapter05")
questions=("What are the main findings?" "What are climate scenarios?" "How do models work?")

for chapter in "${chapters[@]}"; do
    echo "Testing $chapter..."
    for question in "${questions[@]}"; do
        python -m llmrag.cli ask "$question" --chapter "$chapter" --output-format json
    done
done
```

### Performance Monitoring

```bash
# Monitor vector store growth
watch -n 30 'python -m llmrag.cli vector-store status'

# Track response times
python -m llmrag.cli ask "test" --chapter wg1/chapter04 --output-format json | jq '.response_time'
```

### Batch Processing

```bash
# Process multiple questions
echo "What are scenarios?
What are models?
What are projections?" | while read question; do
    python -m llmrag.cli ask "$question" --chapter wg1/chapter04
done
```

## 🔍 Troubleshooting

### Common Issues

1. **Chapter not found**
   ```bash
   # Check available chapters
   python -m llmrag.cli list-chapters
   ```

2. **Slow performance**
   ```bash
   # Check if caching is working
   python -m llmrag.cli test performance --chapter wg1/chapter04
   ```

3. **Memory issues**
   ```bash
   # Use smaller model
   python -m llmrag.cli ask "question" --chapter wg1/chapter04 --model-name gpt2-medium
   ```

4. **Vector store issues**
   ```bash
   # Check status
   python -m llmrag.cli vector-store status
   
   # Clean up if needed
   python -m llmrag.cli vector-store cleanup
   ```

### Debug Mode

For detailed debugging, you can modify the CLI to add verbose logging:

```python
# Add to your development environment
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Best Practices

### Development
1. **Use interactive mode** for exploration and testing
2. **Test with smaller models** first (gpt2-medium)
3. **Use JSON output** for automated testing
4. **Monitor vector store usage** regularly

### Testing
1. **Run performance tests** before and after changes
2. **Use consistent test questions** for comparison
3. **Save benchmark results** for tracking improvements
4. **Test with multiple chapters** to ensure robustness

### Production
1. **Use larger models** for better quality (gpt2-large)
2. **Monitor response times** and quality
3. **Regular cleanup** of old vector stores
4. **Backup important collections** before cleanup

## 🎯 Integration Examples

### CI/CD Pipeline
```yaml
# Example GitHub Actions step
- name: Test RAG System
  run: |
    python -m llmrag.cli test performance --chapter wg1/chapter04
    python -m llmrag.cli test quality --chapter wg1/chapter04
    python -m llmrag.cli benchmark --chapters wg1/chapter04 --output results.json
```

### Monitoring Dashboard
```python
# Example: Collect metrics
import subprocess
import json

def get_rag_metrics():
    result = subprocess.run([
        'python', '-m', 'llmrag.cli', 'ask', 
        'What are climate scenarios?', 
        '--chapter', 'wg1/chapter04',
        '--output-format', 'json'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)
```

---

**Ready for Development!** 🚀

The CLI provides all the tools you need for efficient development, testing, and monitoring of the LLM-RAG system. 