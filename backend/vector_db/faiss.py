from langchain_community.vectorstores import FAISS

from embeddings.embd import embedding_model
from preprocessing_chunks.chunk import get_chunks



vector_db=FAISS.from_texts(
    texts=get_chunks(),
    embedding=embedding_model()
)

#faiss gives indexing to each chunk
vector_db.save_local(str("vector_db/faiss_index"))
print("FAISS index saved sucessfully")