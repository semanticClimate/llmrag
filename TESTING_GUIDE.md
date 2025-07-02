# 🧪 IPCC RAG System - Testing Guide

**A guide for testing and evaluating the IPCC RAG system**

## 🎯 Purpose

This guide helps you:
- **Test the system** with real climate science questions
- **Evaluate answer quality** and accuracy
- **Check source tracking** (paragraph IDs)
- **Provide feedback** for improvements
- **Share findings** with colleagues

## 🚀 Quick Test (10 minutes)

### Step 1: Start the System
```bash
# Navigate to the project directory
cd llmrag

# Start the web interface
streamlit run streamlit_app.py
```

### Step 2: Load a Chapter
1. Open your browser to `http://localhost:8501`
2. Select `wg1/chapter02` (Changing State of the Climate System)
3. Click "Load Chapter"
4. Wait for the loading message to complete

### Step 3: Test Basic Questions
Try these questions in order:

1. **"What are the main findings about temperature trends?"**
   - Should get a detailed answer about global temperature changes
   - Check that paragraph IDs are shown

2. **"How much has the Earth warmed since pre-industrial times?"**
   - Should mention specific temperature increases
   - Look for numerical values and confidence levels

3. **"What causes global warming?"**
   - Should mention greenhouse gases, human activities
   - Check for scientific terminology

## 📋 Comprehensive Testing Checklist

### ✅ System Functionality
- [ ] Web interface loads without errors
- [ ] Chapter selection works
- [ ] Questions generate responses
- [ ] Paragraph IDs are displayed
- [ ] No error messages appear

### ✅ Answer Quality
- [ ] Answers are coherent and readable
- [ ] Information is scientifically accurate
- [ ] Responses are relevant to questions
- [ ] No repetitive or nonsensical text
- [ ] Technical terms are used appropriately

### ✅ Source Tracking
- [ ] Paragraph IDs are shown with answers
- [ ] IDs correspond to actual content
- [ ] Multiple sources are cited when relevant
- [ ] Source information is helpful for verification

### ✅ Performance
- [ ] First question takes <60 seconds
- [ ] Follow-up questions are faster
- [ ] System remains responsive
- [ ] No memory leaks or crashes

## 🔍 Detailed Testing Scenarios

### Scenario 1: Basic Climate Science
**Questions to test:**
- "What is climate change?"
- "What are greenhouse gases?"
- "How do scientists measure temperature?"

**What to look for:**
- Clear, accurate definitions
- Scientific terminology
- Proper source citations

### Scenario 2: Specific Data and Trends
**Questions to test:**
- "What is the current global temperature?"
- "How fast is the Arctic warming?"
- "What are the temperature projections for 2100?"

**What to look for:**
- Specific numerical values
- Units of measurement
- Confidence intervals
- Time periods mentioned

### Scenario 3: Complex Relationships
**Questions to test:**
- "How does climate change affect extreme weather?"
- "What is the relationship between CO2 and temperature?"
- "How do feedback loops work in climate systems?"

**What to look for:**
- Clear explanations of relationships
- Scientific mechanisms
- Multiple factors considered

### Scenario 4: Uncertainty and Confidence
**Questions to test:**
- "How certain are scientists about climate change?"
- "What are the uncertainties in climate projections?"
- "Which climate impacts are most uncertain?"

**What to look for:**
- Discussion of confidence levels
- Acknowledgment of uncertainties
- Nuanced language about certainty

## 📊 Evaluation Criteria

### Answer Quality (1-5 scale)
- **5**: Excellent - Clear, accurate, comprehensive
- **4**: Good - Mostly accurate, some minor issues
- **3**: Adequate - Generally correct, some confusion
- **2**: Poor - Significant errors or confusion
- **1**: Very Poor - Inaccurate or nonsensical

### Source Tracking (1-5 scale)
- **5**: Excellent - Clear, relevant sources
- **4**: Good - Sources provided, mostly relevant
- **3**: Adequate - Some sources, not always helpful
- **2**: Poor - Sources unclear or irrelevant
- **1**: Very Poor - No sources or misleading sources

### System Performance (1-5 scale)
- **5**: Excellent - Fast, reliable, smooth
- **4**: Good - Generally fast, occasional delays
- **3**: Adequate - Acceptable speed, some issues
- **2**: Poor - Slow, frequent problems
- **1**: Very Poor - Very slow or crashes

## 📝 Test Questions by Category

### Temperature and Warming
- "What is the global average temperature?"
- "How much has the Earth warmed?"
- "What are the temperature trends?"
- "How do scientists measure global temperature?"

### Causes and Mechanisms
- "What causes global warming?"
- "How do greenhouse gases work?"
- "What are the main sources of CO2?"
- "How do human activities affect climate?"

### Impacts and Effects
- "What are the impacts of climate change?"
- "How does climate change affect weather?"
- "What are the effects on ecosystems?"
- "How does climate change affect humans?"

### Projections and Future
- "What are the future climate projections?"
- "How will temperatures change by 2100?"
- "What are the different emission scenarios?"
- "How certain are these projections?"

### Scientific Process
- "How do scientists study climate change?"
- "What is the evidence for climate change?"
- "How confident are scientists?"
- "What are the uncertainties?"

## 🔧 Troubleshooting

### Common Issues

#### System won't start
- **Check**: Python is installed (`python --version`)
- **Check**: Dependencies are installed (`pip install -r requirements.txt`)
- **Check**: Port 8501 is available

#### No chapters available
- **Check**: You're in the correct directory
- **Check**: `tests/ipcc/` folder exists
- **Check**: HTML files are present in chapter folders

#### Slow performance
- **Check**: Close other applications
- **Check**: At least 4GB RAM available
- **Check**: First run is always slower (downloading models)

#### Poor answer quality
- **Check**: Chapter is fully loaded
- **Check**: Question is clear and specific
- **Check**: Try rephrasing the question

## 📊 Recording Results

### Test Session Template
```
Date: _______________
Tester: _____________
System Version: _______

Chapter Tested: _______
Questions Asked: ______

Answer Quality Scores:
- Q1: ___/5
- Q2: ___/5
- Q3: ___/5

Source Tracking Scores:
- Q1: ___/5
- Q2: ___/5
- Q3: ___/5

Performance: ___/5

Issues Found:
- ________________
- ________________

Suggestions:
- ________________
- ________________

Overall Rating: ___/5
```

## 📤 Providing Feedback

### What to Include
1. **Specific questions** you tested
2. **Quality scores** for each question
3. **Issues encountered** (with screenshots if possible)
4. **Suggestions for improvement**
5. **Overall assessment**

### How to Submit
- **GitHub Issues**: For bugs and technical problems
- **GitHub Discussions**: For general feedback and suggestions
- **Email**: For private or detailed feedback

### Example Feedback
```
I tested the system with wg1/chapter02 and found:

Good:
- Clear answers about temperature trends
- Good source tracking with paragraph IDs
- Fast response times after initial load

Issues:
- One answer about CO2 was confusing
- Paragraph ID "executive_summary_p15" wasn't very helpful
- System was slow on first question (45 seconds)

Suggestions:
- Add more context to paragraph IDs
- Improve answer clarity for technical topics
- Add loading progress indicator

Overall: 4/5 - Very useful tool with room for improvement
```

## 🎯 Next Steps

After testing:
1. **Share your findings** with the development team
2. **Discuss with colleagues** who might use the system
3. **Suggest additional test cases** based on your expertise
4. **Consider contributing** to the project if you're interested

---

**Thank you for helping improve the IPCC RAG system! 🌍📚** 