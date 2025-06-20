import streamlit as st
from llmrag.pipelines.rag_pipeline import RAGPipeline


# Initialize pipeline
@st.cache_resource
def load_pipeline():
    return RAGPipeline()


st.title("🧠 LLM-RAG Q&A")
st.write("Ask a question based on your vector store!")

# Input question
question = st.text_input("Enter your question:")

# Show docs toggle
show_docs = st.checkbox("Show retrieved context", value=False)

# Answer button
if st.button("Get Answer") and question:
    pipeline = load_pipeline()
    docs = pipeline.retriever.retrieve(question)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""Use the following context to answer the question:
{context}

Question: {question}
Answer:"""

    answer = pipeline.generator.generate(prompt)

    st.subheader("Answer")
    st.success(answer)

    if show_docs:
        st.subheader("Retrieved Context")
        for i, doc in enumerate(docs):
            st.markdown(f"**Chunk {i + 1}:** {doc.page_content}")