# System Architecture

## Domain-Specific RAG Chatbot

```text
                    ┌─────────────────────┐
                    │      User           │
                    │  Upload PDF / Ask   │
                    │      Question       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Streamlit       │
                    │       app.py        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │  PDF Documents  │        │    Question     │
        └────────┬────────┘        └────────┬────────┘
                 │                          │
                 ▼                          │
        ┌─────────────────┐                 │
        │ Text Extraction │                 │
        │ document_loader │                 │
        └────────┬────────┘                 │
                 │                          │
                 ▼                          │
        ┌─────────────────┐                 │
        │ Text Chunking   │                 │
        │ rag_pipeline.py │                 │
        └────────┬────────┘                 │
                 │                          │
                 ▼                          ▼
        ┌──────────────────────────────────────┐
        │       Sentence Transformer           │
        │       all-MiniLM-L6-v2               │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      FAISS      │
                  │  Vector Store   │
                  └────────┬────────┘
                           │
                           │ Retrieve top-k
                           │ relevant chunks
                           ▼
                  ┌─────────────────┐
                  │ Retrieved       │
                  │ Context         │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Grounded Prompt │
                  │    prompt.py    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Groq LLM      │
                  │ GPT-OSS-20B     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Answer + Source │
                  │ Document/Page   │
                  └─────────────────┘