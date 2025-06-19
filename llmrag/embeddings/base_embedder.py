from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts):
        pass
