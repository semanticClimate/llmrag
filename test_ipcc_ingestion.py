#!/usr/bin/env python3
"""
Test script for ingesting IPCC HTML content with paragraph IDs and testing RAG pipeline.
"""

import os
import platform
from pathlib import Path
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.embeddings import SentenceTransformersEmbedder
from llmrag.retrievers import ChromaVectorStore
from llmrag.models.fake_llm import FakeLLM
from llmrag.pipelines.rag_pipeline import RAGPipeline

def test_ipcc_ingestion():
    """Test ingestion of IPCC HTML file and RAG pipeline with paragraph IDs."""
    # Normalize path for cross-platform compatibility
    html_file = Path("tests/ipcc/wg1/chapter04/html_with_ids.html").as_posix()
    
    if platform.system() == "Windows":
        html_file = html_file.replace("/", "\\")  # Adjust for Windows if needed
    
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found at {html_file}")
        return
    
    collection_name = "ipcc_chapter4_test"
    
    print(f"Testing ingestion of {html_file}")
    print(f"Collection name: {collection_name}")
    print("-" * 50)
    
    # Step 1: Ingest the HTML file
    try:
        ingest_html_file(html_file, collection_name=collection_name)
        print("✅ HTML ingestion completed successfully")
    except Exception as e:
        print(f"❌ HTML ingestion failed: {e}")
        return
    
    # Step 2: Set up RAG pipeline
    try:
        embedder = SentenceTransformersEmbedder()
        retriever = ChromaVectorStore(embedder=embedder, collection_name=collection_name)
        llm = FakeLLM()
        pipeline = RAGPipeline(vector_store=retriever, model=llm)
        print("✅ RAG pipeline setup completed")
    except Exception as e:
        print(f"❌ RAG pipeline setup failed: {e}")
        return
    
    # Step 3: Test queries
    test_queries = [
        "What are the main scenarios used in climate projections?",
        "What is the difference between CMIP5 and CMIP6?",
        "How do climate models handle uncertainty?",
        "What are the projected temperature changes by 2100?"
    ]
    
    print("\n" + "=" * 50)
    print("TESTING QUERIES")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 30)
        
        try:
            result = pipeline.run(query)
            
            print(f"Answer: {result['answer']}")
            print(f"Number of context documents: {len(result['context'])}")
            
            # Check if any documents have paragraph IDs in metadata
            paragraph_ids = []
            for doc in result['context']:
                if hasattr(doc, 'metadata') and doc.metadata:
                    # Look for paragraph ID in metadata
                    for key, value in doc.metadata.items():
                        if 'id' in key.lower() or 'paragraph' in key.lower():
                            paragraph_ids.append(value)
                        elif isinstance(value, str) and ('_p' in value or 'paragraph' in value.lower()):
                            paragraph_ids.append(value)
            
            if paragraph_ids:
                print(f"Paragraph IDs found: {paragraph_ids}")
            else:
                print("No paragraph IDs found in context documents")
                # Let's check what metadata is actually available
                if result['context']:
                    print(f"Available metadata keys: {list(result['context'][0].metadata.keys())}")
            
        except Exception as e:
            print(f"❌ Query failed: {e}")

if __name__ == "__main__":
    test_ipcc_ingestion()