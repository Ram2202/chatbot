# scripts/build_index.py
from resources.rag_query import build_vectorstore
build_vectorstore()
print("✅ Vector index built.")
