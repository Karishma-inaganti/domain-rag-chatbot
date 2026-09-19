import streamlit as st
from pathlib import Path

from rag_pipeline import answer_question
from vector_store import create_vector_store


st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Domain-Specific RAG Chatbot")
st.write(
    "Upload PDF documents and ask questions based on their content."
)


# --------------------------------------------------
# PDF UPLOAD SECTION
# --------------------------------------------------

st.sidebar.header("📚 Document Upload")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)


if uploaded_files:

    st.sidebar.write("Uploaded files:")

    valid_files = []

    for uploaded_file in uploaded_files:

        file_size_mb = uploaded_file.size / (1024 * 1024)

        if not uploaded_file.name.lower().endswith(".pdf"):

            st.sidebar.error(
                f"{uploaded_file.name}: Only PDF files are allowed."
            )

        elif file_size_mb > 10:

            st.sidebar.error(
                f"{uploaded_file.name}: File size must be 10 MB or less."
            )

        else:

            valid_files.append(uploaded_file)

            st.sidebar.write(
                f"📄 {uploaded_file.name} "
                f"({file_size_mb:.1f} MB)"
            )

    st.sidebar.write(
        f"Valid files: {len(valid_files)}"
    )

    if valid_files and st.sidebar.button("Process Documents"):

        documents_folder = Path("documents")
        documents_folder.mkdir(exist_ok=True)

        # Remove existing PDF files
        for old_file in documents_folder.glob("*.pdf"):
            old_file.unlink()

        # Save newly uploaded PDFs
        for uploaded_file in valid_files:

            file_path = documents_folder / uploaded_file.name

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

        with st.spinner("Processing documents..."):

            total_chunks, dimension = create_vector_store(
                "documents"
            )

        st.sidebar.success(
            f"Documents processed successfully!\n\n"
            f"Chunks: {total_chunks}\n"
            f"Embedding dimension: {dimension}"
        )


# --------------------------------------------------
# QUESTION SECTION
# --------------------------------------------------

st.subheader("💬 Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: What is artificial intelligence?",
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Searching the documents and generating an answer..."
        ):

            answer, results = answer_question(question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")

        for result in results:

            source = result["metadata"]["source"]
            page = result["metadata"]["page"]
            score = result["score"]

            st.write(
                f"📄 {source} — Page {page} "
                f"(similarity score: {score:.3f})"
            )