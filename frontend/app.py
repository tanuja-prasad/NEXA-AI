import os
import sys

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import streamlit as st
import time
from sqlalchemy import text

from memory.memory import ChatMemory
from memory.db import engine
from langgraph_workflow.graph import graph



st.set_page_config(
    page_title="NEXA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)



memory = ChatMemory()




defaults = {
    "logged_in": False,
    "user_id": None,
    "username": None,
    "email": None,
    "session_id": None,
    "messages": [],
    "page": "login",

    # Evaluation
    "response_time": None,
    "last_evaluation": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value




st.markdown(
    """
<style>


html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
}

.stApp {
    background: #f7f9ff;
    color: #172033;
}




.block-container {
    padding-top: 2rem;
    padding-bottom: 7rem;
    max-width: 1200px;
}




section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e7eaf3;
    padding-top:0px !important;
   
}

section[data-testid="stSidebar"] > div {
    padding: 2rem 1.2rem;
    padding-top: 0px !important;;
}


/* NEXA LOGO */

.nexa-logo {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #172033;
    margin-bottom: 3px;
}

.nexa-star {
    color: #635bff;
}

.nexa-dot {
    color: #6c63ff;
}

.nexa-tagline {
    font-size: 12px;
    color: #7b8498;
    margin-bottom: 28px;
}



section[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px;
    border: 1px solid #e3e6ef;
    background: #ffffff;
    color: #273044;
    font-weight: 500;
    min-height: 42px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #635bff;
    color: #635bff;
    background: #f7f6ff;
}


/* NEW CHAT BUTTON */

.new-chat-btn {
    background: linear-gradient(
        135deg,
        #635bff,
        #7c6cff
    ) !important;

    color: white !important;
    border: none !important;
}




.recent-title {
    font-size: 11px;
    font-weight: 700;
    color: #8991a5;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 28px;
    margin-bottom: 12px;
}




.user-card {
    background: #f7f7ff;
    border: 1px solid #e8e8f5;
    border-radius: 14px;
    padding: 14px;
    margin-top: 20px;
}

.user-name {
    font-weight: 700;
    color: #20283a;
    font-size: 14px;
}

.user-email {
    color: #7b8498;
    font-size: 12px;
    margin-top: 4px;
}




.main-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #172033;
    margin-bottom: 4px;
}

.main-title .accent {
    color: #635bff;
}

.main-subtitle {
    color: #7b8498;
    font-size: 14px;
    margin-bottom: 30px;
}



.welcome-box {
    background: linear-gradient(
        135deg,
        #f0efff,
        #f8f7ff
    );

    border: 1px solid #e3e0ff;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
    margin-top: 30px;
}

.welcome-icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.welcome-title {
    font-size: 23px;
    font-weight: 700;
    color: #20283a;
}

.welcome-text {
    color: #747d91;
    font-size: 14px;
    margin-top: 6px;
}



[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 12px 0 !important;
}


/* USER MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #f0efff !important;
    border-radius: 15px !important;
    padding: 15px 18px !important;
    margin: 8px 0 !important;
}


/* ASSISTANT MESSAGE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #ffffff !important;
    border: 1px solid #e9ebf2 !important;
    border-radius: 15px !important;
    padding: 17px 20px !important;
    margin: 8px 0 16px 0 !important;
    box-shadow: 0 2px 8px rgba(30, 40, 70, 0.03);
}


/* CHAT TEXT */

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: #20283a !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}


/* CODE */

[data-testid="stChatMessage"] code {
    background: #f1f3f8 !important;
    color: #31394d !important;
}




[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #dddff0 !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 30px rgba(42, 48, 80, 0.08);
}

[data-testid="stChatInput"] textarea {
    color: #20283a !important;
    background: #ffffff !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #9aa1b2 !important;
    border:2px;
}




[data-testid="stChatInput"] button {
    background: #635bff !important;
    border-radius: 10px !important;
}




.evaluation-card {
    background: #ffffff;
    border: 1px solid #e6e8f0;
    border-radius: 15px;
    padding: 16px;
    margin-top: 25px;
}

.evaluation-title {
    color: #4b5568;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.metric-label {
    color: #8a92a4;
    font-size: 11px;
}

.metric-value {
    color: #20283a;
    font-size: 20px;
    font-weight: 700;
}



.auth-page {
    min-height: calc(100vh - 80px);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.auth-card {
    width: 100%;
    max-width: 440px;
    background: #ffffff;
    padding: 38px 42px;
    border-radius: 22px;
    box-shadow: 0 15px 45px rgba(30, 41, 59, 0.10);
    border: 1px solid #e5e7eb;
}

.auth-logo {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 5px;
}

.auth-logo span {
    color: #2563eb;
}

.auth-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    margin-bottom: 28px;
}

.auth-card label {
    color: #334155 !important;
    font-weight: 600 !important;
}

.auth-card input {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    border-radius: 10px !important;
}

.auth-card input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
}

.auth-card button {
    border-radius: 10px !important;
    min-height: 44px !important;
    font-weight: 600 !important;
}

.auth-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 25px;
}


body:has(.auth-page) .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

body:has(.auth-page) [data-testid="stHeader"] {
    background: transparent !important;
}

body:has(.auth-page) [data-testid="stToolbar"] {
    display: none;
}
.login-logo {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #172033;
}

.login-logo .accent {
    color: #635bff;
}

.login-subtitle {
    text-align: center;
    color: #7b8498;
    font-size: 13px;
    margin-top: 7px;
    margin-bottom: 25px;
}


/* LOGIN INPUT */

.login-card input {
    border-radius: 10px !important;
}




button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #635bff,
        #7c6cff
    ) !important;

    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}




#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}




::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #f7f9ff;
}

::-webkit-scrollbar-thumb {
    background: #d4d7e3;
    border-radius: 10px;
}

</style>
""",
    unsafe_allow_html=True
)




def valid_email(email):

    email = email.strip()

    return (
        "@" in email
        and "." in email.split("@")[-1]
        and " " not in email
    )


def valid_password(password):

    if len(password) < 8:
        return False

    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)

    return has_letter and has_number




def load_chat(session_id):

    try:

        messages = memory.get_messages(session_id)

        st.session_state.messages = messages

    except Exception as e:

        st.session_state.messages = []

        st.error("Unable to load chat.")




def create_new_chat():

    try:

        sid = memory.create_session(
            st.session_state.user_id,
            "New Chat"
        )

        st.session_state.session_id = str(sid)

        st.session_state.messages = []

        st.rerun()

    except Exception as e:

        st.error(f"Unable to create chat: {e}")




def login_user(email, password):

    try:

        user = memory.login_user(
            email.strip(),
            password
        )

        if not user:

            st.error("Invalid email or password.")

            return

        st.session_state.logged_in = True
        st.session_state.user_id = str(user[0])
        st.session_state.username = user[1]
        st.session_state.email = email.strip()
        st.session_state.page = "chat"

        sessions = memory.get_sessions(
            st.session_state.user_id
        )

        if sessions:

            st.session_state.session_id = str(
                sessions[0]["session_id"]
            )

            load_chat(
                st.session_state.session_id
            )

        else:

            sid = memory.create_session(
                st.session_state.user_id,
                "New Chat"
            )

            st.session_state.session_id = str(sid)

            st.session_state.messages = []

        st.rerun()

    except Exception as e:

        st.error(f"Login failed: {e}")




def signup_user(
    username,
    email,
    password,
    confirm_password
):

    username = username.strip()
    email = email.strip()

    if not username:

        st.error("Please enter your name.")
        return

    if not valid_email(email):

        st.error("Please enter a valid email.")
        return

    if not valid_password(password):

        st.error(
            "Password must contain at least 8 characters, "
            "including letters and numbers."
        )

        return

    if password != confirm_password:

        st.error("Passwords do not match.")
        return

    try:

        query = text(
            """
            SELECT user_id
            FROM users
            WHERE email = :email
            """
        )

        with engine.connect() as conn:

            existing = conn.execute(
                query,
                {"email": email}
            ).fetchone()

        if existing:

            st.error(
                "An account with this email already exists."
            )

            return

        memory.create_user(
            username,
            email,
            password
        )

        st.success(
            "Account created successfully. Please login."
        )

    except Exception as e:

        st.error(f"Signup failed: {e}")




def logout():

    for key in [
        "logged_in",
        "user_id",
        "username",
        "email",
        "session_id",
        "messages"
    ]:

        if key == "logged_in":
            st.session_state[key] = False

        elif key == "messages":
            st.session_state[key] = []

        else:
            st.session_state[key] = None

    st.rerun()




def delete_chat(session_id):

    try:

        memory.delete_session(session_id)

        sessions = memory.get_sessions(
            st.session_state.user_id
        )

        if sessions:

            sid = str(
                sessions[0]["session_id"]
            )

            st.session_state.session_id = sid

            load_chat(sid)

        else:

            sid = memory.create_session(
                st.session_state.user_id,
                "New Chat"
            )

            st.session_state.session_id = str(sid)

            st.session_state.messages = []

        st.rerun()

    except Exception as e:

        st.error(f"Unable to delete chat: {e}")




def authentication_page():

    st.markdown(
        '<div class="login-background">',
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 1.15, 1]
    )

    with center:

        st.markdown(
            """
            <div class="login-logo">
                    <span class="accent">✦</span> NEXA<span class="accent">.</span>
            </div>
            """
            ,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="login-subtitle">
                                Memory-Augmented Knowledge Intelligence
            </div>
            """,
            unsafe_allow_html=True
        )

                

        login_tab, signup_tab = st.tabs(
            ["Login", "💠Create Account"]
        )

        with login_tab:

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="login_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            st.write("")

            if st.button(
                "Sign In",
                type="primary",
                use_container_width=True
            ):

                if not email or not password:

                    st.error(
                        "Please enter email and password."
                    )

                else:

                    login_user(
                        email,
                        password
                    )

        with signup_tab:

            username = st.text_input(
                "Full Name",
                placeholder="Your name",
                key="signup_username"
            )

            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="signup_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 8 characters",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter password",
                key="signup_confirm_password"
            )

            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True
            ):

                signup_user(
                    username,
                    email,
                    password,
                    confirm_password
                )

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#9299aa;
            font-size:12px;
            margin-top:25px;
        ">
            NEXA AI • RAG • Knowledge Graph • Memory
        </div>
        """,
        unsafe_allow_html=True
    )




