from transformers import pipeline
from llmrag.models.base_model import BaseModel

class TransformersModel(BaseModel):
    def __init__(self, model_name="gpt2", device="cpu"):
        device_id = 0 if device == "cuda" else -1
        self.generator = pipeline("text-generation", model=model_name, device=device_id)

    def generate(self, prompt):
        return self.generator(prompt, max_length=200)[0]['generated_text']
