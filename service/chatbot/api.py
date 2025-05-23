#service/chatbot/api.py
from fastapi import APIRouter, Request
from service.chatbot.session import ChatSession
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import HTTPException
from typing import Dict

router = APIRouter()

sessions = {}  # key: user_id hoặc session_id

class ChatRequest(BaseModel):
    user_id: str = "default"
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    user_id = request.user_id
    message = request.message

    if user_id not in sessions:
        sessions[user_id] = ChatSession()

    session = sessions[user_id]

    if session.status == "suggesting":
        reply = session.handle_message(message)
        return StreamingResponse(reply, media_type="text/plain")
    elif session.status == "configuring":
        reply = session.project.next_step()
        return {"response": reply}

class ClearSessionRequest(BaseModel):
    user_id: str

@router.post("/clear_session")
async def clear_session(request: ClearSessionRequest):
    user_id = request.user_id
    if user_id in sessions:
        del sessions[user_id]
        return {"status": "success", "message": f"Session của user_id={user_id} đã bị xóa."}
    else:
        raise HTTPException(status_code=404, detail="Không tìm thấy session để xóa.")

class CreateProjectRequest(BaseModel):
    user_id: str
    project_name: str
    project_type: str
    project_description: str
    dataset: str

projects: Dict[str, dict] = {}

class ConfirmCreateProjectRequest(BaseModel):
    user_id: str

@router.post("/confirm_create_project")
async def confirm_create_project(req: ConfirmCreateProjectRequest):
    user_id = req.user_id
    project_id = f"{user_id}"

    session = sessions[user_id]

    suggestion_config = getattr(session, "project_suggestion", None)
    
    if not suggestion_config:
        raise HTTPException(status_code=404, detail="Không có cấu hình đề xuất trong session.")

    # Lưu tạm project với config lấy từ session
    projects[project_id] = {
        "user_id": user_id,
        "config": suggestion_config,
        "status": "configuring"
    }

    return {
        "status": "ok",
        "message": "Đã tạo project với cấu hình từ session, bạn có thể chỉnh sửa.",
        "config": suggestion_config
    }