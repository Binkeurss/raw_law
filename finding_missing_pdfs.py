import os
import re
from collections import defaultdict

def find_missing_articles(pdf_folder):
    """
    Tìm các điều còn thiếu trong thư mục PDF dựa trên quy ước đặt tên file
    """
    # Tạo dictionary để lưu trữ thông tin theo chương
    chapter_data = defaultdict(dict)
    
    # Lấy danh sách file PDF trong thư mục
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    print(f"Tìm thấy {len(pdf_files)} file PDF trong thư mục")
    
    # Biểu thức chính quy để trích xuất thông tin từ tên file
    pattern = r'BLTTHS_Dieu_(\d{4})_Chuong([IVXLCDM]+|\d+)\.pdf'
    
    for filename in pdf_files:
        match = re.match(pattern, filename)
        if match:
            article_num = int(match.group(1))  # Số điều (dạng số)
            chapter_num = match.group(2)        # Số chương (dạng chuỗi)
            
            # Lưu thông tin điều vào chương tương ứng
            if chapter_num not in chapter_data:
                chapter_data[chapter_num] = {
                    'min_article': article_num,
                    'max_article': article_num,
                    'articles': set()
                }
            else:
                if article_num < chapter_data[chapter_num]['min_article']:
                    chapter_data[chapter_num]['min_article'] = article_num
                if article_num > chapter_data[chapter_num]['max_article']:
                    chapter_data[chapter_num]['max_article'] = article_num
            
            chapter_data[chapter_num]['articles'].add(article_num)
    
    # Kiểm tra các điều còn thiếu
    missing_articles = []
    
    for chapter, data in chapter_data.items():
        min_art = data['min_article']
        max_art = data['max_article']
        existing_articles = data['articles']
        
        # Tạo tập hợp tất cả các số điều nên có trong khoảng min-max
        all_articles = set(range(min_art, max_art + 1))
        
        # Tìm các điều thiếu
        missing = all_articles - existing_articles
        
        if missing:
            print(f"\nChương {chapter}: Thiếu {len(missing)} điều")
            for art_num in sorted(missing):
                # Định dạng số điều thành 4 chữ số (0010, 0100, 1000)
                formatted_num = str(art_num).zfill(4)
                missing_filename = f"BLHS_Dieu_{formatted_num}_Chuong{chapter}.pdf"
                print(f"  - Thiếu: {missing_filename}")
                missing_articles.append(missing_filename)
        else:
            print(f"\nChương {chapter}: Đầy đủ các điều từ {min_art} đến {max_art}")
    
    return missing_articles

if __name__ == "__main__":
    # Thư mục chứa các file PDF
    pdf_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_to_tung_hinh_su/pdf"
    
    # Kiểm tra thư mục tồn tại
    if not os.path.exists(pdf_folder):
        print(f"Lỗi: Thư mục '{pdf_folder}' không tồn tại!")
        exit()
    
    print(f"Bắt đầu kiểm tra các điều còn thiếu trong thư mục: {pdf_folder}")
    missing = find_missing_articles(pdf_folder)
    
    if missing:
        print(f"\nTổng cộng thiếu {len(missing)} điều:")
        for filename in missing:
            print(f"  - {filename}")
    else:
        print("\nKhông thiếu điều nào! Tất cả các điều đều đã được tạo đầy đủ.")