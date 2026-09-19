from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_pdfs


def create_chunks(folder_path="documents"):
    documents = load_pdfs(folder_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = []

    for document in documents:
        split_texts = text_splitter.split_text(document["text"])

        for text in split_texts:
            chunks.append(
                {
                    "text": text,
                    "metadata": document["metadata"],
                }
            )

    return chunks


def answer_question(question, top_k=5):
    from vector_store import search_vector_store
    from prompt import build_prompt

    import os
    from dotenv import load_dotenv
    from groq import Groq

    load_dotenv()

    results = search_vector_store(question, top_k=top_k)

    context_parts = []

    for result in results:
        source = result["metadata"]["source"]
        page = result["metadata"]["page"]
        text = result["text"]

        context_parts.append(
            f"Source: {source}, Page: {page}\n{text}"
        )

    context = "\n\n".join(context_parts)

    final_prompt = build_prompt(context, question)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY was not found.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": final_prompt,
            }
        ],
    )

    answer = response.choices[0].message.content

    return answer, results