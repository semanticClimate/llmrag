"""
Loads a Hugging Face Transformers model for local generation.
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from llmrag.models.base_model import BaseModel

class TransformersModel(BaseModel):
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1", device: str = "cpu"):
        print(f"Loading model: {model_name} on {device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto" if device != "cpu" else None,
            torch_dtype="auto"
        )
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if device == "cuda" else -1)

    def generate(self, prompt: str) -> str:
        result = self.pipeline(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)
        return result[0]["generated_text"][len(prompt):].strip()