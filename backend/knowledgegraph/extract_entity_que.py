from rag.generator import load_llm

llm = load_llm()


def extract_question_entities(question):

    prompt = f"""
Extract the important entities from the following question.

Return ONLY a comma-separated list of entity names.

Example:

Question:
How is machine learning related to data science?

Output:
Machine Learning, Data Science

Question:
{question}

Output:
"""

    response = llm.invoke(prompt)

    entities = response.content.strip()

    return [
        entity.strip()
        for entity in entities.split(",")
        if entity.strip()
    ]