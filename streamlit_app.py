import streamlit as st
from llmrag.utils.pipeline_setup import (
    load_documents_from_file,
    load_documents_from_dir,
    build_pipeline,
)
from langchain_core.documents import Document

st.set_page_config(page_title="RAG Explorer", layout="wide")

st.title("🔍 RAG Explorer")

# Sidebar Inputs
st.sidebar.header("Configuration")

model_name = st.sidebar.text_input("LLM Model", value="gpt2")
embedding_model = st.sidebar.text_input("Embedding Model", value="all-MiniLM-L6-v2")
vector_store_type = st.sidebar.selectbox("Vector Store", options=["chroma"], index=0)

uploaded_files = st.sidebar.file_uploader("Upload documents", type=["txt", "html", "htm"], accept_multiple_files=True)

build_btn = st.sidebar.button("Build Pipeline")

# Initialize session state
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if build_btn:
    docs: list[Document] = []

    # Convert uploaded files to Document
    for uploaded in uploaded_files:
        content = uploaded.read().decode("utf-8")
        ext = uploaded.name.split(".")[-1]
        docs.append(Document(page_content=content, metadata={"source": uploaded.name, "format": ext}))

    st.session_state.pipeline = build_pipeline(
        model_name=model_name,
        embedding_model=embedding_model,
        vector_store_type=vector_store_type,
        documents=docs
    )
    st.success("✅ Pipeline built successfully.")

# User Query Section
if st.session_state.pipeline:
    st.subheader("Ask a question")
    user_query = st.text_input("Enter your query")
    if st.button("Run"):
        with st.spinner("Generating answer..."):
            answer = st.session_state.pipeline.query(user_query)
        st.markdown("### 📤 Answer")
        st.success(answer)
