#service/chatbot/session
from service.models.automlproject import AutoMLProject
from typing import Dict
import json
import re
from service.chatbot.ollama_client import OllamaClient
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

    def detect_intent(self, message: str) -> str:
        text = message.lower().strip()
        
        create_project_keywords = ["tạo dự án", "khởi tạo dự án", "bắt đầu dự án", "create project", "làm project", "tạo model","tạo mô hình"]
        greetings = ["Hello","Hi","hi", "hello", "chào", "xin chào", "chào bạn", "chào anh", "chào chị"]
        update_keywords = ["đổi", "cập nhật", "sửa", "thay đổi", "update", "thêm", "xóa", "tên dự án", "dataset", "mô tả", "project"]
        question_keywords = ["tại sao", "vì sao", "giải thích", "hướng dẫn", "làm sao", "cách", "ví dụ", "help", "thắc mắc", "câu hỏi","không hiểu lắm"]
        
            
        # Kiểm tra greeting theo từ nguyên vẹn
        for greet in greetings:
            pattern = r'\b' + re.escape(greet) + r'\b'  # ví dụ \bhi\b
            if re.search(pattern, text):
                return "greeting"
        
        
        if any(kw in text for kw in create_project_keywords):
                return "create_project"
        
        # Check update intent
        if any(kw in text for kw in update_keywords):
            if not self.project_suggestion:
                return "create_project"
            else:
                return "update_project"
        
        # Check question intent
        if any(kw in text for kw in question_keywords):
           return "ask_question"
        
        # Mặc định coi là câu hỏi (hoặc bạn có thể trả về "unknown")
        return "ask_question"

    def _build_history_prompt(self, user_message: str) -> str:
        """
        Tạo prompt cho AI bao gồm các turn hội thoại gần đây để giữ ngữ cảnh.
        Giới hạn lấy 3-4 turn gần nhất (user + assistant).
        """
        turns = self.history[-8:]  
        prompt_lines = []
        for turn in turns:
            role = turn["role"]
            content = turn["content"]
            if role == "user":
                prompt_lines.append(f"Người dùng: {content}")
            else:
                prompt_lines.append(f"Trợ lý: {content}")
        prompt_lines.append(f"Người dùng: {user_message}")
        return "\n".join(prompt_lines)

    def handle_message(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})

        intent = self.detect_intent(message)
        print (intent)
        if intent == "greeting":
            yield "Moew~ Moew~ Chào bạn! Tôi có thể giúp gì cho bạn nào?"
        
        elif intent == "create_project":
            prompt = f"""
Chỉ trả lời bằng tiếng việt, chỉ có 1 JSON luôn ở cuối cùng, trả lời ngắn gọn ít hơn 100 từ.
Bạn là trợ lý AutoML. Với yêu cầu: "{message}"
Hãy tư vấn chi tiết từng bước giúp người dùng như sau:

1. Xác định nhiệm vụ học máy phù hợp: (chọn 1 trong Image Classification, Text Classification, Tabular Classification, Multimodal Classification và giải thích)
2. Database phù hợp trong hệ thống: Không có thì đừng trả lời mục này
2. Cách thu thập dữ liệu :Hướng dẫn xây dựng hoặc thu thập tập dữ liệu (cách lấy dữ liệu, đặc trưng cần chú ý, kích thước mẫu)
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
- Phần tư vấn chi tiết (văn bản) theo cấu trúc mục đề:
1. Xác định nhiệm vụ học máy phù hợp:
2. Database phù hợp trong hệ thống: Không có thì đừng trả lời mục này
3. Cách gán nhãn cho tập dữ liệu (có ví dụ cụ thể)
4. 4. Cách đánh giá mô hình gồm các chỉ số: 
- độ chính xác (Accuracy) (nên chọn chỉ số bao nhiêu)
- Độ chính xác (Precision) 
- Độ nhảy cảm (Recall) 

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
                buffet = ""
                
                for chunk in self.aiAssistant.analyze_message(prompt):
                    buffet += chunk
                    # Bắt đầu JSON block
                    if "```json" in buffet and not in_json_block:
                        in_json_block = True
                        print("In JSON")
                        continue
                    
                    #Nếu vào phần JSON thì
                    if in_json_block:
                        # Nếu phát hiện kết thúc JSON block
                        if "}```" in buffet:
                            print("Out JSON")
                            in_json_block = False

                    #Nếu chưa vào phần JSON
                    else: yield chunk

                # Lưu trợ lý trả lời vào lịch sử
                self.history.append({"role": "assistant", "content": buffet})

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

                yield self.format_summary(self.project_suggestion)
            except Exception as e:
                    print(f"❌ Lỗi khi gọi AI: {e}")

        elif intent == "update_project":

            prompt = f"""  
Bạn là trợ lý AutoML. Người dùng gửi câu:

"{message}"

Hãy phân tích và chỉ trả về một JSON gồm một hoặc nhiều trường muốn cập nhật trong project hiện tại:

- project_name

- project_description

- dataset

- project_type

Nếu không có thay đổi gì, trả về {{}}
Ví dụ trả về:

{{
"project_name": "Tên mới",
"dataset": "dataset ABC"
}}

Chỉ trả về JSON đúng định dạng, không thêm gì khác.
"""     
            update_fields = {}
            response = self.aiAssistant.analyze_message(prompt)
            response2 = ''.join(response)
            print (response2)
            try:
                update_fields = json.loads(response2)
                
            except Exception:
                 print(f"❌ Lỗi khi parse JSON cập nhật: {e}")
                 update_fields = {}
            # Cập nhật vào project_suggestion
            self.project_suggestion.update(update_fields)
            # Trả về tóm tắt
            yield self.format_summary(self.project_suggestion)


        #Người dùng hỏi sâu về vấn đề
        elif intent == "ask_question":
            # Tạo prompt giữ lịch sử hội thoại để AI trả lời sát ngữ cảnh
            prompt = self._build_history_prompt(message)
            prompt += "\n\n Nếu người dùng không hỏi về AutoML thì bảo là: Meo~ Meo~ bạn chỉ nên hỏi về vấn đề liên quan đến AutoML thôi nhé (chỉ trả lời như thế ko thêm gì vào) còn nếu liên quan đến AutoML thì trả lời ngắn gọn, tối đa 3-4 câu, không trả về JSON hay mã code. "
            
            buffet = ""

            try:
                for chunk in self.aiAssistant.analyze_message(prompt):
                    buffet += chunk
                    yield chunk

                self.history.append({"role": "assistant", "content": buffet})
                yield response

            except Exception as e:
                return f"❌ Lỗi khi xử lý câu hỏi: {e}"
    
    def format_summary(self, suggestion: dict) -> str:
        summary = "Thông tin dự án hiện tại:\n"
        for key in ["project_name", "project_description", "dataset", "project_type"]:
            if key in suggestion:
                summary += f"- {key.replace('_', ' ').title()}: {suggestion[key]}\n"
        
        return summary.strip()


    def confirm_create_project(self):
        if not self.project_suggestion:
            return "❌ Chưa có cấu hình dự án đề xuất."
    
        self.project = AutoMLProject()
        # Giả sử AutoMLProject có các thuộc tính tương ứng bạn có thể gán trực tiếp:
        for key, value in self.project_suggestion.items():
            if hasattr(self.project, key):
                setattr(self.project, key, value)
        return "✅ Đã tạo project. Bạn có thể tiếp tục cấu hình thêm."
