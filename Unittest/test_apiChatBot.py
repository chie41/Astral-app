import sys
import os

# Thêm thư mục gốc Astral-app vào sys.path để Python biết tìm module 'service'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from service.chatbot.api import router, sessions, projects
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

class ApiChatBotTest(unittest.TestCase):
    def setUp(self):
        sessions.clear()

    def test_chat_create_session_and_response(self):
        response = client.post("/chat", json={"user_id": "user1", "message": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers["content-type"].startswith("text/plain"))


    def test_clear_session(self):
        sessions["user2"] = object()
        response = client.post("/clear_session", json={"user_id": "user2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "Session của user_id=user2 đã bị xóa."
        })
        self.assertNotIn("user2", sessions)

    def test_clear_session_not_found(self):
        response = client.post("/clear_session", json={"user_id": "unknown"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Không tìm thấy session để xóa.")

    def test_confirm_create_project_success(self):
        class DummySession:
            project_suggestion = {"name": "Test Project", "type": "classification"}
        sessions["user3"] = DummySession()
        response = client.post("/confirm_create_project", json={"user_id": "user3"})
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp["status"], "ok")
        self.assertIn("config", json_resp)
        self.assertIsNotNone(projects.get("user3"))
        self.assertEqual(projects["user3"]["config"], sessions["user3"].project_suggestion)

    def test_confirm_create_project_no_suggestion(self):
        sessions["user4"] = object()
        response = client.post("/confirm_create_project", json={"user_id": "user4"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Không có cấu hình đề xuất trong session.")

if __name__ == "__main__":
    unittest.main()
