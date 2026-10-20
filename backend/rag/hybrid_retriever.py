from rag.retriever import retrival
from knowledgegraph.extract_entity_que import extract_question_entities
from knowledgegraph.graph_search import graph_search


def hybrid_retrieval(question):

   
    # FAISS retrieval
    

    docs = retrival(question)

    vector_context = "\n\n".join(doc.page_content for doc in docs)


    
    # Neo4j retrieval
   

    entities = extract_question_entities(question)

    graph_results = graph_search(entities)

    graph_context = "\n".join(graph_results)


    
    # Combine both
    

    combined_context = f"""VECTOR KNOWLEDGE:{vector_context}
                            KNOWLEDGE GRAPH:{graph_context}
                        """

    return combined_context