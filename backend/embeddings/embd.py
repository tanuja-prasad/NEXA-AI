from langchain_huggingface import HuggingFaceEmbeddings
from preprocessing_chunks.chunk import get_chunks

def embedding_model():
    emb_model=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    return emb_model


print("embeddings created")

