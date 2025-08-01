import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
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

def convert_roman_to_int(roman):
    """Chuyển đổi số La Mã thành số thập phân"""
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 
        'C': 100, 'D': 500, 'M': 1000
    }
    total = 0
    prev_value = 0
    
    for char in reversed(roman.upper()):
        value = roman_values.get(char, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    return total

def split_articles(input_file):
    try:
        print(f"Reading file: {input_file}")
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = content.strip()
        
        # Extract chapter title and number
        chapter_match = re.match(r'Chương\s+([IVXLCDM]+|[0-9]+)\s*([^\n]*)', content, re.IGNORECASE | re.MULTILINE)
        chapter_title = ""
        chapter_number = ""
        chapter_roman = ""
        
        if chapter_match:
            chapter_number_raw = chapter_match.group(1)
            chapter_title_text = chapter_match.group(2).strip() if chapter_match.group(2) else "Untitled Chapter"
            
            if re.match(r'^[IVXLCDM]+$', chapter_number_raw, re.IGNORECASE):
                chapter_roman = chapter_number_raw.upper()
                chapter_number = str(convert_roman_to_int(chapter_number_raw))
            else:
                chapter_number = chapter_number_raw
                chapter_roman = f"Chapter{chapter_number}"
            
            chapter_title = "Bộ luật hình sự - Chương " + chapter_roman
            print(f"Found chapter: {chapter_title} (Number: {chapter_number}, Title text: {chapter_title_text})")
        else:
            print(f"Warning: No chapter title found in {input_file}. Using default chapter number from filename.")
            filename = os.path.basename(input_file)
            chapter_number_match = re.search(r'chuong_(\d+)\.txt', filename, re.IGNORECASE)
            if chapter_number_match:
                chapter_number = chapter_number_match.group(1)
                chapter_roman = f"Chapter{chapter_number}"
                chapter_title = f"Bộ luật hình sự - Chương {chapter_number}"
                print(f"Using chapter number {chapter_number} from filename")
            else:
                print(f"Error: Cannot determine chapter number for {input_file}")
                return "", "", "", [], []
        
        # Split content into articles
        articles_raw = re.split(r'\n\s*(?=Điều\s*\d+\.)', content, flags=re.MULTILINE)
        article_list = []
        article_numbers = []
        
        for article in articles_raw:
            article = article.strip()
            if article.startswith("Chương") and not article.startswith("Điều"):
                continue
            
            if "Điều" in article:
                article_number_match = re.search(r'Điều\s*(\d+)\.', article)
                if article_number_match:
                    article_number = article_number_match.group(1)
                    article_numbers.append(article_number)
                    article_list.append(article)
                    print(f"Found article {article_number}")
                else:
                    print(f"Warning: No article number found in article: {article[:50]}...")
        
        print(f"Found {len(article_list)} articles in {input_file}")
        return chapter_title, chapter_number, chapter_roman, article_list, article_numbers
    except Exception as e:
        print(f"Error in split_articles for {input_file}: {str(e)}")
        return "", "", "", [], []

def create_pdf_for_article(chapter_title, chapter_number, chapter_roman, article, article_number, output_folder):
    try:
        print(f"Creating PDF for Article {article_number}")
        print(f"Article content preview: {article[:100]}...")
        
        # Tạo tên file
        article_number_padded = article_number.zfill(4)
        pdf_filename = f"BLHS_Dieu_{article_number_padded}_Chuong{chapter_roman}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        # Tạo document với lề nhỏ hơn
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
        
        # Style cho tiêu đề chương
        chapter_style = ParagraphStyle(
            name='ChapterTitle',
            parent=styles['Normal'],
            fontName='Arial-Bold',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=6*mm
        )
        
        # Style cho tiêu đề điều (in đậm)
        article_title_style = ParagraphStyle(
            name='ArticleTitle',
            parent=styles['Normal'],
            fontName='Arial-Bold',
            fontSize=10,
            spaceAfter=4,
            leading=12
        )
        
        # Style cho nội dung điều
        content_style = ParagraphStyle(
            name='Content',
            parent=styles['Normal'],
            fontName='Arial',
            fontSize=10,
            alignment=TA_JUSTIFY,
            leading=12  # Khoảng cách giữa các dòng
        )
        
        # Chuẩn bị nội dung
        story = []
        
        # Thêm tiêu đề chương
        chap_para = Paragraph(chapter_title, chapter_style)
        story.append(chap_para)
        
        # Tách tiêu đề điều và nội dung
        # Tìm vị trí kết thúc của tiêu đề điều (sau số điều)
        title_end = article.find('.') + 1
        if title_end > 0:
            article_title = article[:title_end].strip()
            article_content = article[title_end:].strip()
        else:
            article_title = article
            article_content = ""
        
        # Thêm tiêu đề điều (in đậm)
        title_para = Paragraph(article_title, article_title_style)
        story.append(title_para)
        
        # Xử lý nội dung điều
        # Giữ nguyên các điểm con (a, b, c) nhưng loại bỏ các xuống dòng không mong muốn
        cleaned_text = article_content.replace('\n', ' ')  # Thay thế tất cả dấu xuống dòng bằng khoảng trắng
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Loại bỏ khoảng trắng thừa
        
        # Thêm nội dung điều
        content_para = Paragraph(cleaned_text, content_style)
        story.append(content_para)
        
        # Build PDF
        doc.build(story)
        print(f"✅ Đã tạo: {pdf_path}")
    except Exception as e:
        print(f"Error creating PDF for article {article_number}: {str(e)}")

def convert_txt_folder_to_pdfs(input_folder, output_folder):
    try:
        print("Starting script...")
        print(f"Checking input folder: {input_folder}")
        if not os.path.exists(input_folder):
            print(f"Error: Input folder {input_folder} does not exist")
            return
        
        # Đăng ký font
        register_fonts()
        
        files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
        print(f"Found {len(files)} .txt files: {files}")
        if not files:
            print("No .txt files found in input folder")
            return
        
        os.makedirs(output_folder, exist_ok=True)
        
        for filename in sorted(files):
            input_file = os.path.join(input_folder, filename)
            print(f"Processing file: {filename}")
            chapter_title, chapter_number, chapter_roman, articles, article_numbers = split_articles(input_file)
            if not articles:
                print(f"No articles found in {filename}")
                continue
            for article, article_number in zip(articles, article_numbers):
                create_pdf_for_article(chapter_title, chapter_number, chapter_roman, article, article_number, output_folder)
    except Exception as e:
        print(f"Error in convert_txt_folder_to_pdfs: {str(e)}")

# Input and output folders
input_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_hinh_su/txt"
output_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_hinh_su/pdf"

# Run the conversion
convert_txt_folder_to_pdfs(input_folder, output_folder)