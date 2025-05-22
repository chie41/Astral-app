# api/api.py
from fastapi import APIRouter, Request
from service.chatbot.session import ChatSession

router = APIRouter()

sessions = {}  # key: user_id hoặc session_id

@router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = body.get("user_id", "default")
    message = body["message"]

    if user_id not in sessions:
        sessions[user_id] = ChatSession()

    session = sessions[user_id]

    if session.status == "suggesting":
        reply = session.suggest_project(message)
    elif message.lower() == "tạo project":
        reply = session.confirm_create_project()
    else:
        reply = session.project.next_step()

    return {"response": reply}
