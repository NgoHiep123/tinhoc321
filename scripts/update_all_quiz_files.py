"""
Script cập nhật tất cả file quiz với:
- Ẩn nút "Câu tiếp theo" ở câu cuối
- Tự động chuyển sang kết quả sau 2 giây
"""

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def update_quiz_file(file_path):
    """Cập nhật logic quiz"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Thay đổi checkAnswer để ẩn nút ở câu cuối
    old_pattern = "document.getElementById('next-btn').classList.remove('hidden')}"
    
    if old_pattern in content:
        # Thay bằng logic mới
        new_code = "if(currentQ<quiz.length-1){document.getElementById('next-btn').classList.remove('hidden')}else{setTimeout(showResults,2000)}}"
        content = content.replace(old_pattern, new_code)
        
        # Lưu lại
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False

def main():
    """Main function"""
    
    print("="*60)
    print("CAP NHAT TAT CA FILE QUIZ")
    print("="*60)
    
    web_dir = '../Web'
    
    # Tìm tất cả file HTML quiz
    quiz_files = []
    for file in os.listdir(web_dir):
        if (file.startswith('K6_') or file.startswith('A') or file == 'quiz_template_with_images.html'):
            if file.endswith('.html') and file not in ['index.html', 'login.html', 'login_offline.html']:
                quiz_files.append(os.path.join(web_dir, file))
    
    print(f"\nTim thay {len(quiz_files)} file quiz\n")
    
    updated = 0
    skipped = 0
    
    for file in sorted(quiz_files):
        filename = os.path.basename(file)
        if update_quiz_file(file):
            print(f"[OK] {filename}")
            updated += 1
        else:
            print(f"[SKIP] {filename} - Da cap nhat roi")
            skipped += 1
    
    print("\n" + "="*60)
    print("HOAN THANH!")
    print("="*60)
    print(f"\nTong ket:")
    print(f"  - Da cap nhat: {updated} files")
    print(f"  - Bo qua: {skipped} files")
    print(f"\n[INFO] Thay doi:")
    print(f"  - O cau cuoi: Nut 'Cau tiep theo' TU DONG AN")
    print(f"  - Sau 2 giay: Tu dong chuyen sang ket qua")
    print(f"\n[TEST] Mo START_SERVER.bat va test lai!")

if __name__ == '__main__':
    main()

