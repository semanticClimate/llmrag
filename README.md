# llmrag

LLM-RAG system built by PMR and ChatGPT allowing for flexible usage.

for chat history see 
./project.md and ./all_code.py (Messy)

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

We run on Python 3.12. This can cause problems with some librraies, such as NumPy. Although `numpy` is not included in `llmrag` at present it may be in your environment. *ALWAYS USE A VIRTUAL ENVIRONMENT*

