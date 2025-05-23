import sys
import os

# Thêm thư mục gốc Astral-app vào sys.path để Python biết tìm module 'service'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from service.models.automlproject import AutoMLProject  # đổi tên your_module thành file chứa class này

class TestAutoMLProject(unittest.TestCase):
    def setUp(self):
        self.project = AutoMLProject()

    def test_initial_state(self):
        self.assertIsNone(self.project.project_name)
        self.assertIsNone(self.project.project_description)
        self.assertIsNone(self.project.project_type)
        self.assertIsNone(self.project.dataset)
        self.assertIsNone(self.project.first_column)
        self.assertIsNone(self.project.second_column)
        self.assertIsNone(self.project.accuracy)
        self.assertIsNone(self.project.training_time)
        self.assertEqual(self.project.steps_done, [])

    def test_update_and_getters(self):
        self.project.update_project_name("My Project")
        self.project.update_project_description("Desc")
        self.project.update_project_type("Text Classification")
        self.project.update_dataset_info("Dataset A")
        self.project.update_columns("image", "label")
        self.project.update_accuracy(0.95)
        self.project.update_training_time(120)
        self.project.add_step_done("step1")

        self.assertEqual(self.project.get_project_name(), "My Project")
        self.assertEqual(self.project.get_project_description(), "Desc")
        self.assertEqual(self.project.get_project_type(), "Text Classification")
        self.assertEqual(self.project.get_dataset(), "Dataset A")
        self.assertEqual(self.project.get_columns(), ("image", "label"))
        self.assertEqual(self.project.get_accuracy(), 0.95)
        self.assertEqual(self.project.get_training_time(), 120)
        self.assertIn("step1", self.project.get_steps_done())

    def test_add_step_done_no_duplicates(self):
        self.project.add_step_done("step1")
        self.project.add_step_done("step1")  # thêm lại không được trùng
        self.assertEqual(self.project.get_steps_done().count("step1"), 1)

    def test_next_step_logic(self):
        # Step 0: chưa có project_type và project_name
        self.project.steps_done = []
        self.project.project_type = None
        self.project.project_name = None
        self.assertEqual(self.project.next_step(), "Bạn muốn làm loại bài toán nào?")

        # Step 0: có project_type nhưng chưa có project_name
        self.project.project_type = "Image Classification"
        self.project.project_name = None
        self.assertEqual(self.project.next_step(), "Bạn cần phải đặt tên cho bài toán")

        # Step 0: có cả project_type và project_name
        self.project.project_name = "Test Project"
        self.assertEqual(self.project.next_step(), "Ok")

        # Step 1: yêu cầu dataset_info (note: property tên dataset chứ không phải dataset_info)
        self.project.steps_done = ["step1"]
        self.project.dataset = None
        self.assertEqual(self.project.next_step(), "Vui lòng chọn dataset huấn luyện")

        self.project.dataset = "Dataset A"
        self.assertEqual(self.project.next_step(), "Ok")

        # Step 2: yêu cầu điền đủ 2 cột
        self.project.steps_done = ["step1", "step2"]
        self.project.first_column = None
        self.project.second_column = None
        self.assertEqual(self.project.next_step(), "Vui lòng điền đủ hai cột (ví dụ image column và target column)")

        self.project.first_column = "image"
        self.project.second_column = "label"
        self.assertEqual(self.project.next_step(), "Ok")

        # Step 3: yêu cầu accuracy và training_time
        self.project.steps_done = ["step1", "step2", "step3"]
        self.project.accuracy = None
        self.project.training_time = None
        self.assertEqual(self.project.next_step(), "Vui lòng điền tỉ lệ chính xác")

        self.project.accuracy = 0.9
        self.assertEqual(self.project.next_step(), "Vui lòng điền thời gian huấn luyện")

        self.project.training_time = 100
        self.assertEqual(self.project.next_step(), "Ok")

        # Step lớn hơn 3
        self.project.steps_done = ["step1", "step2", "step3", "step4"]
        self.assertEqual(self.project.next_step(), "Ok")

if __name__ == "__main__":
    unittest.main()
