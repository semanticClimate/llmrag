@echo off
echo ========================================
echo LLMRAG Fast Installation Script
echo Optimized for Windows 11 + Python 3.12
echo ========================================
echo.

echo [1/5] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip tools
    pause
    exit /b 1
)

echo.
echo [2/5] Installing core dependencies (fast)...
python -m pip install pyyaml lxml pytest rich streamlit toml
if %errorlevel% neq 0 (
    echo ERROR: Failed to install core dependencies
    pause
    exit /b 1
)

echo.
echo [3/5] Installing medium dependencies...
python -m pip install chromadb langchain coverage
if %errorlevel% neq 0 (
    echo ERROR: Failed to install medium dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Installing heavy dependencies (this may take 5-10 minutes)...
echo Installing transformers and sentence-transformers...
python -m pip install --only-binary=all transformers sentence-transformers
if %errorlevel% neq 0 (
    echo ERROR: Failed to install heavy dependencies
    echo Trying alternative approach...
    python -m pip install transformers sentence-transformers
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install heavy dependencies with alternative approach
        pause
        exit /b 1
    )
)

echo.
echo [5/5] Installing LLMRAG in development mode...
python -m pip install -e .
if %errorlevel% neq 0 (
    echo ERROR: Failed to install LLMRAG
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Expected installation time: 5-10 minutes
echo If this took longer, check your internet connection.
echo.
echo To test the installation, run:
echo   python -m pytest tests/ -v
echo.
pause 