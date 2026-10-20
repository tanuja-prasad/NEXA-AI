from langgraph.graph import StateGraph, START, END

from langgraph_workflow.state import ChatState

from langgraph_workflow.nodes import (
    memory_node,
    long_term_memory_node,
    router_node,
    retrieve_node,
    web_search_node,
    generate_node,
    save_memory_node
)


builder = StateGraph(ChatState)



# ADD NODES


builder.add_node(
    "memory",
    memory_node
)

builder.add_node(
    "long_term_memory",
    long_term_memory_node
)

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "retrieve",
    retrieve_node
)

builder.add_node(
    "web_search",
    web_search_node
)

builder.add_node(
    "generate",
    generate_node
)

builder.add_node(
    "save_memory",
    save_memory_node
)



# START → MEMORY

builder.add_edge(
    START,
    "memory"
)



# MEMORY → LONG-TERM MEMORY


builder.add_edge(
    "memory",
    "long_term_memory"
)



# LONG-TERM MEMORY → ROUTER


builder.add_edge(
    "long_term_memory",
    "router"
)



# ROUTER DECISION


def route_next(state: ChatState):

    route = state["route"]

    if route == "RAG":

        return "retrieve"

    elif route == "WEB":

        return "web_search"

    else:

        return "generate"


builder.add_conditional_edges(
    "router",
    route_next
)



# RAG → GENERATE


builder.add_edge(
    "retrieve",
    "generate"
)


# WEB → GENERATE


builder.add_edge(
    "web_search",
    "generate"
)



# GENERATE → SAVE


builder.add_edge(
    "generate",
    "save_memory"
)



# SAVE → END


builder.add_edge(
    "save_memory",
    END
)



# COMPILE


graph = builder.compile()