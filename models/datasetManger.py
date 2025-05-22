import sqlite3
import pandas as pd
import os

class DatasetManager:
    def __init__(self, db_path="datasets.db"):
        self.db_path = db_path
        self.create_db()
    
    def create_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            description TEXT,
            data_type TEXT,
            size INTEGER,
            source TEXT,
            tags TEXT,
            status TEXT CHECK(status IN ('labeled', 'unlabeled')) DEFAULT 'unlabeled'
        )
        ''')
        conn.commit()
        conn.close()
        print("✅ Database và bảng 'datasets' đã được tạo hoặc xác nhận tồn tại.")

    def insert_dataset(self, name, path, description, data_type, size, source, tags, status='unlabeled'):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
        INSERT INTO datasets (name, path, description, data_type, size, source, tags, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, path, description, data_type, size, source, tags, status))
        conn.commit()
        conn.close()
        print(f"✅ Dataset '{name}' đã được thêm vào database.")

    def get_all_dataset_info(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT name, path, description, status FROM datasets")
        rows = c.fetchall()
        conn.close()

        results = []
        for name, path, description, status in rows:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path, nrows=5)
                    full_df = pd.read_csv(path)
                    info = {
                        "name": name,
                        "description": description,
                        "status": status,
                        "size": len(full_df),
                        "columns": list(df.columns)
                    }
                    results.append(info)
                except Exception as e:
                    print(f"❌ Không thể đọc {path}: {e}")
            else:
                print(f"⚠️ Dataset path không tồn tại: {path}")

        return results
