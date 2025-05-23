from service.chatbot.session import ChatSession

def test_update():
    chat = ChatSession()

    # Giả lập có gợi ý project sẵn (để tránh nó hiểu là create_project)
    chat.project_suggestion = {
        "project_name": "Dự án cũ",
        "project_type": "Image Classification",
        "project_description": "Mô tả ban đầu",
        "dataset": "DatasetA"
    }

    user_message = "Đổi tên dự án thành Dự án Mới và dùng dataset DatasetB"

    print("===== Phản hồi từ handle_message =====")
    for response in chat.handle_message(user_message):
        if isinstance(response, str):
            print(response)
        elif hasattr(response, "__iter__"):  # nếu là generator
            for r in response:
                print(r)

if __name__ == "__main__":
    test_update()
