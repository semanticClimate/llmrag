from llmrag.models.transformers_model import TransformersModel
from llmrag.models.fake_llm import FakeLLM

def load_model(config):
    """
    Load a model based on configuration.
    
    Args:
        config: Either a string (model type) or dict (model config)
        
    Returns:
        Model instance
    """
    if isinstance(config, str):
        # Handle string config (e.g., "fake_llm")
        if config == "fake_llm":
            return FakeLLM()
        else:
            # Assume it's a model name for TransformersModel
            return TransformersModel(model_name=config, device="cpu")
    else:
        # Handle dict config
        return TransformersModel(
            model_name=config.get("model_name", "gpt2-large"),
            device=config.get("device", "cpu")
        )
