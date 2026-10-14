from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

# ---------------------------
# LLM INIT
# ---------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.1,
    max_tokens=2048,
    reasoning_effort="low",
    reasoning_format="hidden",
)