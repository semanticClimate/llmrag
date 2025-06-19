from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, docs):
        pass

    @abstractmethod
    def retrieve(self, query):
        pass
