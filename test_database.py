# test_database.py

import tkinter as tk
from tkinter import filedialog, messagebox
from database.upload_csv_file import upload_csv_file
from database.dataset_manager import create_db, get_all_dataset_info

if __name__ == "__main__":
    datasets = get_all_dataset_info()
    for d in datasets:
        print(d)