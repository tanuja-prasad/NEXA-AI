from fastapi import FastAPI
from pydantic import BaseModel

from langgraph_workflow.graph import graph


app = FastAPI(
    title="Memory-Augmented Hybrid RAG Chatbot",
    description="AI chatbot using RAG, Knowledge Graph, Web Search and Long-Term Memory",
    version="1.0"
)



# REQUEST MODEL


class ChatRequest(BaseModel):

    user_id: str
    session_id: str
    question: str



# CHAT ENDPOINT


@app.post("/chat")
def chat(request: ChatRequest):

    result = graph.invoke({
        "user_id": request.user_id,
        "session_id": request.session_id,
        "question": request.question
    })

    return {
        "question": request.question,
        "route": result.get("route"),
        "answer": result.get("answer")
    }



# HEALTH CHECK


@app.get("/")
def root():

    return {
        "message": "Memory-Augmented Hybrid RAG Chatbot API is running"
    }