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
        output = self.pipe(
            prompt,
            max_new_tokens=256,
            temperature=temperature,
            pad_token_id=50256,
            do_sample=True,
            return_full_text=False  # Only get the completion, not full prompt
        )

        generated = output[0]["generated_text"].strip()

        # Optional: Cut off any hallucinated QA chaining
        for stop_token in ["\nQuestion:", "\nContext:", "\n\n"]:
            if stop_token in generated:
                generated = generated.split(stop_token)[0].strip()

        return generated
