from llmrag.models.transformers_model import TransformersModel

def load_model(config):
    return TransformersModel(
        model_name=config.get("model_name", "gpt2"),
        device=config.get("device", "cpu")
    )
