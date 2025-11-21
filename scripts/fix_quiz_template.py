"""
Script sửa template cho tất cả file quiz HTML
- Ẩn nút "Câu tiếp theo" ở câu cuối
- Cải thiện màn hình kết quả
"""

import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix_quiz_html(file_path):
    """Sửa file HTML quiz"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm và thay thế function checkAnswer
    # Thêm logic ẩn nút ở câu cuối
    old_check = r"document\.getElementById\('next-btn'\)\.classList\.remove\('hidden'\)"
    new_check = """if(currentQ < quiz.length - 1){document.getElementById('next-btn').classList.remove('hidden')}else{setTimeout(showResults,1500)}"""
    
    content = re.sub(old_check, new_check, content)
    
    # Lưu lại
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Sửa tất cả file quiz"""
    
    print("="*60)
    print("SUA TEMPLATE QUIZ - AN NUT 'CAU TIEP THEO' O CAU CUOI")
    print("="*60)
    
    web_dir = '../Web'
    
    # Tìm tất cả file quiz
    quiz_files = []
    for file in os.listdir(web_dir):
        if file.startswith(('K6_', 'A1.html', 'A2.html', 'A4.html', 'A5.html', 'A1_enhanced.html')):
            if file.endswith('.html'):
                quiz_files.append(os.path.join(web_dir, file))
    
    print(f"\nTim thay {len(quiz_files)} file quiz")
    print("\nDang sua...")
    
    fixed = 0
    for file in quiz_files:
        try:
            fix_quiz_html(file)
            filename = os.path.basename(file)
            print(f"[OK] {filename}")
            fixed += 1
        except Exception as e:
            print(f"[ERROR] {os.path.basename(file)}: {e}")
    
    print("\n" + "="*60)
    print("HOAN THANH!")
    print("="*60)
    print(f"\nDa sua {fixed}/{len(quiz_files)} files")
    print("\n[INFO] Gio o cau cuoi:")
    print("  - Nut 'Cau tiep theo' se TU DONG AN")
    print("  - Sau 1.5 giay tu dong chuyen sang ket qua")
    print("\n[TEST] Mo lai cac file HTML va test!")

if __name__ == '__main__':
    main()

