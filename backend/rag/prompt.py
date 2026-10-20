from langchain_core.prompts import PromptTemplate

template='''You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply:

"I don't know based on the provided context."

Conversation Hostory:
{history}

Context:
{context}

Question:
{question}

Answer:'''

prompt=PromptTemplate(
    input_variables=["history","context","question"],
    template=template
)

