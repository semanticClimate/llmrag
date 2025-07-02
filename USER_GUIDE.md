# 📖 IPCC RAG System - User Guide

**A friendly guide to using the IPCC RAG system for climate research**

## 🎯 Who is this guide for?

This guide is designed for:
- **Researchers** who want to quickly find information in IPCC reports
- **Students** learning about climate science
- **Policymakers** who need accurate climate information
- **Anyone** interested in understanding climate change better

**No technical knowledge required!** 🎉

## 🚀 Getting Started (5 minutes)

### Step 1: Install Python
**Don't worry if you've never used Python before!**

#### Windows Users:
1. Go to [python.org](https://www.python.org/downloads/)
2. Click "Download Python" (get the latest version)
3. Run the installer
4. **Important**: Check "Add Python to PATH" during installation

#### Mac Users:
1. Open Terminal (press Cmd+Space, type "Terminal")
2. Type: `python3 --version`
3. If you see a version number, you're good!
4. If not, install with: `brew install python3`

#### Linux Users:
1. Open Terminal
2. Type: `sudo apt install python3 python3-pip`
3. Press Enter and wait for installation

### Step 2: Download the System
1. Go to the [GitHub repository](https://github.com/yourusername/llmrag)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder on your computer

### Step 3: Install Dependencies
1. Open Terminal/Command Prompt
2. Navigate to the downloaded folder:
   ```bash
   cd path/to/llmrag
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Start Using!
```bash
streamlit run streamlit_app.py
```

Your browser will open automatically to the web interface!

## 🎮 How to Use the Web Interface

### First Time Setup
1. **Select a Chapter**: Choose from the dropdown menu
   - `wg1/chapter02` = Changing State of the Climate System
   - `wg1/chapter04` = Future Global Climate
   - More chapters available!

2. **Load the Chapter**: Click "Load Chapter"
   - This might take 30-60 seconds the first time
   - The system is downloading and processing the content

3. **Start Asking Questions**: Type your question and press Enter!

### Example Questions to Try
- "What are the main findings about temperature trends?"
- "How much has the Earth warmed since pre-industrial times?"
- "What are the projected impacts of climate change?"
- "What causes global warming?"
- "How confident are scientists about climate change?"

### Understanding the Answers
Each answer includes:
- **The response**: A clear, scientific explanation
- **Source paragraphs**: The exact paragraphs from the IPCC report
- **Confidence level**: How certain the system is about the answer

## 💻 Using the Command Line (Advanced Users)

If you prefer typing commands:

### List Available Chapters
```bash
python -m llmrag.cli list-chapters
```

### Ask a Question
```bash
python -m llmrag.cli ask "What causes global warming?" --chapter wg1/chapter02
```

### Interactive Mode
```bash
python -m llmrag.cli interactive --chapter wg1/chapter02
```

## 🔍 Understanding the Technology

### What is RAG?
**RAG** = Retrieval-Augmented Generation

Think of it like a **super-smart research assistant**:
1. **You ask a question** → "What causes global warming?"
2. **System searches** through IPCC reports for relevant information
3. **System finds** the most relevant paragraphs
4. **System creates** a clear answer based on those paragraphs
5. **System shows you** exactly where the information came from

### Why is this useful?
- **Fast**: Get answers in seconds instead of hours
- **Accurate**: Based on official IPCC reports
- **Transparent**: See exactly where information comes from
- **Local**: Runs on your computer, no internet needed after setup

## 📚 Learning More About Climate Science

### Understanding IPCC Reports
- **WG1**: Physical Science Basis (how climate works)
- **WG2**: Impacts, Adaptation, and Vulnerability (effects on people)
- **WG3**: Mitigation (how to reduce emissions)

### Key Climate Concepts
- **Global Warming**: Increase in Earth's average temperature
- **Climate Change**: Long-term changes in weather patterns
- **Greenhouse Gases**: Gases that trap heat (CO2, methane, etc.)
- **Mitigation**: Actions to reduce greenhouse gas emissions
- **Adaptation**: Actions to prepare for climate impacts

### Recommended Reading
- [IPCC FAQ](https://www.ipcc.ch/about/faq/) - Official IPCC explanations
- [NASA Climate Change](https://climate.nasa.gov/) - Easy-to-understand explanations
- [NOAA Climate.gov](https://www.climate.gov/) - US government climate information

## 🛠️ Troubleshooting

### Common Issues

#### "Python not found"
- **Solution**: Make sure Python is installed and added to PATH
- **Windows**: Reinstall Python and check "Add to PATH"
- **Mac/Linux**: Try `python3` instead of `python`

#### "Module not found" errors
- **Solution**: Install requirements again:
  ```bash
  pip install -r requirements.txt
  ```

#### "Port already in use"
- **Solution**: Close other applications or use a different port:
  ```bash
  streamlit run streamlit_app.py --server.port 8502
  ```

#### Slow performance
- **Solution**: 
  - Close other applications
  - Make sure you have at least 4GB RAM
  - First run is always slower (downloading models)

#### No chapters available
- **Solution**: Make sure you're in the correct directory with the `tests/ipcc` folder

### Getting Help
- **GitHub Issues**: [Report bugs here](https://github.com/yourusername/llmrag/issues)
- **Discussions**: [Ask questions here](https://github.com/yourusername/llmrag/discussions)
- **Email**: your.email@example.com

## 🎯 Best Practices

### Asking Good Questions
- **Be specific**: "What are the impacts on agriculture?" vs "What are the impacts?"
- **Use scientific terms**: "temperature trends" vs "weather changes"
- **Ask follow-up questions**: Build on previous answers

### Understanding Answers
- **Check sources**: Look at the paragraph IDs to verify information
- **Ask for clarification**: If an answer isn't clear, ask a follow-up
- **Cross-reference**: Compare with other chapters or sources

### Research Workflow
1. **Start broad**: Ask general questions about your topic
2. **Narrow down**: Ask more specific questions based on initial answers
3. **Verify sources**: Check the paragraph IDs for accuracy
4. **Take notes**: Save important answers and sources

## 🌍 Contributing to Climate Science

### How You Can Help
- **Test the system**: Try different questions and report issues
- **Share with colleagues**: Help others discover this tool
- **Improve documentation**: Suggest better explanations
- **Report bugs**: Help make the system more reliable

### For Researchers
- **Cite properly**: Use paragraph IDs in your citations
- **Verify information**: Always check against original sources
- **Share findings**: Let us know how you're using the system

## 📞 Support and Community

### Getting Help
- **GitHub Issues**: For bugs and technical problems
- **GitHub Discussions**: For questions and ideas
- **Email**: For private or urgent matters

### Staying Updated
- **Watch the repository**: Get notified of updates
- **Join discussions**: Share your experiences
- **Follow the project**: Stay informed about new features

---

## 🎉 You're Ready!

You now have a powerful tool for climate research at your fingertips. Remember:
- **Start simple**: Try basic questions first
- **Be patient**: The system gets faster with use
- **Explore**: Try different chapters and questions
- **Share**: Help others discover this resource

**Happy researching! 🌍📚**

---

*This guide is part of the IPCC RAG System project. For technical details, see the [README.md](README.md) and [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md).* 