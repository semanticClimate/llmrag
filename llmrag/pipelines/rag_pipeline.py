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
        # Check if this is an Executive Summary query
        if self._is_executive_summary_query(query):
            # Use fewer documents and focus on executive summary content
            documents = self.vector_store.retrieve(query + " executive summary", top_k=2)
        else:
            documents = self.vector_store.retrieve(query, top_k=top_k)

        # Deduplicate context to reduce redundancy
        seen = set()
        unique_docs = []
        for doc in documents:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_docs.append(doc)

        context = "\n\n".join(doc.page_content for doc in unique_docs)

        # Check if this is a section-specific query
        section_match = self._extract_section_query(query)
        
        if section_match:
            # Use a focused prompt for section queries
            prompt = self._create_section_prompt(context, query, section_match)
        elif self._is_executive_summary_query(query):
            # Use a focused prompt for executive summary queries
            prompt = self._create_executive_summary_prompt(context, query)
        else:
            # Use the enhanced scientific prompt for general queries
            prompt = self._create_scientific_prompt(context, query)

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

    def _create_scientific_prompt(self, context: str, query: str) -> str:
        """
        Create a sophisticated prompt optimized for scientific IPCC content.
        """
        return f"""You are a climate science expert analyzing IPCC reports. Provide accurate, evidence-based answers using ONLY the provided context.

Guidelines:
- Base your answer ONLY on the provided context
- Be precise and scientific with technical terminology
- Cite specific data and findings when available
- Acknowledge uncertainty and confidence levels
- If context is insufficient, say so clearly
- Structure your response with key points and evidence
- Be specific about what the IPCC report actually states

Context:
{context}

Question: {query}

Answer:"""

    def _create_section_prompt(self, context: str, query: str, section_number: str) -> str:
        """
        Create a focused prompt for section-specific queries.
        """
        return f"""You are a climate science expert analyzing a specific section ({section_number}) of an IPCC report.
Use ONLY the following context to answer the user's question about this section.

SECTION-SPECIFIC GUIDELINES:
1. **Focus on section {section_number}** - only use information from this specific section
2. **Be precise about what this section covers** - don't generalize beyond the section scope
3. **If the section doesn't address the question**, say "Section {section_number} does not address this question"
4. **Cite specific findings** from this section when available
5. **Maintain scientific accuracy** - use the exact language and data from the section

CONTEXT FROM SECTION {section_number}:
{context}

QUESTION: {query}

ANSWER:"""

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

    def _is_executive_summary_query(self, query: str) -> bool:
        """
        Check if the query is asking about the Executive Summary.
        """
        executive_summary_keywords = [
            'executive summary', 'summary', 'overview', 'main findings',
            'key conclusions', 'main conclusions', 'summary of findings'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in executive_summary_keywords)

    def _create_executive_summary_prompt(self, context: str, query: str) -> str:
        """
        Create a focused prompt for Executive Summary queries.
        """
        return f"""Based on the following context from an IPCC chapter, answer the question about the Executive Summary or main findings.

Context:
{context}

Question: {query}

Answer:"""

    def query(self, question: str, top_k=4, temperature=0.3) -> str:
        """
        Legacy method - use run() instead for full results with paragraph IDs.
        """
        result = self.run(question, top_k=top_k, temperature=temperature)
        return result["answer"]

