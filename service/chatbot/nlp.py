def analyze_message(text: str):
    # Gọi AI hoặc xử lý text thô
    # Ví dụ trả về loại bài toán và câu trả lời đơn giản
    if "ảnh" in text or "image" in text:
        return "image classification", "Bạn chọn Image Classification."
    elif "text" in text:
        return "text classification", "Bạn chọn Text Classification."
    else:
        return "tabular classification", "Bạn chọn Tabular Classification."
