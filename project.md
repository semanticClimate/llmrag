llmrag/
├── __init__.py
├── main.py
├── chunking/
│   ├── __init__.py
│   └── text_splitter.py
├── embeddings/
│   ├── __init__.py
│   ├── base_embedder.py
│   └── sentence_transformers_embedder.py
├── models/
│   ├── __init__.py
│   ├── base_model.py
│   └── transformers_model.py
├── pipelines/
│   ├── __init__.py
│   └── rag_pipeline.py
├── retrievers/
│   ├── __init__.py
│   ├── base_vector_store.py
│   └── chroma_store.py
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py
│   ├── test_embedding.py
│   ├── test_model.py
│   ├── test_retriever.py
│   └── test_chunking.py
├── data/
│   ├── __init__.py
│   └── test_data.yaml
├── configs/
│   ├── __init__.py
│   └── default.yaml
├── requirements.txt
├── pyproject.toml
└── .github/
    └── workflows/
        └── ci.yml