def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="nexa-logo">
                <span class="nexa-star">✦</span> NEXA<span class="nexa-dot">.</span>
            </div>

            <div class="nexa-tagline">
                Memory-Augmented Knowledge Intelligence
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "+  New Chat",
            use_container_width=True,
            type="primary"
        ):

            create_new_chat()

        st.markdown(
            '<div class="recent-title">Recent Chats</div>',
            unsafe_allow_html=True
        )

        try:

            sessions = memory.get_sessions(
                st.session_state.user_id
            )

        except Exception:

            sessions = []

        if sessions:

            for session in sessions:

                sid = str(
                    session["session_id"]
                )

                title = session["title"] or "New Chat"

                if len(title) > 27:

                    title = title[:27] + "..."

                c1, c2 = st.columns(
                    [5, 1]
                )

                with c1:

                    if st.button(
                        title,
                        key=f"chat_{sid}",
                        use_container_width=True
                    ):

                        st.session_state.session_id = sid

                        load_chat(sid)

                        st.rerun()

                with c2:

                    if st.button(
                        "⋮",
                        key=f"menu_{sid}",
                        use_container_width=True
                    ):

                        delete_chat(sid)

        else:

            st.caption(
                "Your conversations will appear here."
            )

        st.divider()

        

        st.markdown(
            """<div class="recent-title">Evaluation</div>""",
            unsafe_allow_html=True
        )

        if st.session_state.response_time is not None:

            st.markdown(
                f"""
                <div class="evaluation-card">

                <div class="evaluation-title">
                        Latest Response
                </div>

                <div class="metric-label">
                        Response time
                </div>

                <div class="metric-value">
                        {st.session_state.response_time:.2f}s
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.caption(
                "Metrics will appear after your first question."
            )

       
        st.markdown(
            f"""
            <div class="user-card">

            <div class="user-name">
                    👤 {st.session_state.username}
            </div>

            <div class="user-email">
                    {st.session_state.email}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "Logout",
            use_container_width=True
        ):

            logout()




