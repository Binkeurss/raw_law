import json
import os

def convert_all_json_to_txt(json_folder, output_folder):
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # Duyệt từng file trong thư mục JSON
    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            json_path = os.path.join(json_folder, filename)
            txt_path = os.path.join(output_folder, filename.replace(".json", ".txt"))

            try:
                # Đọc dữ liệu từ JSON
                with open(json_path, "r", encoding="utf-8") as f:
                    chapter = json.load(f)

                # Ghi ra file TXT
                with open(txt_path, "w", encoding="utf-8") as f:
                    # Tiêu đề chương
                    f.write(f"{chapter.get('chuong_title', '')}\n")
                    f.write(f"{chapter.get('chuong_name', '')}\n\n")

                    # Danh sách điều
                    for dieu in chapter.get("dieu_list", []):
                        f.write(f"{dieu.get('dieu_title', '')}\n")
                        f.write(f"{dieu.get('dieu_content', '')}\n")
                        f.write("\n")

                print(f"✅ Đã convert: {filename} → {os.path.basename(txt_path)}")

            except Exception as e:
                print(f"❌ Lỗi với {filename}: {e}")

json_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_hinh_su/json"
output_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_hinh_su/txt"

convert_all_json_to_txt(json_folder, output_folder)
