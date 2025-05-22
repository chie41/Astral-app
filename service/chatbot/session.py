from service.models.automlproject import AutoMLProject
from typing import Dict
import json
import re
from service.chatbot.ollama_client import OllamaClient
from service.chatbot.huggingface import HuggingFaceClient
from service.models.datasetManager import DatasetManager

class ChatSession:
    def __init__(self):
        self.project_suggestion: Dict = {}
        self.project: AutoMLProject = None
        self.history = []
        self.status = "suggesting"  # or "configuring"
        #self.aiAssistant = HuggingFaceClient()
        self.aiAssistant = OllamaClient()
        self.datasetmanager = DatasetManager()

    def get_all_datasets(self):
        all_datasets = self.datasetmanager.get_all_dataset_info()
        relevant = []
        for ds in all_datasets:
            # Chuẩn bị thông tin dataset đầy đủ hơn, thêm danh sách cột
                relevant.append({
                    "name": ds.get("name"),
                    "description": ds.get("description"),
                    "status": ds.get("status"),
                    "size": ds.get("size"),
                    "columns": ds.get("columns")  # Đây là danh sách tên cột
                })
        return relevant
    

    def is_automl_request(self, message: str) -> str:
        text = message.lower().strip()
        greetings = ["hi", "hello", "chào", "xin chào"]
        if text in greetings:
            return "Lời chào"

        # Một số câu hỏi phổ biến về giải thích có thể tự xử lý trước
        if any(kw in text for kw in ["tại sao", "vì sao", "giải thích"]):
            return "Giải thích"

        # Một số từ khóa gợi ý tạo model
        if any(kw in text for kw in ["tạo model", "tạo mô hình", "dự án", "project", "gợi ý"]):
            return "Model"

        # Nếu không trúng, gọi AI để phân loại chính xác hơn
        prompt = f"""Hãy phân tích câu nói của người dùng và trả lời:
1. Trả về "Model" nếu người dùng muốn gợi ý tạo model và nếu nó nằm 1 trong 4 loại bài toán (Image Classification, Text Classification, Tabular Classification, Multimodal Classification)
2. Trả về "Giải thích" nếu người dùng hỏi cần giải thích.
3. Trả về "Lời chào" nếu người dùng chào hỏi.
4. Trả về "Khác" nếu không liên quan AutoML.

Chỉ trả lời một trong bốn từ khóa trên, không giải thích gì thêm.

Câu nói: 
{message}
"""
        try:
            resl = self.aiAssistant.analyze_message(prompt)
            return resl.strip()
        except Exception as e:
            return f"❌ Lỗi khi gọi AI phân loại: {e}"

    def handle_message(self, message: str) -> str:
        if self.status == "configuring":
            return self.project.next_step()

        type_ = "Model"

        if type_ == "Model":
            all_datasets = self.get_all_datasets()

            dataset_info_text = "Hiện tại tôi có một số dataset và mô tả như sau. Tôi nên sử dụng dataset nào hay đi thu thập bên ngo:\n"
            if all_datasets:
                for ds in all_datasets:
                    dataset_info_text += f"- {ds['name']} (Số mẫu: {ds['size']}, Mô tả: {ds['description']})\n"
            else:
                dataset_info_text += "Chưa tìm thấy dataset phù hợp trong hệ thống.\n"

            prompt = f"""
Bạn là trợ lý AutoML. Với yêu cầu: "{message}"
{dataset_info_text}
Hãy tư vấn chi tiết từng bước giúp người dùng như sau:

1. Xác định nhiệm vụ học máy phù hợp (chọn 1 trong Image Classification, Text Classification, Tabular Classification, Multimodal Classification và giải thích)
2. Hướng dẫn xây dựng hoặc thu thập tập dữ liệu (cách lấy dữ liệu, đặc trưng cần chú ý, kích thước mẫu) và Dataset gợi ý (nếu có) có thể dùng được (có thể tìm trong database hệ thống) 
3. Cách gán nhãn cho tập dữ liệu (có ví dụ cụ thể)
4. Cách đánh giá mô hình gồm các chỉ số: 
- độ chính xác (Accuracy), 
- Độ chính xác (Precision)
- Độ nhảy cảm (Recall) 

Sau đó, ở cuối hãy gợi ý dự án dưới dạng JSON gồm các trường:
- project_name
- project_type
- project_description
- dataset (tìm trong database gợi ý cho người dùng)

Trả lời theo cấu trúc:
- Phần tư vấn chi tiết (văn bản) 
- Phần JSON (mã code block) viết sau cùng và phần trả lời dưới dạng **JSON duy nhất** như sau không cần thêm gì như "Phần JSON" vào trước cấu trúc cả:

```json
{{
  "project_name": "...",
  "project_type": "...",
  "project_description": "...",
  "dataset": "..."
}}

"""
            
            try:
                in_json_block = False
                json_lines = []
                buffet = ""

                for chunk in self.aiAssistant.analyze_message(prompt):
                    buffet += chunk
                    # Bắt đầu JSON block
                    if "```json" in buffet and not in_json_block:
                        in_json_block = True
                        print("In JSON")
                        continue

                    if in_json_block:
                        # Nếu phát hiện kết thúc JSON block
                        if "}```" in buffet:
                            print("Out JSON")
                            in_json_block = False
                
                    else: yield chunk  # Trả về từng phần text ngay lập tức
                
                #Chạy text hướng dẫn xong thì xử lý JSON
                try:
                    match = re.search(r"```json\s*({.*?})\s*```", buffet, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                        data = json.loads(json_str)
                        self.project_suggestion = {
                            "project_name": data.get("project_name"),
                            "project_type": data.get("project_type"),
                            "project_description": data.get("project_description"),
                            "dataset": data.get("dataset"),
                        }
                        print("Xử lý xong JSON rồi")
                    else:
                        print("❌ Không tìm thấy JSON hợp lệ trong kết quả AI trả về.")
                except Exception as e:
                    print(f"❌ Lỗi khi parse JSON: {e}")
            except Exception as e:
                print(f"❌ Lỗi khi gọi AI: {e}")


        elif type_ == "Lời chào":
            yield "Moew~ Moew~ Xin chào!"


        elif type_ == "Giải thích":
            yield "Moew moew giải thích cho bạn đây!"

        elif type_ == "Khác":
            yield "Moew moew mình không biết, bạn thử hỏi điều khác nhé!"

        else:
            yield "Xin lỗi, tôi chưa hiểu yêu cầu của bạn."

    def confirm_create_project(self):
        self.project = AutoMLProject()
        self.project.update_project_type(self.project_suggestion.get("project_type"))
        self.status = "configuring"
        return "✅ Đã tạo project. Bạn có thể tiếp tục cấu hình thêm."
