from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

# ---------------------------
# LLM INIT
# ---------------------------
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=1024
)