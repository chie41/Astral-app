import os
import pandas as pd
from database.dataset_manager import insert_dataset  # import từ file của bạn

def upload_csv_file(filepath, description="", source="", tags="", status="unlabeled"):
    if not os.path.exists(filepath):
        print(f"⚠️ File không tồn tại: {filepath}")
        return False

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Lỗi đọc file CSV: {e}")
        return False

    name = os.path.splitext(os.path.basename(filepath))[0]
    data_type = "csv"
    size = len(df)

    insert_dataset(name, filepath, description, data_type, size, source, tags, status)
    print(f"✅ Upload và ghi database thành công cho dataset '{name}'")
    return True
