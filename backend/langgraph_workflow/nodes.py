from rag.hybrid_retriever import hybrid_retrieval
from langgraph_workflow.state import ChatState
from memory.memory import ChatMemory
from rag.generator import load_llm
from tools.web_search import web_search
from langgraph_workflow.router import route_question


llm = load_llm()
memory = ChatMemory()



# Memory Node


def memory_node(state: ChatState):

    session_id = state["session_id"]

    history = memory.get_history(session_id)

    return {
        "chat_history": history
    }



# Router Node


def router_node(state: ChatState):

    question = state["question"]

    route = route_question(question)

    return {
        "route": route
    }



# RAG Retrieval Node


def retrieve_node(state: ChatState):

    question = state["question"]

    context = hybrid_retrieval(question)

    return {
        "final_context": context
    }



# Web Search Node


def web_search_node(state: ChatState):

    question = state["question"]

    results = web_search(question)

    web_context = "\n\n".join(
        f"""
SOURCE {i}:
Title: {result['title']}
Information: {result['body']}
URL: {result['href']}
"""
        for i, result in enumerate(results, 1)
    )

    return {
        "web_context": web_context
    }



# Long-Term Memory Node


def long_term_memory_node(state: ChatState):

    user_id = state["user_id"]

    memories = memory.get_memories(user_id)

    memory_context = ""

    for item in memories:

        memory_context += (
            f"[{item['category']}] "
            f"{item['memory']}\n"
        )

    return {
        "long_term_memory": memory_context
    }



# Generate Answer Node


def generate_node(state: ChatState):

    question = state["question"]

    history = state.get("chat_history", "")

    long_term_memory = state.get(
        "long_term_memory",
        ""
    )

    route = state["route"]


    
    # Select knowledge context
   

    if route == "RAG":

        context = state.get(
            "final_context",
            ""
        )

        prompt = f"""
You are a helpful and knowledgeable AI assistant.

Answer the user's question using the provided knowledge context.

Use the conversation history when relevant.

Use the user's long-term memory when it is relevant
to personalize the response.

Do not make up facts that are not supported by the
knowledge context.

If the information is not available in the context,
clearly say that you do not have enough information.

CONVERSATION HISTORY:

{history}


LONG-TERM USER MEMORY:

{long_term_memory}


KNOWLEDGE CONTEXT:

{context}


USER QUESTION:

{question}


ANSWER:
"""


    elif route == "WEB":

        context = state.get(
            "web_context",
            ""
        )

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question using the web search
results below.

IMPORTANT:

- Use only information supported by the search results.
- Do not invent facts.
- Mention the source when presenting important information.
- If the search results are insufficient, say so.
- For latest/current questions, make it clear that the
  information comes from the retrieved web results.
- Use the user's long-term memory when it is relevant.

CONVERSATION HISTORY:

{history}


LONG-TERM USER MEMORY:

{long_term_memory}


WEB SEARCH RESULTS:

{context}


USER QUESTION:

{question}


ANSWER:
"""


    else:

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question naturally.

Use the conversation history when relevant.

Use the user's long-term memory when it is relevant
to personalize the response.

Do not make up personal information about the user.

CONVERSATION HISTORY:

{history}


LONG-TERM USER MEMORY:

{long_term_memory}


USER QUESTION:

{question}


ANSWER:
"""


    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }



# Save Chat + Long-Term Memory


def save_memory_node(state: ChatState):

    user_id = state["user_id"]

    session_id = state["session_id"]

    question = state["question"]

    answer = state["answer"]


    
    # Save conversation
   

    memory.save_message(
        session_id,
        "user",
        question
    )


    memory.save_message(
        session_id,
        "assistant",
        answer
    )
    
    memory.update_session_title(
        session_id,
        question
    )


    
    # Extract and save long-term memory
    

    memory.save_memory(
        user_id,
        question
    )


    return {}


