from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.chat import router as chat_router

app = FastAPI(
    title="Multi Tool Agent API",
    description="API for the Multi-Tool AI Agent built with LangChain",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)