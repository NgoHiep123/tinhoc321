"""
Script tối ưu cuối cùng cho tất cả file quiz
- Ẩn nút "Câu tiếp theo" ở câu cuối, tự động chuyển kết quả
- Áp dụng cho cả K6 và K7
"""

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Pattern 1: K6 files (minified)
PATTERN_K6_OLD = "document.getElementById('next-btn').classList.remove('hidden')}"
PATTERN_K6_NEW = "if(currentQ<quiz.length-1){document.getElementById('next-btn').classList.remove('hidden')}else{setTimeout(showResults,1800)}}"

# Pattern 2: K7 files (readable)
PATTERN_K7_OLD = """      nextBtn.classList.remove('hidden');
      if(currentQuestionIndex === shuffledQuestions.length - 1) nextBtn.textContent = 'Xem kết quả';
      else nextBtn.textContent = 'Câu tiếp theo';"""

PATTERN_K7_NEW = """      if(currentQuestionIndex < shuffledQuestions.length - 1){
        nextBtn.classList.remove('hidden');
        nextBtn.textContent = 'Câu tiếp theo';
      }else{
        setTimeout(showResults, 1800);
      }"""

def update_file(file_path):
    """Update quiz file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Try K6 pattern
    if PATTERN_K6_OLD in content and PATTERN_K6_NEW not in content:
        content = content.replace(PATTERN_K6_OLD, PATTERN_K6_NEW)
        modified = True
    
    # Try K7 pattern  
    if PATTERN_K7_OLD in content:
        content = content.replace(PATTERN_K7_OLD, PATTERN_K7_NEW)
        modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Main"""
    
    print("="*60)
    print("FIX TAT CA FILE QUIZ - AN NUT O CAU CUOI")
    print("="*60)
    
    web_dir = '../Web'
    quiz_files = []
    
    for file in os.listdir(web_dir):
        if file.endswith('.html') and file not in ['index.html', 'login.html', 'login_offline.html']:
            if any(file.startswith(p) for p in ['K6_', 'A1', 'A2', 'A4', 'A5', 'quiz_']):
                quiz_files.append(os.path.join(web_dir, file))
    
    print(f"\nTim thay: {len(quiz_files)} files\n")
    
    updated = 0
    skipped = 0
    
    for file in sorted(quiz_files):
        filename = os.path.basename(file)
        if update_file(file):
            print(f"[OK] {filename}")
            updated += 1
        else:
            print(f"[--] {filename}")
            skipped += 1
    
    print("\n" + "="*60)
    print(f"Cap nhat: {updated} files")
    print(f"Bo qua: {skipped} files")
    print("="*60)
    print("\n[INFO] Thay doi:")
    print("  O cau cuoi:")
    print("    - Nut 'Cau tiep theo' TU DONG AN")
    print("    - Sau 1.8 giay chuyen sang ket qua")
    print("    - Khong hien nut nua!")
    print("\n[TEST] Double-click START_SERVER.bat de test!")

if __name__ == '__main__':
    main()

