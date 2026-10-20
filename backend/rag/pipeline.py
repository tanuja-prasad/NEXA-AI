from memory.memory import ChatMemory
from rag.retriever import retrival
from rag.generator import load_llm
from rag.prompt import prompt
from rag.hybrid_retriever import hybrid_retrieval



# Initialize components


memory = ChatMemory()
llm = load_llm()


# Create user and chat session


user_id = memory.create_user(
    "Tanuja",
    "tanuja@example.com"
)

SESSION_ID = memory.create_session(
    user_id,
    "ChatBot"
)

print("User ID:", user_id)
print("Session ID:", SESSION_ID)



# Chat loop


while True:

    question = input("\nYou: ")

    # Exit condition
    if question.lower() == "exit":
        print("Chat ended.")
        break


    
    # 1. Get previous conversation from PostgreSQL
   

    history = memory.get_history(SESSION_ID)


    
    # 2. Retrieve relevant documents from FAISS
  


    #from FAISS db for static - no longer to be used
    '''docs = retrival(question)


  
    # 3. Combine retrieved documents
    

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )'''
    
    
    #context from both RAG static(using FAISS vector db) + neo4j graph db
    context=hybrid_retrieval(question)



    # 4. Create final prompt
   

    final_prompt = prompt.format(
        history=history,
        context=context,
        question=question
    )


    
    # 5. Send prompt to OpenRouter LLM
 

    response = llm.invoke(final_prompt)

    answer = response.content


   
    # 6. Display answer
   

    print("\nAssistant:", answer)


  
    # 7. Save user message in PostgreSQL
    
    memory.save_message(
        SESSION_ID,
        "user",
        question
    )


  
    # 8. Save assistant response in PostgreSQL
    

    memory.save_message(
        SESSION_ID,
        "assistant",
        answer
    )