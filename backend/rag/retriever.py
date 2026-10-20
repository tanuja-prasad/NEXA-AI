from pathlib import Path

from preprocessing_chunks.chunk import get_chunks
from embeddings.embd import embedding_model
from langchain_community.vectorstores import FAISS

BACKEND_DIR = Path(__file__).resolve().parents[1]
INDEX_DIR = BACKEND_DIR / "vector_db" / "faiss_index"


db=FAISS.load_local(
    str(INDEX_DIR),
    embedding_model(),
    allow_dangerous_deserialization=True
)

def retrival(query,k=3):
    docs=db.similarity_search(query,k=3)
    return docs

