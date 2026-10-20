from rag.generator import load_llm


llm = load_llm()


def evaluate_context_relevance(question, context):

    prompt = f"""
You are an evaluator.

Evaluate how relevant the retrieved context is to the user question.

Give a score from 1 to 5.

1 = Completely irrelevant
2 = Mostly irrelevant
3 = Partially relevant
4 = Mostly relevant
5 = Highly relevant

QUESTION:
{question}

CONTEXT:
{context}

Return only the score.
"""

    response = llm.invoke(prompt)

    return response.content.strip()


def evaluate_answer_correctness(question, answer):

    prompt = f"""
You are an evaluator.

Evaluate whether the answer correctly addresses the user's question.

Give a score from 1 to 5.

1 = Completely incorrect
2 = Mostly incorrect
3 = Partially correct
4 = Mostly correct
5 = Fully correct

QUESTION:
{question}

ANSWER:
{answer}

Return only the score.
"""

    response = llm.invoke(prompt)

    return response.content.strip()


def evaluate_faithfulness(answer, context):

    prompt = f"""
You are an evaluator.

Evaluate whether the answer is supported by the provided context.

Give a score from 1 to 5.

1 = Completely unsupported
2 = Mostly unsupported
3 = Partially supported
4 = Mostly supported
5 = Fully supported

CONTEXT:
{context}

ANSWER:
{answer}

Return only the score.
"""

    response = llm.invoke(prompt)

    return response.content.strip()