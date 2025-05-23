#service/models/chatbot
from models.automlproject import AutoMLProject
class Chatbot:
    def __init__(self):
        self.sessions = {}  # key: user_id, value: dict chứa history + project

    def start_session(self, user_id):
        self.sessions[user_id] = {
            "history": [],
            "project": AutoMLProject()
        }

    def end_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]

    def handle_message(self, user_id, message):
        if user_id not in self.sessions:
            self.start_session(user_id)

        session = self.sessions[user_id]
        session["history"].append({"user": message})
    
        yield session.handle_message
