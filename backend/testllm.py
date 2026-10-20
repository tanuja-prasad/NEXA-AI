
from rag.generator import load_llm

try:
    llm = load_llm()
    response = llm.invoke("Explain data science in two sentences.")
    print(response.content)

except Exception as e:
    print(f"LLM test failed: {type(e).__name__}: {e}")
