from llmrag.retrievers.chroma_store import ChromaVectorStore
from llmrag.generators.local_generator import LocalGenerator
from langchain_core.documents import Document
import re

class RAGPipeline:

    def __init__(self, *, model, vector_store):
        """
        Initializes the RAGPipeline with a model and a vector store.

        Args:
            model: An object that implements `generate(prompt: str, temperature: float) -> str`.
            vector_store: An object that implements `retrieve(query: str, top_k: int) -> List[Document]`.

        Raises:
            ValueError: If either `model` or `vector_store` is None.
        """
        if model is None:
            raise ValueError("`model` must be provided and non-None")
        if vector_store is None:
            raise ValueError("`vector_store` must be provided and non-None")

        self.model = model
        self.vector_store = vector_store

    def run(self, query: str, top_k=4, temperature=0.3) -> dict:
        """
        Runs the RAG pipeline: retrieves documents and generates an answer.

        Args:
            query: The user query.
            top_k: Number of documents to retrieve
            temperature: Temperature for generation

        Returns:
            dict: A dictionary containing:
                - answer: The generated answer string
                - context: List of retrieved documents
                - paragraph_ids: List of unique paragraph IDs from the context documents
        """
        documents = self.vector_store.retrieve(query, top_k=top_k)

        # Deduplicate context to reduce redundancy
        seen = set()
        unique_docs = []
        for doc in documents:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_docs.append(doc)

        context = "\n".join(doc.page_content for doc in unique_docs)

        # Check if this is a section-specific query
        section_match = self._extract_section_query(query)
        
        if section_match:
            # Use a more focused prompt for section queries
            prompt = f"""You are a helpful assistant answering questions about specific sections of a document. 
Use ONLY the following context to answer the user's question about section {section_match}.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {query}
Answer:"""
        else:
            # Use the standard prompt for general queries
            prompt = f"""You are a helpful assistant. Use ONLY the following context to answer the user's question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {query}
Answer:"""

        answer = self.model.generate(prompt, temperature=temperature)
        
        # Extract paragraph IDs from the retrieved documents
        paragraph_ids = []
        for doc in unique_docs:
            if hasattr(doc, 'metadata') and doc.metadata:
                if 'paragraph_ids' in doc.metadata and doc.metadata['paragraph_ids']:
                    # Split comma-separated string back into list
                    ids = doc.metadata['paragraph_ids'].split(',')
                    paragraph_ids.extend([id.strip() for id in ids if id.strip()])
        
        # Remove duplicates while preserving order
        unique_paragraph_ids = list(dict.fromkeys(paragraph_ids))
        
        return {
            "answer": answer,
            "context": unique_docs,
            "paragraph_ids": unique_paragraph_ids
        }

    def _extract_section_query(self, query: str) -> str:
        """
        Extract section number from query if present.
        """
        # Look for section numbers in parentheses
        match = re.search(r'\((\d+\.\d+(?:\.\d+)*)\)', query)
        if match:
            return match.group(1)
        
        # Look for section numbers at the beginning or with "section"
        match = re.search(r'(?:section\s+)?(\d+\.\d+(?:\.\d+)*)', query, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None

    def query(self, question: str, top_k=4, temperature=0.3) -> str:
        """
        Legacy method - use run() instead for full results with paragraph IDs.
        """
        result = self.run(question, top_k=top_k, temperature=temperature)
        return result["answer"]

