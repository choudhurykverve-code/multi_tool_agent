from fastapi import APIRouter, HTTPException

from api.schemas.chat import ChatRequest, ChatResponse
from api.services.chat_service import chat_with_agent

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post('/', response_model=ChatResponse)
def chat(request:ChatRequest):
    try:
        response = chat_with_agent(request.message)

        return ChatResponse(response=response)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )