from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "raw.txt"

with open(RAW_FILE, "r", encoding="utf-8") as f:
    text = f.read()


def get_chunks():
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
        
    return splitter.split_text(text)

if __name__ == "__main__":
    chunks=get_chunks()
    print(len(chunks))
    




