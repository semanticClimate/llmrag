from transformers import pipeline
from llmrag.models.base_model import BaseModel

class TransformersModel(BaseModel):
    """
    Text generation model using Hugging Face Transformers.

    Args:
        model_name (str): The name of the pretrained model to load.
        device (str): Device to run the model on ('cpu' or 'cuda').

    Methods:
        generate(prompt: str) -> str:
            Generates text from a given prompt.
    """

    def __init__(self, model_name="gpt2", device="cpu"):
        device_id = 0 if device == "cuda" else -1
        self.generator = pipeline("text-generation", model=model_name, device=device_id)


    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        return self.generator(
            prompt,
            max_new_tokens=256,
            temperature=temperature,
            pad_token_id=50256
        )[0]['generated_text']