from sentence_transformers import SentenceTransformer
import faiss
import pickle

from rag_pipeline import create_chunks


# Load the embedding model only once
MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(folder_path="documents"):
    # Create chunks from the PDFs
    chunks = create_chunks(folder_path)

    # Get the text from every chunk
    texts = [chunk["text"] for chunk in chunks]

    # Convert text into embeddings
    embeddings = MODEL.encode(
        texts,
        convert_to_numpy=True
    )

    # Normalize embeddings so inner product works like cosine similarity
    faiss.normalize_L2(embeddings)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to the index
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, "vector_store/faiss.index")

    # Save chunk information
    with open("vector_store/chunks.pkl", "wb") as file:
        pickle.dump(chunks, file)

    return len(chunks), dimension


def search_vector_store(query, top_k=5):
    # Convert the question into an embedding
    query_embedding = MODEL.encode(
        [query],
        convert_to_numpy=True
    )

    # Normalize the query embedding
    faiss.normalize_L2(query_embedding)

    # Load the saved FAISS index
    index = faiss.read_index("vector_store/faiss.index")

    # Search for the most similar chunks
    scores, indices = index.search(query_embedding, top_k)

    # Load the saved chunks
    with open("vector_store/chunks.pkl", "rb") as file:
        chunks = pickle.load(file)

    results = []

    for score, index_number in zip(scores[0], indices[0]):
        if index_number != -1:
            results.append(
                {
                    "text": chunks[index_number]["text"],
                    "metadata": chunks[index_number]["metadata"],
                    "score": float(score),
                }
            )

    return results