def chat_page():

    render_sidebar()

    
    st.markdown(
        """
        <div class="main-title">
            Welcome to <span class="accent">NEXA.</span>
        </div>

        <div class="main-subtitle">
            Your memory-augmented knowledge intelligence assistant.
        </div>
        """,
        unsafe_allow_html=True
    )

    

    if not st.session_state.session_id:

        create_new_chat()

        return

    

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="welcome-box">

            <div class="welcome-icon">
                    ✦
            </div>

            <div class="welcome-title">
                    How can NEXA help you?
            </div>

            <div class="welcome-text">
                    start a conversation.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    

    for message in st.session_state.messages:

        role = message["role"]

        content = message["content"]

        with st.chat_message(
            role,
            avatar="🤖" if role == "assistant" else "👤"
        ):

            st.markdown(content)

    

    question = st.chat_input(
        "Message NEXA..."
    )

    if not question:

        return

    question = question.strip()

    if not question:

        return

   

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(question)

    

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        start_time = time.perf_counter()

        try:

            with st.spinner("NEXA is thinking..."):

                result = graph.invoke(
                    {
                        "user_id":
                            st.session_state.user_id,

                        "session_id":
                            st.session_state.session_id,

                        "question":
                            question
                    }
                )

            elapsed = time.perf_counter() - start_time

            st.session_state.response_time = elapsed

           

            answer = result.get(
                "answer",
                ""
            )

            if not answer:

                answer = (
                    "I could not generate an answer "
                    "for this question."
                )

           

            st.markdown(answer)

           

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            

            try:

                memory.update_session_title(
                    st.session_state.session_id,
                    question
                )

            except Exception:
                pass

            

            try:

                memory.save_message(
                    st.session_state.session_id,
                    "user",
                    question
                )

                memory.save_message(
                    st.session_state.session_id,
                    "assistant",
                    answer
                )

            except Exception:
                pass

            

            try:

                memory.save_memory(
                    st.session_state.user_id,
                    question
                )

            except Exception:
                pass

        except Exception as e:

            elapsed = time.perf_counter() - start_time

            st.session_state.response_time = elapsed

            st.error(
                "NEXA could not process this request."
            )

            with st.expander(
                "Technical details"
            ):

                st.exception(e)




if st.session_state.logged_in:

    chat_page()

else:

    authentication_page()