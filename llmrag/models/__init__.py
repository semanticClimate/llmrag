"""Simple loader function based on config.
"""
from llmrag.models.transformers_model import TransformersModel

def load_model(config):
    model_type = config.get("type", "transformers")
    if model_type == "transformers":
        return TransformersModel(
            model_name=config.get("model_name", "mistralai/Mistral-7B-Instruct-v0.1"),
            device=config.get("device", "cpu")
        )
    else:
        raise NotImplementedError(f"Model type {model_type} not implemented.")