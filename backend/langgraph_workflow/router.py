from rag.generator import load_llm

llm = load_llm()


def route_question(question):

    prompt = f"""
You are a routing system for a chatbot.

The chatbot has a static knowledge base containing information about:

- Data Science
- Machine Learning
- Python for Machine Learning
- Statistics
- Probability
- Data Analysis
- Data Preprocessing
- Exploratory Data Analysis
- NumPy
- Pandas
- Data Visualization
- Related technical and educational topics

Classify the user's question into exactly ONE category.

RAG:
Use this when the question is related to information
available in the chatbot's static knowledge base.

WEB:
Use this when the question requires current, latest,
live, recent, or real-time information.

GENERAL:
Use this for casual conversation or questions unrelated
to the knowledge base and not requiring current information.

Important:
If the question asks about a topic present in the knowledge base,
choose RAG even if it is a simple question such as
"What is X?" or "Explain X."

Return ONLY:
RAG
WEB
or
GENERAL

Question:
{question}
"""

    response = llm.invoke(prompt)

    route = response.content.strip().upper()

    if route not in ["RAG", "WEB", "GENERAL"]:
        route = "GENERAL"

    return route