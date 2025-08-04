import json
import os
import re

from fpdf import FPDF

def split_chapters_to_files(chapters, output_dir="inventories"):
    """
    Tách từng chương trong danh sách `chapters` thành file JSON riêng.

    Args:
        chapters (list): Danh sách chương (list of dict) như bạn cung cấp.
        output_dir (str): Thư mục để lưu các file chương. Mặc định là "output_chapters".
    """
    # Tạo thư mục nếu chưa có
    os.makedirs(output_dir, exist_ok=True)

    for chapter in chapters:
        # Lấy ID chương, ví dụ: "chuong_1"
        chuong_id = chapter.get("chuong_id", "unknown")
        filename = f"{chuong_id}.json"

        # Đường dẫn đầy đủ tới file
        filepath = os.path.join(output_dir, filename)

        # Ghi nội dung chương vào file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(chapter, f, ensure_ascii=False, indent=2)

        print(f"✅ Đã lưu: {filepath}")

import sys
import os

# Thêm thư mục cha vào PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(project_root)

json_path = r"E:/intership/raw_law/thi_hanh_an_hinh_su.json"
output_folder = r"E:/intership/raw_law/inventory/thi_hanh_an_hinh_su/json"


with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)  # Đây là list chứa các chương

split_chapters_to_files(data, output_folder)
