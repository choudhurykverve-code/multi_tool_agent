import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from api.schemas.chat import ChatRequest, ChatResponse
from api.services.chat_service import chat_with_agent

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post('/', response_model=ChatResponse)
def chat(request: Request, payload: ChatRequest):
    try:
        session_id = request.cookies.get("agent_session_id")
        if not session_id:
            session_id = str(uuid.uuid4())

        response_text = chat_with_agent(payload.message, session_id)

        response = JSONResponse(content={"response": response_text})
        response.set_cookie(
            key="agent_session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
        )
        return response

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