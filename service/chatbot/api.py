#service/chatbot/api.py
from fastapi import APIRouter, Request
from service.chatbot.session import ChatSession
from pydantic import BaseModel
from starlette.responses import StreamingResponse

router = APIRouter()

sessions = {}  # key: user_id hoặc session_id

class Request(BaseModel):
    user_id: str = "default"
    message: str


@router.post("/chat")
async def chat(request: Request):
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
