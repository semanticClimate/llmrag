class FakeLLM:

    def __init__(self):
        pass

    def generate(self, query: str, documents: list) -> dict:
        context = [doc.page_content for doc in documents]
        answer = f"[FAKE ANSWER] This is a dummy answer to: '{query}'"
        return {
            "answer": answer,
            "context": context
        }
