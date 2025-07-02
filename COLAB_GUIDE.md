# 🌐 Google Colab Setup Guide

**Running the IPCC RAG System on Google Colab**

## 🚀 Quick Setup (5 minutes)

### Step 1: Enable GPU (Recommended)
```python
# In Colab, go to: Runtime → Change runtime type → GPU
# This will significantly speed up model inference
```

### Step 2: Install Dependencies
```python
!pip install -r requirements.txt
!pip install -q streamlit
```

### Step 3: Clone Repository
```python
!git clone https://github.com/yourusername/llmrag.git
%cd llmrag
```

### Step 4: Download IPCC Data
```python
# You'll need to upload IPCC HTML files to Colab
# Or download them from a public source
!mkdir -p tests/ipcc/wg1/chapter02
# Upload your HTML files to this directory
```

## ⚡ Colab-Optimized Configuration

### **Recommended Model Settings:**
```python
# Use smaller model for faster inference
model_config = {
    "model_name": "gpt2",  # Smaller than gpt2-large
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}

# Reduce chunk size for memory efficiency
chunk_size = 300  # Instead of 500
```

### **Memory Optimization:**
```python
import gc
import torch

# Clear GPU memory between operations
def clear_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# Use after loading chapters
clear_memory()
```

## 📊 Performance Expectations

### **Free Tier Colab:**
- **Setup time**: 5-10 minutes
- **Question response**: 15-30 seconds
- **Memory usage**: ~8GB peak
- **Session limit**: 12 hours

### **Pro Tier Colab:**
- **Setup time**: 3-5 minutes
- **Question response**: 5-15 seconds
- **Memory usage**: ~12GB peak
- **Session limit**: 12 hours

## 🔧 Colab-Specific Code

### **Streamlit in Colab:**
```python
# Install streamlit
!pip install -q streamlit

# Run streamlit with colab-specific settings
!streamlit run streamlit_app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

# Use ngrok to access from browser
!pip install -q pyngrok
from pyngrok import ngrok
public_url = ngrok.connect(port=8501)
print(f"Access your app at: {public_url}")
```

### **Alternative: Direct Python Interface**
```python
from llmrag.chapter_rag import ask_chapter

# Load chapter once
print("Loading chapter...")
# This will take 30-60 seconds

# Ask questions
question = "What are the main findings about temperature trends?"
result = ask_chapter(question, "wg1/chapter02")
print(f"Answer: {result['answer']}")
print(f"Sources: {result['paragraph_ids']}")
```

## ⚠️ Important Limitations

### **Session Management:**
- **Save your work** frequently
- **Download results** before session ends
- **Use persistent storage** for models (they cache between sessions)

### **Memory Management:**
- **Close unused tabs** in Colab
- **Restart runtime** if memory gets full
- **Use smaller models** if needed

### **Network Issues:**
- **Model downloads** can fail - retry if needed
- **Large files** may timeout - use smaller chunks
- **Connection drops** - save progress frequently

## 🎯 Recommended Workflow

### **For Research:**
1. **Start fresh session** with GPU enabled
2. **Load one chapter** at a time
3. **Ask multiple questions** in one session
4. **Export results** to Google Drive
5. **Save model cache** for next session

### **For Teaching:**
1. **Pre-load models** in a separate session
2. **Create demo notebook** with pre-loaded data
3. **Use smaller models** for faster responses
4. **Prepare example questions** in advance

## 💾 Data Persistence

### **Save Models Locally:**
```python
# Models are cached in ~/.cache/huggingface/
# They persist between Colab sessions
# No need to re-download each time
```

### **Save Results:**
```python
import json
from google.colab import files

# Save results to file
results = {
    "question": "What causes global warming?",
    "answer": result['answer'],
    "sources": result['paragraph_ids']
}

with open('results.json', 'w') as f:
    json.dump(results, f)

# Download to your computer
files.download('results.json')
```

## 🚨 Troubleshooting

### **Out of Memory:**
```python
# Restart runtime and try again
# Use smaller models
# Reduce batch sizes
```

### **Model Download Fails:**
```python
# Check internet connection
# Try again in a few minutes
# Use alternative model
```

### **Session Disconnects:**
```python
# Save work frequently
# Use persistent storage
# Reconnect and reload
```

## 📈 Performance Tips

### **For Faster Responses:**
- **Use GPU runtime**
- **Pre-load chapters**
- **Ask multiple questions** in one session
- **Use smaller models** if speed is critical

### **For Better Answers:**
- **Use gpt2-large** if memory allows
- **Increase chunk size** for more context
- **Ask specific questions**
- **Check source paragraphs**

---

**Happy researching on Colab! 🌍📚** 