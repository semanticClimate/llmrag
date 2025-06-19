
### `base_model.py`

from abc import ABC, abstractmethod

"""
Defines a clean interface for all language models.

"""
class BaseModel(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Given a prompt, return a generated response.
        """
        pass

