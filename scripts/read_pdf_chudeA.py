"""
Script đọc PDF Sách giáo khoa Tin 6 - Chủ đề A
"""

import PyPDF2
import sys
import io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_pdf_content(pdf_path):
    """Đọc nội dung PDF"""
    print("Dang doc file PDF...")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"Tong so trang: {total_pages}")
            
            # Đọc 30 trang đầu (chủ đề A thường ở đầu sách)
            text = ""
            for i in range(min(30, total_pages)):
                page = pdf_reader.pages[i]
                text += f"\n{'='*60}\nTRANG {i+1}\n{'='*60}\n"
                text += page.extract_text()
            
            return text
    except Exception as e:
        print(f"Loi doc PDF: {e}")
        return None

# Đọc file
pdf_path = "../Sach_giao_khoa_Tin_6.pdf"
content = read_pdf_content(pdf_path)

if content:
    # Lưu ra file text
    with open("tin6_chudeA.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("\nDa luu noi dung vao tin6_chudeA.txt")
    
    # In ra màn hình một phần
    print("\n" + "="*60)
    print("NOI DUNG 2000 KY TU DAU:")
    print("="*60)
    print(content[:2000])

