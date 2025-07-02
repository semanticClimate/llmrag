# Installation Optimization Guide

## 🚨 Problem: Slow Installation on Windows 11 + Python 3.12

**Issue**: `pip install -e .` taking 30+ minutes on Windows 11 with Python 3.12

## 🔍 Root Causes

### 1. Heavy Dependencies
- **transformers**: ~2GB+ library with model downloads
- **sentence-transformers**: Downloads models during installation
- **spacy**: Large NLP library requiring compilation
- **chromadb**: Can be slow to compile on Windows

### 2. Windows-Specific Issues
- **Compilation**: Windows compilation is slower than Linux/Mac
- **Wheels**: Some packages lack pre-compiled wheels for Python 3.12
- **Dependencies**: Complex dependency resolution on Windows

### 3. Installation Strategy Issues
- **Multiple requirements files**: Confusion between `requirements.txt` and `pipeline_requirements.txt`
- **No optimization flags**: Missing pip optimization settings

## 🚀 Optimized Installation Strategies

### Strategy 1: Staged Installation (Recommended)

```bash
# Step 1: Install core dependencies first (fast)
pip install --no-deps -e .

# Step 2: Install light dependencies
pip install pyyaml lxml pytest rich streamlit toml

# Step 3: Install medium dependencies
pip install chromadb langchain

# Step 4: Install heavy dependencies last
pip install transformers sentence-transformers
```

### Strategy 2: Use Pre-compiled Wheels

```bash
# Use wheels when available (much faster)
pip install --only-binary=all -e .

# Or install specific packages with wheels
pip install --only-binary=all transformers sentence-transformers
```

### Strategy 3: Optimize pip Settings

```bash
# Use multiple workers for parallel downloads
pip install --use-feature=fast-deps -e .

# Or set environment variable
export PIP_USE_PEP517=1
pip install -e .
```

### Strategy 4: Windows-Specific Optimizations

```bash
# Use conda for heavy packages (often faster on Windows)
conda install -c conda-forge transformers sentence-transformers
pip install -e .

# Or use mamba (faster conda alternative)
mamba install -c conda-forge transformers sentence-transformers
pip install -e .
```

## 📦 Dependency Analysis

### Fast Dependencies (< 1 minute)
- `pyyaml` - Small, pure Python
- `lxml` - Usually has wheels
- `pytest` - Small testing framework
- `rich` - Pure Python
- `streamlit` - Usually has wheels
- `toml` - Pure Python

### Medium Dependencies (1-5 minutes)
- `chromadb` - Can be slow to compile
- `langchain` - Moderate size
- `coverage` - Small but may compile

### Slow Dependencies (5-30+ minutes)
- `transformers` - Very large, downloads models
- `sentence-transformers` - Downloads models during install
- `spacy` - Large NLP library

## 🛠️ Recommended Solutions

### For Windows Users (Immediate Fix)

```bash
# 1. Create optimized requirements file
pip install --upgrade pip setuptools wheel

# 2. Install with optimization flags
pip install --use-feature=fast-deps --only-binary=all -e .

# 3. If still slow, use staged approach
pip install pyyaml lxml pytest rich streamlit toml
pip install chromadb langchain
pip install transformers sentence-transformers
```

### For Development Team

```bash
# Create a fast-install script
# install_fast.bat (Windows)
@echo off
echo Installing LLMRAG with optimized settings...
pip install --upgrade pip setuptools wheel
pip install --use-feature=fast-deps --only-binary=all -e .
echo Installation complete!
```

### For CI/CD Pipeline

```yaml
# .github/workflows/install.yml
- name: Install dependencies
  run: |
    pip install --upgrade pip setuptools wheel
    pip install --use-feature=fast-deps --only-binary=all -e .
```

## 📊 Performance Benchmarks

### Expected Times (Windows 11 + Python 3.12)
- **Optimized install**: 5-10 minutes
- **Standard install**: 15-30 minutes
- **Unoptimized install**: 30+ minutes

### Factors Affecting Speed
- **Internet connection**: Model downloads are large
- **Disk speed**: SSD vs HDD makes big difference
- **CPU cores**: More cores = faster compilation
- **Available RAM**: More RAM = faster processing

## 🔧 Troubleshooting

### Common Issues

1. **Out of Memory**
   ```bash
   # Reduce parallel workers
   pip install --no-cache-dir -e .
   ```

2. **Network Timeouts**
   ```bash
   # Increase timeout
   pip install --timeout 300 -e .
   ```

3. **Compilation Failures**
   ```bash
   # Use pre-compiled wheels only
   pip install --only-binary=all -e .
   ```

### Windows-Specific Issues

1. **Visual Studio Build Tools Missing**
   - Install Visual Studio Build Tools 2019 or later
   - Or use conda/mamba for heavy packages

2. **PATH Issues**
   - Ensure Python and pip are in PATH
   - Use `python -m pip` instead of `pip`

3. **Antivirus Interference**
   - Temporarily disable antivirus during installation
   - Add project directory to antivirus exclusions

## 📝 Action Items

### Immediate (This Session)
- [ ] Create optimized installation script
- [ ] Update documentation with fast install instructions
- [ ] Test installation times on Windows

### Short Term
- [ ] Split requirements into core/optional
- [ ] Create conda environment file
- [ ] Add installation benchmarks to CI

### Long Term
- [ ] Consider lighter alternatives for heavy dependencies
- [ ] Implement lazy loading for models
- [ ] Create Docker image for consistent environments

## 🎯 Success Metrics

- **Target**: < 10 minutes installation time
- **Current**: 30+ minutes (problematic)
- **Optimization Goal**: 5-10 minutes

---

**Next Steps**: Test the optimized installation strategies and create team-friendly installation scripts. 