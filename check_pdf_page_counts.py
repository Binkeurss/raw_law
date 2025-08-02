import os
from PyPDF2 import PdfReader

def check_pdf_page_counts(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    over_one_page = []
    
    for file in pdf_files:
        file_path = os.path.join(folder_path, file)
        try:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            print(f"{file}: {num_pages} trang")
            if num_pages > 1:
                over_one_page.append((file, num_pages))
        except Exception as e:
            print(f"❌ Không đọc được {file}: {e}")
    
    if over_one_page:
        print("\n📌 Các file PDF dài hơn 1 trang:")
        for name, pages in over_one_page:
            print(f"👉 {name}: {pages} trang")
    else:
        print("\n✅ Tất cả file PDF đều chỉ có 1 trang.")

# Ví dụ sử dụng
if __name__ == "__main__":
    folder = "E:/intership/raw_law/inventory/bo_luat_to_tung_hinh_su/pdf"
    check_pdf_page_counts(folder)
