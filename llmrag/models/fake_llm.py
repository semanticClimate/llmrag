from typing import List
from langchain_core.documents import Document

class FakeLLM:
    """
    A fake LLM for testing purposes that returns mock responses.
    """

    def __init__(self):
        pass

    def generate(self, prompt_or_query: str, temperature: float = 0.3, documents: List[Document] = None) -> str:
        """
        Generate a fake response for testing.
        
        Args:
            prompt_or_query (str): The prompt or query
            temperature (float): Temperature parameter (ignored in fake model)
            documents (List[Document], optional): Context documents (ignored in fake model)
            
        Returns:
            str: A mock response
        """
        # Simple fake model for testing
        return f"Mock answer to: {prompt_or_query.split('Question:')[-1].strip() if 'Question:' in prompt_or_query else prompt_or_query}"
