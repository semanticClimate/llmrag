class RAGPipeline:
    def __init__(self, model, retriever):
        self.model = model
        self.retriever = retriever

    def query(self, question):
        docs = self.retriever.retrieve(question)
        context = "\n".join(docs)
        prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
        return self.model.generate(prompt)
