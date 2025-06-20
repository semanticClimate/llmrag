class RAGPipeline:
    def __init__(self, model, retriever):
        self.model = model
        self.retriever = retriever

    def query(self, question):
        docs = self.retriever.retrieve(question)
        context = "\n".join(doc.page_content for doc in docs)
        prompt = f"Answer the question based on the context:\n{context}\n\nQuestion: {question}\nAnswer:"
        return self.model.generate(prompt)

    # def __init__(self, retriever, generator):
    #     self.retriever = retriever
    #     self.generator = generator
    #
    # def query(self, question: str):
    #     docs = self.retriever.retrieve(question)
    #     # Join the page_content strings of the Documents
    #     context = "\n".join(doc.page_content for doc in docs)
    #
    #     # Generate answer using your generator (example)
    #     answer = self.generator.generate(context, question)
    #     return answer