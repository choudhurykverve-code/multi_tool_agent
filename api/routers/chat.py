import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from api.schemas.chat import ChatRequest, ChatResponse
from api.services.chat_service import chat_with_agent
from tools.rag import reset_vectorstore_cache

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


@router.post('/upload-pdf')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    documents_dir = Path("documents")
    documents_dir.mkdir(exist_ok=True)

    file_path = documents_dir / file.filename
    counter = 1
    while file_path.exists():
        stem = Path(file.filename).stem
        suffix = Path(file.filename).suffix
        file_path = documents_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    contents = await file.read()
    with file_path.open("wb") as target:
        target.write(contents)

    reset_vectorstore_cache()

    return {
        "message": "PDF uploaded successfully.",
        "filename": file_path.name,
        "saved_to": str(file_path)
    }