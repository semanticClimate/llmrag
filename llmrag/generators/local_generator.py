from transformers import pipeline

class LocalGenerator:
    """
    Wrapper for local Hugging Face language model generation.

    Args:
        model_name (str): The name of the text generation model to use.

    Methods:
        generate(prompt: str, temperature=0.7) -> str:
            Generates a text response based on the prompt.
    """

    def __init__(self, model_name="gpt2"):
        self.pipe = pipeline("text-generation", model=model_name, device=-1)

    def generate(self, prompt: str, temperature=0.7) -> str:
        """
        Generate a text response based on the provided prompt.

        Args:
            prompt (str): The input prompt.
            temperature (float): Sampling temperature for generation.

        Returns:
            str: The generated answer (post-processed).
        """
        output = self.pipe(
            prompt,
            max_new_tokens=256,
            temperature=temperature,
            pad_token_id=50256,
        )
        return output[0]["generated_text"].split("Answer:")[-1].strip()
