# Domain-Specific RAG Chatbot

## Project Overview

This project is a Domain-Specific Retrieval-Augmented Generation (RAG) Chatbot for the Education domain, focused on Artificial Intelligence.

The chatbot allows users to upload PDF documents and ask questions about their content. It retrieves relevant information from the uploaded documents and uses a Large Language Model to generate an answer based only on the retrieved information.

## Domain

Education → Artificial Intelligence (AI)

## Technologies Used

- Python
- Streamlit
- PyPDF
- LangChain Text Splitters
- Sentence Transformers
- FAISS
- Groq
- python-dotenv

## RAG Workflow

1. User uploads PDF documents.
2. PDF text is extracted page by page.
3. Extracted text is divided into smaller chunks.
4. Text chunks are converted into embeddings.
5. Embeddings are stored in a FAISS vector database.
6. User enters a question.
7. The system searches the vector database for relevant chunks.
8. The retrieved chunks are provided to the language model.
9. The chatbot generates an answer using the retrieved document content.
10. The source document and page number are displayed.

## Main Features

- PDF document upload
- PDF file validation
- Text extraction
- Text chunking
- Semantic search using embeddings
- FAISS vector database
- Grounded question answering
- Source document and page display
- Refusal when information is not available in the uploaded documents
- Streamlit web interface

## Project Structure

```text
domain_rag_chatbot/
│
├── app.py
├── rag_pipeline.py
├── document_loader.py
├── vector_store.py
├── prompt.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── documents/
│   └── education1.pdf
│
├── vector_store/
│   ├── faiss.index
│   └── chunks.pkl
│
├── tests/
│
└── venv/