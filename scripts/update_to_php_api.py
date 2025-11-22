#!/usr/bin/env python3
"""
Script tự động chuyển từ Google Sheets sang PHP API
"""

import os
import re
import sys

# API endpoint mới
NEW_API_URL = "https://tinhoc321.com/api/save_result.php"

# Code JavaScript mới
NEW_SEND_RESULT_FUNCTION = '''async function sendResult(name, className, quizId, score, total, duration) {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        student_name: name,
        class_name: className,
        quiz_id: quizId,
        score: score,
        total: total,
        duration: duration
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      document.getElementById('send-status').textContent = '✅ Đã lưu!';
      console.log('Result saved:', result.data);
    } else {
      throw new Error(result.message || 'Unknown error');
    }
    
  } catch (e) {
    console.error('Save error:', e);
    document.getElementById('send-status').textContent = '⚠️ Không lưu được: ' + e.message;
  }
}'''

def update_html_file(filepath):
    """Cập nhật một file HTML"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Thay đổi ENDPOINT
    content = re.sub(
        r'const ENDPOINT="https://script\.google\.com/macros/s/[^"]+";',
        f'const API_ENDPOINT="{NEW_API_URL}";',
        content
    )
    
    # 2. Thay đổi function sendResult
    # Tìm function cũ
    old_function_pattern = r'async function sendResult\([^)]+\)\s*\{[^}]+\}'
    
    if re.search(old_function_pattern, content):
        content = re.sub(
            old_function_pattern,
            NEW_SEND_RESULT_FUNCTION,
            content,
            flags=re.DOTALL
        )
        return content, True
    else:
        print(f"  ⚠️ Không tìm thấy function sendResult trong {filepath}")
        return content, False

def main():
    """Hàm chính"""
    
    print("=" * 70)
    print("🔄 CHUYỂN ĐỔI TỪ GOOGLE SHEETS SANG PHP API")
    print("=" * 70)
    print(f"\n✅ API mới: {NEW_API_URL}\n")
    
    # Di chuyển đến thư mục gốc
    if os.path.basename(os.getcwd()) == 'scripts':
        os.chdir('..')
    
    # Tìm file HTML
    html_files = []
    for filename in os.listdir('.'):
        if (filename.startswith('K6_') or filename.startswith('K7_')) and filename.endswith('.html'):
            html_files.append(filename)
    
    html_files.sort()
    
    if not html_files:
        print("❌ Không tìm thấy file HTML nào!")
        sys.exit(1)
    
    print(f"📂 Tìm thấy {len(html_files)} file HTML\n")
    print("Đang cập nhật...\n")
    
    updated_count = 0
    error_count = 0
    
    for filename in html_files:
        try:
            new_content, success = update_html_file(filename)
            
            if success:
                # Ghi file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ {filename:20s} - Đã cập nhật")
                updated_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            print(f"❌ {filename:20s} - Lỗi: {e}")
            error_count += 1
    
    # Tổng kết
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ:")
    print("=" * 70)
    print(f"✅ Đã cập nhật:  {updated_count}/{len(html_files)} file")
    print(f"❌ Lỗi:          {error_count}/{len(html_files)} file")
    print("=" * 70)
    
    if updated_count > 0:
        print("\n✅ HOÀN THÀNH!")
        print("\n📝 BƯỚC TIẾP THEO:")
        print("1. Upload file PHP lên hosting (api/save_result.php)")
        print("2. Tạo database MySQL và import schema")
        print("3. Cấu hình api/config.php")
        print("4. Test một file HTML bất kỳ")
        print("5. Kiểm tra kết quả trong dashboard")

if __name__ == '__main__':
    main()

