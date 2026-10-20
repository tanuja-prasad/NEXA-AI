from sqlalchemy import text
from memory.db import engine
from memory.memory_extractor import extract_memories, parse_memory
from uuid import uuid4


class ChatMemory:

   
    # 1. CREATE USER
   

    def create_user(self, username, email,password):

        user_id = uuid4()

        query = text("""
            INSERT INTO users
            (user_id, username, email,password)
            VALUES
            (:uid, :username, :email,:password)
        """)

        with engine.begin() as conn:
            conn.execute(
                query,
                {
                    "uid": user_id,
                    "username": username,
                    "email": email,
                    "password":password
                }
            )

        return user_id

    # Login existing user
    def login_user(self, email, password):

        query = text("""
            SELECT user_id, username
            FROM users
            WHERE email = :email
            AND password = :password
        """)

        with engine.connect() as conn:

            row = conn.execute(
                query,
                {
                    "email": email,
                    "password": password
                }
            ).fetchone()

        return row
    
    # 2. CREATE CHAT SESSION
    
    def create_session(self, user_id, title="New Chat"):

        session_id = uuid4()

        query = text("""
            INSERT INTO chat_sessions
            (session_id, user_id, title)
            VALUES
            (:sid, :uid, :title)
        """)

        with engine.begin() as conn:
            conn.execute(
                query,
                {
                    "sid": session_id,
                    "uid": user_id,
                    "title": title
                }
            )

        return session_id
    
   

    
    # 3. SAVE CHAT MESSAGE
   

    def save_message(self, session_id, role, message):

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

    def get_messages(self, session_id):

        query = text("""
            SELECT role, message
            FROM chat_history
            WHERE session_id = :sid
            ORDER BY created_at
        """)

        with engine.connect() as conn:

            rows = conn.execute(
                query,
                {"sid": session_id}
            ).fetchall()

        messages = []

        for role, message in rows:

            messages.append({
                "role": role,
                "content": message
            })

        return messages
    
    # 4. GET CONVERSATION HISTORY
    

    def get_history(self, session_id):

        query = text("""
            SELECT role, message
            FROM chat_history
            WHERE session_id = :sid
            ORDER BY created_at
        """)

        with engine.connect() as conn:

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


   
    # 5. EXTRACT AND SAVE LONG-TERM MEMORY
    def update_session_title(self, session_id, question):
    
            title = question.strip()
    
            if len(title) > 40:
                title = title[:40] + "..."
    
            query = text("""
                UPDATE chat_sessions
                SET title = :title
                WHERE session_id = :sid
                AND title = 'New Chat'
            """)
    
            with engine.begin() as conn:
    
                conn.execute(
                    query,
                    {
                        "sid": session_id,
                        "title": title
                    }
                )
    
       
        # 6. GET LONG-TERM MEMORIES
        
    
           # ============================================================
    # GET ALL CHAT SESSIONS FOR A USER
    # ============================================================

    def get_sessions(self, user_id):

        query = text("""
            SELECT session_id, title, created_at
            FROM chat_sessions
            WHERE user_id = :uid
            ORDER BY created_at DESC
        """)

        with engine.connect() as conn:

            rows = conn.execute(
                query,
                {
                    "uid": user_id
                }
            ).fetchall()

        sessions = []

        for row in rows:

            sessions.append({
                "session_id": str(row[0]),
                "title": row[1],
                "created_at": row[2]
            })

        return sessions

    # ============================================================
    # GET ONE CHAT SESSION
    # ============================================================

    def get_session(self, session_id):

        query = text("""
            SELECT session_id, title, created_at
            FROM chat_sessions
            WHERE session_id = :sid
        """)

        with engine.connect() as conn:

            row = conn.execute(
                query,
                {
                    "sid": session_id
                }
            ).fetchone()

        if not row:
            return None

        return {
            "session_id": row[0],
            "title": row[1],
            "created_at": row[2]
        }


    # ============================================================
    # DELETE CHAT SESSION
    # ============================================================

    def delete_session(self, session_id):

        delete_messages = text("""
            DELETE FROM chat_history
            WHERE session_id = :sid
        """)

        delete_session = text("""
            DELETE FROM chat_sessions
            WHERE session_id = :sid
        """)

        with engine.begin() as conn:

            conn.execute(
                delete_messages,
                {
                    "sid": session_id
                }
            )

            conn.execute(
                delete_session,
                {
                    "sid": session_id
                }
            )
    
        # Get memories of a user
    def get_memories(self, user_id):
    
            query = text("""
                SELECT memory, category
                FROM user_memory
                WHERE user_id = :uid
                ORDER BY created_at DESC
            """)
    
            with engine.connect() as conn:
    
                rows = conn.execute(
                    query,
                    {
                        "uid": user_id
                    }
                ).fetchall()
    
            memories = []
    
            for memory_value, category in rows:
    
                memories.append({
                    "memory": memory_value,
                    "category": category
                })
    
            return memories
        
        

    def save_memory(self, user_id, user_message):

        # Ask LLM to extract useful memory
        raw_memory = extract_memories(user_message)

        # Convert LLM response into structured data
        memory = parse_memory(raw_memory)

        # Nothing useful to remember
        if memory is None:
            return None

        query = text("""
            INSERT INTO user_memory
            (user_id, memory, category)
            VALUES
            (:uid, :memory, :category)
        """)

        with engine.begin() as conn:

            conn.execute(
                query,
                {
                    "uid": user_id,
                    "memory": memory["memory"],
                    "category": memory["category"]
                }
            )

        return memory
    
    
   