#service/models/automlproject
class AutoMLProject:
    def __init__(self):
        self.project_name = None
        self.project_description = None
        self.project_type = None
        self.dataset = None
        self.first_column = None       # vd: image column
        self.second_column = None      # vd: target column
        self.accuracy = None
        self.training_time = None
        self.steps_done = []

    # Update methods
    def update_project_name(self, name):
        self.project_name = name

    def update_project_description(self, description):
        self.project_description = description

    def update_project_type(self, project_type):
        self.project_type = project_type

    def update_dataset_info(self, dataset_info):
        self.dataset = dataset_info

    def update_columns(self, first_col=None, second_col=None):
        if first_col is not None:
            self.first_column = first_col
        if second_col is not None:
            self.second_column = second_col

    def update_accuracy(self, accuracy):
        self.accuracy = accuracy

    def update_training_time(self, training_time):
        self.training_time = training_time

    def add_step_done(self, step_name):
        if step_name not in self.steps_done:
            self.steps_done.append(step_name)

    # Get methods
    def get_project_name(self):
        return self.project_name

    def get_project_description(self):
        return self.project_description

    def get_project_type(self):
        return self.project_type

    def get_dataset(self):
        return self.dataset

    def get_columns(self):
        return self.first_column, self.second_column

    def get_accuracy(self):
        return self.accuracy

    def get_training_time(self):
        return self.training_time

    def get_steps_done(self):
        return self.steps_done

    # Logic next step based on steps_done
    def next_step(self):
        step_count = len(self.steps_done)

        if step_count == 0:  # Step 1
            if not self.project_type:
                return "Bạn muốn làm loại bài toán nào?"
            if not self.project_name:
                return "Bạn cần phải đặt tên cho bài toán"
            return "Ok"

        elif step_count == 1:  # Step 2
            if not self.dataset:
                return "Vui lòng chọn dataset huấn luyện"
            return "Ok"

        elif step_count == 2:  # Step 3
            if not self.first_column or not self.second_column:
                return "Vui lòng điền đủ hai cột (ví dụ image column và target column)"
            return "Ok"

        elif step_count == 3:  # Step 4
            if not self.accuracy:
                return "Vui lòng điền tỉ lệ chính xác"
            if not self.training_time:
                return "Vui lòng điền thời gian huấn luyện"
            return "Ok"

        return "Ok"
