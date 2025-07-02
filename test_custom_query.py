#!/usr/bin/env python3
"""
Interactive test script for custom queries using the RAG pipeline.
"""

import os
from llmrag.ingestion.ingest_html import ingest_html_file
from llmrag.embeddings import SentenceTransformersEmbedder
from llmrag.retrievers import ChromaVectorStore
from llmrag.models.fake_llm import FakeLLM
from llmrag.pipelines.rag_pipeline import RAGPipeline

def setup_pipeline():
    """Set up the RAG pipeline with IPCC data."""
    html_file = "tests/ipcc/wg1/chapter04/html_with_ids.html"
    collection_name = "ipcc_chapter4_custom"
    
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found at {html_file}")
        return None
    
    print("Setting up RAG pipeline...")
    
    # Ingest the HTML file
    try:
        ingest_html_file(html_file, collection_name=collection_name)
        print("✅ HTML ingestion completed")
    except Exception as e:
        print(f"❌ HTML ingestion failed: {e}")
        return None
    
    # Set up the pipeline
    try:
        embedder = SentenceTransformersEmbedder()
        retriever = ChromaVectorStore(embedder=embedder, collection_name=collection_name)
        llm = FakeLLM()
        pipeline = RAGPipeline(vector_store=retriever, model=llm)
        print("✅ RAG pipeline setup completed")
        return pipeline
    except Exception as e:
        print(f"❌ Pipeline setup failed: {e}")
        return None

def test_query(pipeline, query):
    """Test a single query and display results."""
    print(f"\n🔍 Query: {query}")
    print("-" * 50)
    
    try:
        result = pipeline.run(query)
        
        print(f"📝 Answer: {result['answer']}")
        print(f"📊 Number of context documents: {len(result['context'])}")
        
        if result['paragraph_ids']:
            print(f"🏷️  Paragraph IDs: {result['paragraph_ids']}")
        else:
            print("🏷️  No paragraph IDs found")
        
        # Show a preview of the context documents
        print("\n📄 Context Preview:")
        for i, doc in enumerate(result['context'][:2], 1):  # Show first 2 docs
            preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            print(f"  {i}. {preview}")
        
        if len(result['context']) > 2:
            print(f"  ... and {len(result['context']) - 2} more documents")
            
    except Exception as e:
        print(f"❌ Query failed: {e}")

def interactive_mode():
    """Run interactive query testing."""
    pipeline = setup_pipeline()
    if not pipeline:
        return
    
    print("\n" + "=" * 60)
    print("🎯 INTERACTIVE QUERY TESTING")
    print("=" * 60)
    print("Type your queries about climate change, IPCC scenarios, etc.")
    print("Type 'quit' or 'exit' to stop")
    print("Type 'help' for example queries")
    print("-" * 60)
    
    example_queries = [
        "What are the main climate scenarios used in IPCC projections?",
        "How do CMIP6 models differ from CMIP5?",
        "What is the projected temperature increase by 2100?",
        "How do climate models handle uncertainty?",
        "What are the Shared Socioeconomic Pathways?",
        "How does the Arctic sea ice change in projections?",
        "What is the difference between near-term and long-term projections?"
    ]
    
    while True:
        try:
            query = input("\n❓ Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif query.lower() == 'help':
                print("\n💡 Example queries:")
                for i, example in enumerate(example_queries, 1):
                    print(f"  {i}. {example}")
                continue
            elif not query:
                print("Please enter a query or type 'help' for examples")
                continue
            
            test_query(pipeline, query)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_mode() 