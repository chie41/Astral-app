# chat_test.py
from service.models.automlproject import AutoMLProject
from service.chatbot.session import ChatSession

def run_chat():
    session = ChatSession()

    print("lấy dataset")

    all_datasets = session.get_all_datasets()
    dataset_info_text = "Hiện tại tôi có một số dataset phù hợp:\n"
        
    if all_datasets:
        for ds in all_datasets:
            dataset_info_text += f"- {ds['name']} (Số mẫu: {ds['size']}, Mô tả: {ds['description']})\n"
    else:
        dataset_info_text += "Chưa tìm thấy dataset phù hợp trong hệ thống.\n"

    print(dataset_info_text)
    print(f"Tổng số dataset: {len(all_datasets)}")

    print("💬 AI: Xin chào! Bạn muốn tạo model gì hoặc cần tôi giải thích điều gì?")
    while True:
        user_input = input("🧑 Bạn: ").strip()

        if user_input.lower() in ["thoát", "exit", "quit"]:
            print("💬 AI: Tạm biệt!")
            break

        # Nếu đang ở trạng thái config, gọi next_step của project
        if session.status == "configuring":
            response = session.project.next_step()
            print("💬 AI:", response)
            continue


        # Ở trạng thái đề xuất, xử lý message qua handle_message
        response = session.handle_message(user_input)
        print("💬 AI:", response)

        # Nếu user đồng ý tạo project (ví dụ nhập "tôi đồng ý")
        if "tôi đồng ý" in user_input.lower() and session.status == "suggesting" and session.project_suggestion:
            confirm_resp = session.confirm_create_project()
            print("💬 AI:", confirm_resp)


if __name__ == "__main__":
    run_chat()
