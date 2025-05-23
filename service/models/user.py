#service/models/user
from models.automlproject import AutoMLProject
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_project = None
        self.history = []

    def start_new_project(self):
        self.current_project = AutoMLProject()

    def add_to_history(self, message):
        self.history.append(message)
