#service/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.chatbot.api import router  # import router từ api.py

app = FastAPI()

app.include_router(router, prefix="/api")  # đăng ký router

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc ["http://localhost:5500"] nếu frontend chạy local
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

