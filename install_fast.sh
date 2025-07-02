#!/bin/bash

echo "========================================"
echo "LLMRAG Fast Installation Script"
echo "Optimized for Unix/Linux systems"
echo "========================================"
echo

echo "[1/5] Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip tools"
    exit 1
fi

echo
echo "[2/5] Installing core dependencies (fast)..."
python3 -m pip install pyyaml lxml pytest rich streamlit toml
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install core dependencies"
    exit 1
fi

echo
echo "[3/5] Installing medium dependencies..."
python3 -m pip install chromadb langchain coverage
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install medium dependencies"
    exit 1
fi

echo
echo "[4/5] Installing heavy dependencies (this may take 5-10 minutes)..."
echo "Installing transformers and sentence-transformers..."
python3 -m pip install --only-binary=all transformers sentence-transformers
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install heavy dependencies"
    echo "Trying alternative approach..."
    python3 -m pip install transformers sentence-transformers
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install heavy dependencies with alternative approach"
        exit 1
    fi
fi

echo
echo "[5/5] Installing LLMRAG in development mode..."
python3 -m pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install LLMRAG"
    exit 1
fi

echo
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo
echo "Expected installation time: 5-10 minutes"
echo "If this took longer, check your internet connection."
echo
echo "To test the installation, run:"
echo "  python3 -m pytest tests/ -v" 