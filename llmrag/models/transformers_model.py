from transformers import pipeline
from llmrag.models.base_model import BaseModel
from langchain_core.documents import Document

class TransformersModel(BaseModel):
    """
    Text generation model using Hugging Face Transformers.

    Args:
        model_name (str): The name of the pretrained model to load.
        device (str): Device to run the model on ('cpu' or 'cuda').

    Methods:
        generate(prompt: str, temperature: float) -> str:
            Generates text from a given prompt.
        generate(query: str, documents: list[Document]) -> str:
            Generates text from a query and context documents.
    """

    def __init__(self, model_name="gpt2", device="cpu"):
        device_id = 0 if device == "cuda" else -1
        self.generator = pipeline("text-generation", model=model_name, device=device_id)
        self.device = device

    def generate(self, prompt_or_query: str, temperature: float = 0.7, documents: list[Document] = None) -> str:
        """
        Generate text from a prompt or query with optional context documents.
        
        Args:
            prompt_or_query (str): The prompt or query to generate from
            temperature (float): Sampling temperature for generation
            documents (list[Document], optional): Context documents for RAG-style generation
            
        Returns:
            str: The generated text
        """
        if documents is not None:
            # RAG-style generation with context
            context = "\n\n".join(doc.page_content for doc in documents)
            prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {prompt_or_query}

Answer:"""
        else:
            # Direct prompt generation
            prompt = prompt_or_query

        response = self.generator(
            prompt, 
            max_new_tokens=200,
            temperature=temperature,
            pad_token_id=50256
        )
        return response[0]["generated_text"]
