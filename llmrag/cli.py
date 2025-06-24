import argparse
from llmrag.ingest_html import ingest_html_file
from llmrag.pipelines.rag_pipeline import RAGPipeline

def run_ingest_html(args):
    ingest_html_file(args.file, args.collection)

def run_retrieve(args):
    pipeline = RAGPipeline(collection_name=args.collection)
    result = pipeline.run(args.query)
    print("\n[Answer]")
    print(result["answer"])
    print("\n[Context]")
    for i, chunk in enumerate(result["context"], 1):
        print(f"\n[{i}] {chunk[:300]}...")

def main():
    parser = argparse.ArgumentParser(description="LLM-RAG CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Ingest HTML
    ingest_parser = subparsers.add_parser("ingest-html", help="Ingest an HTML file into Chroma")
    ingest_parser.add_argument("file", type=str, help="Path to the HTML file")
    ingest_parser.add_argument("--collection", default="html_docs", help="Chroma collection name")
    ingest_parser.set_defaults(func=run_ingest_html)

    # Retrieve
    retrieve_parser = subparsers.add_parser("retrieve", help="Query the pipeline and retrieve context")
    retrieve_parser.add_argument("query", type=str, help="Your query")
    retrieve_parser.add_argument("--collection", default="html_docs", help="Chroma collection name")
    retrieve_parser.set_defaults(func=run_retrieve)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
