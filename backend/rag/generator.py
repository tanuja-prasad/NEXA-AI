
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("API_KEY")


def load_llm():
    if not api_key:
        raise ValueError(
            "API_KEY is missing. Check your backend .env file."
        )

    llm = ChatOpenAI(
        model="openrouter/free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=512,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "NEXA-AI"
        }
    )

    return llm
