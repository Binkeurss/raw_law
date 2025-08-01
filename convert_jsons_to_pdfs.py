import os
import json
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# Đăng ký font Arial Unicode để hỗ trợ tiếng Việt
def register_fonts():
    try:
        # Đường dẫn đến font Arial trong Windows
        arial_path = "C:/Windows/Fonts/arial.ttf"
        arial_bold_path = "C:/Windows/Fonts/arialbd.ttf"
        
        pdfmetrics.registerFont(TTFont("Arial", arial_path))
        pdfmetrics.registerFont(TTFont("Arial-Bold", arial_bold_path))
        return True
    except:
        # Fallback nếu không tìm thấy font
        print("Warning: Arial font not found. Using default font.")
        return False

def create_pdf_for_article(chuong_title, dieu, output_folder):
    try:
        # Trích xuất số điều
        dieu_title = dieu['dieu_title']
        dieu_content = dieu['dieu_content']
        
        # Trích xuất số chương từ chuong_title
        chapter_number = re.search(r'Chương\s+([IVXLCDM]+|\d+)', chuong_title, re.IGNORECASE)
        chapter_number = chapter_number.group(1) if chapter_number else ""
        
        # Trích xuất số điều từ dieu_title
        article_number_match = re.search(r'Điều\s*(\d+)\.', dieu_title)
        article_number = article_number_match.group(1) if article_number_match else "unknown"
        
        # Tạo tên file
        article_number_padded = article_number.zfill(4)
        pdf_filename = f"BLTTHS_Dieu_{article_number_padded}_Chuong{chapter_number}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        # Tạo document với lề
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4,
            leftMargin=15*mm,
            rightMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        
        # Tạo style
        styles = getSampleStyleSheet()
        
        # Style cho tiêu đề chương (Bộ luật tố tụng hình sự - Chương I)
        chapter_style = ParagraphStyle(
            name='ChapterTitle',
            parent=styles['Normal'],
            fontName='Arial-Bold',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=8*mm
        )
        
        # Style cho tiêu đề điều (in đậm)
        article_title_style = ParagraphStyle(
            name='ArticleTitle',
            parent=styles['Normal'],
            fontName='Arial-Bold',
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=4*mm,
            leading=14
        )
        
        # Style cho nội dung điều
        content_style = ParagraphStyle(
            name='Content',
            parent=styles['Normal'],
            fontName='Arial',
            fontSize=11,
            alignment=TA_JUSTIFY,
            leading=14  # Khoảng cách giữa các dòng
        )
        
        # Chuẩn bị nội dung
        story = []
        
        # 1. Thêm tiêu đề chương: "Bộ luật tố tụng hình sự - Chương I"
        chapter_full_title = f"Bộ luật tố tụng hình sự - {chuong_title}"
        chap_para = Paragraph(chapter_full_title, chapter_style)
        story.append(chap_para)
        
        # 2. Thêm tiêu đề điều (Điều 1. Nhiệm vụ của Bộ luật tố tụng hình sự)
        title_para = Paragraph(dieu_title, article_title_style)
        story.append(title_para)
        
        # 3. Thêm nội dung điều
        content_para = Paragraph(dieu_content, content_style)
        story.append(content_para)
        
        # Build PDF
        doc.build(story)
        print(f"✅ Đã tạo: {pdf_path}")
        return True
    except Exception as e:
        print(f"Error creating PDF for article: {str(e)}")
        return False

def convert_json_folder_to_pdfs(input_folder, output_folder):
    try:
        print("Starting JSON to PDF conversion...")
        print(f"Checking input folder: {input_folder}")
        if not os.path.exists(input_folder):
            print(f"Error: Input folder {input_folder} does not exist")
            return
        
        # Đăng ký font
        register_fonts()
        
        files = [f for f in os.listdir(input_folder) if f.endswith(".json")]
        print(f"Found {len(files)} JSON files: {files}")
        if not files:
            print("No JSON files found in input folder")
            return
        
        os.makedirs(output_folder, exist_ok=True)
        
        for filename in sorted(files):
            input_file = os.path.join(input_folder, filename)
            print(f"Processing file: {filename}")
            
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Lấy thông tin chương
            chuong_title = data.get("chuong_title", "")
            dieu_list = data.get("dieu_list", [])
            
            if not dieu_list:
                print(f"No articles found in {filename}")
                continue
            
            print(f"Found {len(dieu_list)} articles in chapter {chuong_title}")
            
            # Tạo PDF cho từng điều
            for dieu in dieu_list:
                create_pdf_for_article(
                    chuong_title, 
                    dieu, 
                    output_folder
                )
                
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Error in convert_json_folder_to_pdfs: {str(e)}")

# Input and output folders
input_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_to_tung_hinh_su/json"
output_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_to_tung_hinh_su/pdf"

# Run the conversion
convert_json_folder_to_pdfs(input_folder, output_folder)