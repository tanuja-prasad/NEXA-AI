from sqlalchemy import text
from memory.db import engine
from memory.extractor import extract_memories, parse_memory


class ChatMemory:

   
  
   
    def save_memory(self, session_id, role, message):

        query = text("""
            INSERT INTO chat_history
            (session_id, role, message)
            VALUES
            (:sid, :role, :message)
        """)

        with engine.begin() as conn:
            conn.execute(
                query,
                {
                    "sid": session_id,
                    "role": role,
                    "message": message
                }
            )


    def get_history(self, session_id):

        query = text("""
            SELECT role, message
            FROM chat_history
            WHERE session_id = :sid
            ORDER BY created_at
        """)

        with engine.begin() as conn:

            rows = conn.execute(
                query,
                {"sid": session_id}
            ).fetchall()

        history = ""

        for role, message in rows:

            if role == "user":
                history += f"User: {message}\n"

            elif role == "assistant":
                history += f"Assistant: {message}\n"

        return history


    
    # Long-term memory
    # -----------------------------

    def save_memory(self, user_id, user_message):

        # Extract memory
        raw_memory = extract_memories(user_message)

        # Convert LLM output into structured data
        memory = parse_memory(raw_memory)

        # Nothing useful to remember
        if memory is None:
            return None

        query = text("""
            INSERT INTO user_memory
            (user_id, memory, category)
            VALUES
            (:user_id, :memory, :category)
        """)

        with engine.begin() as conn:

            conn.execute(
                query,
                {
                    "user_id": user_id,
                    "memory": memory["memory"],
                    "category": memory["category"]
                }
            )

        return memory


    def get_memories(self, user_id):

        query = text("""
            SELECT memory, category
            FROM user_memory
            WHERE user_id = :user_id
            ORDER BY created_at
        """)

        with engine.begin() as conn:

            rows = conn.execute(
                query,
                {"user_id": user_id}
            ).fetchall()

        memories = []

        for memory, category in rows:

            memories.append({
                "memory": memory,
                "category": category
            })

        return memories