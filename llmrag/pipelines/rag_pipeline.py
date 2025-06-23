from llmrag.retrievers.chroma_store import ChromaVectorStore
from llmrag.generators.local_generator import LocalGenerator
from langchain.schema import Document

class RAGPipeline:

    def __init__(self, *, model, vector_store):
        """
        Initializes the RAGPipeline with a model and a vector store.

        Args:
            model: An object that implements `generate(prompt: str, temperature: float) -> str`.
            vector_store: An object that implements `retrieve(query: str, top_k: int) -> list[Document]`.

        Raises:
            ValueError: If either `model` or `vector_store` is None.
        """
        if model is None:
            raise ValueError("`model` must be provided and non-None")
        if vector_store is None:
            raise ValueError("`vector_store` must be provided and non-None")

        self.model = model
        self.vector_store = vector_store

    def query(self, question: str, top_k=4, temperature=0.3) -> str:
        docs = self.vector_store.retrieve(question, top_k=top_k)

        # Deduplicate context to reduce redundancy
        seen = set()
        unique_docs = []
        for doc in docs:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_docs.append(doc)

        context = "\n".join(doc.page_content for doc in unique_docs)

        # Clear instruction with delimiter to prevent multiple QA pairs
        prompt = f"""You are a helpful assistant. Use ONLY the following context to answer the user's question.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question: {question}
    Answer:"""

        return self.model.generate(prompt, temperature=temperature)

    def run(self, query: str) -> str:
        """
        Runs the RAG pipeline: retrieves documents and generates an answer.

        Args:
            query: The user query.

        Returns:
            The generated answer string.
        """
        documents = self.vector_store.retrieve(query)
        context = "\n".join(doc.page_content for doc in documents)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        return self.model.generate(prompt)


