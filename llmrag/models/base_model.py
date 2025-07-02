from abc import ABC, abstractmethod

class BaseModel(ABC):
    from abc import ABC, abstractmethod

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a response from a prompt."""
        pass
