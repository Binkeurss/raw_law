import os
import re

def generate_github_urls(input_folder, repo_owner="Binkeurss", repo_name="raw_law", branch="main", github_folder="pdf_dieu_v2"):
    """
    Generate a list of dictionaries containing GitHub URLs for PDFs in the input folder,
    sorted by article number (Dieu_YYY).
    
    Args:
        input_folder (str): Local folder containing the PDFs (e.g., Dieu_YYY_Chuong_X.pdf).
        repo_owner (str): GitHub repository owner (e.g., 'Binkeurss').
        repo_name (str): GitHub repository name (e.g., 'raw_law').
        branch (str): GitHub branch (e.g., 'main').
        github_folder (str): Folder in the GitHub repo where PDFs are stored (e.g., 'pdf_dieu_v2').
    
    Returns:
        list: List of dictionaries with URL, MIME type, filename, and vision flag, sorted by article number.
    """
    base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/refs/heads/{branch}/{github_folder}"
    files_list = []
    
    # Iterate through all .pdf files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            # Match the new filename pattern (Dieu_YYY_Chuong_X.pdf)
            match = re.match(r'Dieu_(\d{3})_Chuong_([IVXLCDM0-9]+)\.pdf', filename)
            if match:
                article_number = int(match.group(1))  # Extract article number for sorting
                files_list.append({
                    "url": f"{base_url}/{filename}",
                    "mime": "application/pdf",
                    "filename": filename,
                    "vision": True,
                    "article_number": article_number
                })
    
    # Sort by article number
    files_list.sort(key=lambda x: x["article_number"])
    
    # Remove article_number from output
    for item in files_list:
        del item["article_number"]
    
    return files_list

def save_files_list(files_list, output_file):
    """
    Save the list of dictionaries to a Python file as a variable named '_files'.
    
    Args:
        files_list (list): List of dictionaries containing file metadata.
        output_file (str): Path to the output Python file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("_files = [\n")
        for item in files_list:
            f.write(f"    {{"
                    f'"url": "{item["url"]}", '
                    f'"mime": "{item["mime"]}", '
                    f'"filename": "{item["filename"]}", '
                    f'"Vision": {str(item["vision"]).lower()}}},\n')
        f.write("]\n")

# Example usage
input_folder = r"E:/intership/web_crawling/selenium_thuvienphapluat/inventory/bo_luat_to_tung_hinh_su"
output_file = r"E:/intership/web_crawling/selenium_thuvienphapluat/pdf_urls_v2.py"
files_list = generate_github_urls(input_folder, repo_owner="Binkeurss", repo_name="raw_law", branch="main", github_folder="bo_luat_to_tung_hinh_su")
save_files_list(files_list, output_file)
print(f"✅ Đã tạo: {output_file}")
print(f"Total PDFs listed: {len(files_list)}")