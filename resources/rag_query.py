from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def get_embeddings():
    # Safely force CPU — handles torch meta tensor crash
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"device": "cpu"}  # This line is critical
    )
def build_vectorstore():
    loader = DirectoryLoader("resources/docs", glob="**/*.txt")
    docs = loader.load()
    embeddings = get_embeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("resources/faiss_index")

def get_relevant_chunks(query: str):
    embeddings = get_embeddings()
    db = FAISS.load_local("resources/faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db.similarity_search(query, k=3)
