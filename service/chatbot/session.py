from models.automlproject import AutoMLProject
from typing import Dict
import json
import re
from service.chatbot.ollama_client import OllamaClient
from service.chatbot.huggingface import HuggingFaceClient

class ChatSession:
    def __init__(self):
        self.project_suggestion: Dict = {}
        self.project: AutoMLProject = None
        self.history = []
        self.status = "suggesting"  # or "configuring"
        #self.aiAssistant = HuggingFaceClient()
        self.aiAssistant = OllamaClient()

    def get_relevant_datasets(self, project_type: str):
        all_datasets = self.dataset_manager.get_all_dataset_info()
        relevant = []
        for ds in all_datasets:
            # Kiểm tra mô tả có chứa project_type (không phân biệt hoa thường)
            if ds.get("description") and project_type.lower() in ds["description"].lower():
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

        type_ = self.is_automl_request(message)

        if type_ == "Model":
            prompt = f"""
Bạn là trợ lý AutoML. Với yêu cầu: "{message}"
Hãy tư vấn chi tiết từng bước giúp người dùng như sau:

1. Xác định nhiệm vụ học máy phù hợp (chọn 1 trong Image Classification, Text Classification, Tabular Classification, Multimodal Classification và giải thích)
VD trả lời câu 1: Multimodal Classification la lựa chọn tốt nhất cho dự an nay vì bạn sẽ lam việc với hai loại dữ liệu khác nhau: hình ảnh (ảnh sản phẩm) và văn bản (thông tin mô tả sản phẩm). Mô hình sẽ học cách kết hợp thông tin từ cả hai nguồn để đưa ra dự đoán chính xác về loại mỹ phẩm.
2. Hướng dẫn xây dựng hoặc thu thập tập dữ liệu (cách lấy dữ liệu, đặc trưng cần chú ý, kích thước mẫu) và Dataset gợi ý (nếu có) có thể dùng được (có thể tìm trong database hệ thống) 
VD trả lời câu 2:
Hiện nay trong các dataset của bạn tôi không thấy loại nào phù hợp nhưng tôi sẽ hướng dẫn bạn thu thập dữ liệu như sau:
 -	Thu thập dữ liệu: Bạn cần thu thập ảnh sản phẩm và thông tin mô tả của chúng từ Shopee. Bạn có thể sử dụng API của Shopee (nếu có) hoặc thu thập dữ liệu thủ công từ trang web.
Ví dụ: Một tập dữ liệu có thể bao gồm:
-	Hình ảnh: Ánh của các sản phẩm như son môi, kem dưỡng da, phấn trang điểm.
-	Thông tin mô tả: Tên sản phẩm, loại sản phẩm, thành phần, công dụng, giá cả.
-	 Chọn đặc trưng: Đối với hình ảnh, bạn có thể sử dụng các đặc trưng như kích thước, màu sắc, và hình dạng. Đối với văn bản, bạn có thể sử dụng các từ khóa và mô tả sản phẩm.
-	Kich thưoc tập dữ liệu: Một tập dữ liệu tối thieu nên có từ 1000 đến 5000 mẫu để đảm bảo mô hình có đủ thông tin để học.
3. Cách gán nhãn cho tập dữ liệu (ví dụ cụ thể)
Ví dụ trả lời câu 3:
Mỗi sản phẩm trong tập dữ liệu căn được gán nhãn với loại mỹ phẩm tương ứng. Ví dụ:
-	Son môi: "Son môi"
-	Kem dưỡng da: "Kem dưỡng da"
-	Phan trang điểm: "Phan trang điểm" Gan nhãn nay sẽ giup mô hình học cách phân loại sản phẩm dựa trên hình ảnh và thông tin mô tả.

4. Cách đánh giá mô hình gồm các chỉ số: 
- độ chính xác (Accuracy), 
- Độ chính xác (Precision)
- Độ nhảy cảm (Recall) 
VD trả lời câu 4: 
Để đánh giá mô hình, bạn có thể sử dụng các chỉ số sau:
-	Độ chính xác (Accuracy): Tỷ lệ phần trăm dự đoán đúng so với tổng số dự đoán. Ví dụ, nếu mô hình dự đoán đúng 80 trên 100 sản phẩm, độ chính xác là 80%.
-	Độ chính xác (Precision): Tỷ lệ dự đoán đúng trong số các dự đoán tích cực. Ví dụ, nếu mô hình dự đoán 50 sản phẩm là "Son môi" và 40 trong số đó là đúng, độ chính xác là 80%.
-	Độ nhạy (Recall): Tỷ lệ sản phẩm thực sự là "Son môi" mà mô hình đã dự đoán đúng. Nếu có 60 sản phẩm thực sự là "Son môi" và mô hình dự đoán đúng 40, độ nhạy là 66.67%.

Sau đó, ở cuối hãy gợi ý dự án dưới dạng JSON gồm các trường:
- project_name
- project_type
- project_description
- dataset (tìm trong database gợi ý cho người dùng)

Trả lời theo cấu trúc:
- Phần tư vấn chi tiết (văn bản)
- Phần JSON (mã code block)
"""
            try:
                response_text = self.aiAssistant.analyze_message(prompt)

                # Cố gắng tách JSON trong block ```json ... ```
                json_match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL)
                if not json_match:
                    return "❌ Không tìm thấy JSON trong phản hồi AI."

                json_str = json_match.group(1)
                data = json.loads(json_str)

                explanation = response_text[:json_match.start()].strip()

                self.project_suggestion = {
                    "project_name": data.get("project_name"),
                    "project_type": data.get("project_type"),
                    "project_description": data.get("project_description"),
                    "dataset": data.get("dataset"),
                }

                return (
                    f"{explanation}\n\n"
                    f"Gợi ý dự án:\n"
                    f"- Tên dự án: {data.get('project_name')}\n"
                    f"- Loại bài toán: {data.get('project_type')}\n"
                    f"- Mô tả dự án: {data.get('project_description')}\n"
                    f"- Dataset gợi ý: {data.get('dataset')}\n\n"
                    f"Nếu bạn đồng ý, hãy nhập 'Tôi đồng ý'."
                )

            except Exception as e:
                return f"❌ Lỗi khi gọi AI: {e}"

        elif type_ == "Lời chào":
            return "Moew~ Moew~ Xin chào!"

        elif type_ == "Giải thích":
            return "Moew moew giải thích cho bạn đây!"

        elif type_ == "Khác":
            return "Moew moew mình không biết, bạn thử hỏi điều khác nhé!"

        else:
            return "Xin lỗi, tôi chưa hiểu yêu cầu của bạn."

    def confirm_create_project(self):
        self.project = AutoMLProject()
        self.project.update_project_type(self.project_suggestion.get("project_type"))
        self.status = "configuring"
        return "✅ Đã tạo project. Bạn có thể tiếp tục cấu hình thêm."
