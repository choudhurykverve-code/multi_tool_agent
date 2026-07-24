from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI 

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash",
#     temperature=0
# )