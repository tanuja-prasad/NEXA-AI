from typing import TypedDict


class ChatState(TypedDict, total=False):

    user_id: str

    session_id: str

    question: str

    route: str

    chat_history: str

    long_term_memory: str

    final_context: str

    web_context: str

    answer: str