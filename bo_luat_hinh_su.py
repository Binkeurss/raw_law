from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
import json


def clean_text(text):
    return text.strip().replace("\xa0", " ").replace("\n", " ").replace("  ", " ")


def crawl_bo_luat():
    url = "https://thuvienphapluat.vn/van-ban/Trach-nhiem-hinh-su/Bo-luat-hinh-su-2015-296661.aspx"

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Bỏ comment nếu muốn xem trình duyệt chạy
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")

    print("🚀 Mở trình duyệt và truy cập trang...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        print("⏳ Đang chờ phần tử `.content1` xuất hiện...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content1"))
        )
        print("✅ Đã tìm thấy phần tử nội dung.")
    except:
        print("❌ Không tìm thấy phần tử `.content1` sau 10 giây.")
        driver.quit()
        return

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    content = soup.select_one(".content1")
    if not content:
        print("❌ Không tìm thấy class .content1 trong HTML!")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        return

    print("🧠 Đang phân tích nội dung...")
    elements = content.find_all(["p"])

    chapters = []
    current_chapter = None
    current_dieu = None

    for el in elements:
        a = el.find("a")
        text = el.get_text(strip=True)

        if a and a.get("name", "").startswith("chuong_") and "_name" not in a["name"]:
            if current_chapter:
                if current_dieu:
                    current_chapter["dieu_list"].append(current_dieu)
                    current_dieu = None
                chapters.append(current_chapter)
            current_chapter = {
                "chuong_id": a["name"],
                "chuong_title": text,
                "chuong_name": "",
                "dieu_list": []
            }
            print(f"📘 Phát hiện chương: {text}")
            continue

        if a and "_name" in a.get("name", "") and current_chapter:
            current_chapter["chuong_name"] = text
            continue

        if a and a.get("name", "").startswith("dieu_"):
            if current_dieu:
                current_chapter["dieu_list"].append(current_dieu)
            current_dieu = {
                "dieu_id": a["name"],
                "dieu_title": text,
                "dieu_content": []
            }
            print(f"  📄 Phát hiện điều: {text}")
            continue

        if current_dieu and text:
            current_dieu["dieu_content"].append(text)

    if current_dieu and current_chapter:
        current_chapter["dieu_list"].append(current_dieu)
    if current_chapter:
        chapters.append(current_chapter)

    print(f"📚 Tổng số chương: {len(chapters)}")
    print("💾 Đang ghi dữ liệu ra file JSON...")

    output = []
    for chuong in chapters:
        output.append({
            "chuong_id": chuong["chuong_id"],
            "chuong_title": clean_text(chuong["chuong_title"]),
            "chuong_name": clean_text(chuong["chuong_name"]),
            "dieu_list": [
                {
                    "dieu_id": d["dieu_id"],
                    "dieu_title": clean_text(d["dieu_title"]),
                    "dieu_content": clean_text(" ".join(d["dieu_content"]))
                } for d in chuong["dieu_list"]
            ]
        })

    with open("bo_luat_hinh_su_2015.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("🎉 Hoàn tất! File đã được lưu: bo_luat_hinh_su_2015.json")


if __name__ == "__main__":
    crawl_bo_luat()
