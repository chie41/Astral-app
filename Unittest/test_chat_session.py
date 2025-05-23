import sys
import os

# Thêm thư mục gốc Astral-app vào sys.path để Python biết tìm module 'service'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch
from service.chatbot.session import ChatSession
from service.models.automlproject import AutoMLProject

class TestChatSession(unittest.TestCase):
    def setUp(self):
        self.session = ChatSession()
        # Mock AI assistant tránh gọi API thực
        self.session.aiAssistant.analyze_message = MagicMock(return_value=iter(["dummy response"]))
    
    #test phân biệt loại message
    def test_detect_intent(self):
        self.assertEqual(self.session.detect_intent("Hello"), "greeting")
        self.assertEqual(self.session.detect_intent("Tôi muốn tạo dự án mới"), "create_project")
        self.session.project_suggestion = {}
        self.assertEqual(self.session.detect_intent("Tôi muốn đổi tên dự án"), "create_project")
        self.session.project_suggestion = {"project_name": "Test"}
        self.assertEqual(self.session.detect_intent("Tôi muốn đổi tên dự án"), "update_project")
        self.assertEqual(self.session.detect_intent("Tại sao mô hình không tốt?"), "ask_question")
        self.assertEqual(self.session.detect_intent("Không hiểu lắm"), "ask_question")

    #Test hàm tóm tắt JSON các thông tin dự án
    def test_format_summary(self):
        sugg = {
            "project_name": "Dự án A",
            "project_description": "Mô tả dự án A",
            "dataset": "Dataset 1",
            "project_type": "Text Classification"
        }
        expected = (
            "Thông tin dự án hiện tại:\n"
            "- Project Name: Dự án A\n"
            "- Project Description: Mô tả dự án A\n"
            "- Dataset: Dataset 1\n"
            "- Project Type: Text Classification"
        )
        self.assertEqual(self.session.format_summary(sugg), expected)
    
    #test nếu chưa có cấu hình thì từ chối
    def test_confirm_create_project_no_suggestion(self):
        self.session.project_suggestion = {}
        self.assertEqual(self.session.confirm_create_project(), "❌ Chưa có cấu hình dự án đề xuất.")
        self.assertIsNone(self.session.project)

    #test tạo project với các trường thông tin JSON
    def test_confirm_create_project_with_suggestion(self):
        self.session.project_suggestion = {
            "project_name": "Project X",
            "project_type": "Image Classification",
            "project_description": "Test description",
            "dataset": "DatasetX"
        }
        result = self.session.confirm_create_project()
        self.assertEqual(result, "✅ Đã tạo project. Bạn có thể tiếp tục cấu hình thêm.")
        self.assertIsInstance(self.session.project, AutoMLProject)
        self.assertEqual(self.session.project.project_name, "Project X")
        self.assertEqual(self.session.project.project_type, "Image Classification")
        self.assertEqual(self.session.project.project_description, "Test description")
        self.assertEqual(self.session.project.dataset, "DatasetX")
    
    
    def test_handle_message_create_project_without_json(self):
        # Giả lập AI trả về text không có JSON block
        class FakeAI:
            def analyze_message(self, prompt):
                yield "Đây là phần tư vấn chi tiết..."
                yield "Không có JSON."

        self.session.aiAssistant = FakeAI()

        responses = list(self.session.handle_message("Tạo dự án mới"))
        # Cuối cùng vẫn có phần tóm tắt (dù rỗng)
        self.assertIn("Thông tin dự án hiện tại", responses[-1])

    #test tạo project từ JSON
    def test_handle_message_create_project_with_json(self):
        # Giả lập AI trả về JSON block đúng định dạng
        class FakeAI:
            def analyze_message(self, prompt):
                yield "Tư vấn chi tiết...\n```json\n"
                yield '{"project_name": "TestProj", "project_type": "Tabular", "project_description": "Desc", "dataset": "Data1"}'
                yield "\n```"

        self.session.aiAssistant = FakeAI()

        responses = list(self.session.handle_message("Tạo dự án AI"))
        self.assertIn("Thông tin dự án hiện tại", responses[-1])
        self.assertEqual(self.session.project_suggestion.get("project_name"), "TestProj")

    #test update project
    def test_handle_message_update_project(self):
        # Giả lập AI trả về JSON cập nhật
        class FakeAI:
            def analyze_message(self, prompt):
                yield '{"project_name": "Updated Project"}'

        self.session.aiAssistant = FakeAI()
        self.session.project_suggestion = {
            "project_name": "Old Project",
            "project_type": "Text Classification",
            "project_description": "Old desc",
            "dataset": "Old Dataset"
        }

        responses = list(self.session.handle_message("Cập nhật tên dự án"))
        self.assertIn("Thông tin dự án hiện tại", responses[-1])
        self.assertEqual(self.session.project_suggestion.get("project_name"), "Updated Project")



if __name__ == '__main__':
    unittest.main()
