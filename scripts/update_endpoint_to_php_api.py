#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động cập nhật endpoint từ Google Sheets sang PHP API
File: scripts/update_endpoint_to_php_api.py
"""

import os
import re
import sys
import glob

# Đường dẫn API mới (sửa theo domain hosting của bạn)
NEW_API_ENDPOINT = "https://tinhoc321.com/api/save_result.php"

# Endpoint cũ (Google Sheets)
OLD_ENDPOINT_PATTERN = r'https://script\.google\.com/macros/s/[^/]+/exec'

def update_html_file(filepath):
    """Cập nhật endpoint trong file HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Tìm và thay thế endpoint trong biến const ENDPOINT
        pattern1 = r'(const\s+ENDPOINT\s*=\s*")[^"]*(")'
        if re.search(pattern1, content):
            content = re.sub(pattern1, f'\\g<1>{NEW_API_ENDPOINT}\\g<2>', content)
        
        # Tìm và thay thế endpoint trong URL (nếu có dạng khác)
        if re.search(OLD_ENDPOINT_PATTERN, content):
            content = re.sub(OLD_ENDPOINT_PATTERN, NEW_API_ENDPOINT, content)
        
        # Cập nhật function sendResult để dùng POST thay vì GET
        # Tìm function sendResult
        send_result_pattern = r'(async\s+function\s+sendResult\([^)]+\)\s*\{[^}]*\})'
        
        new_send_result = f'''async function sendResult(name, className, quizId, score, total, duration) {{
      try {{
        const response = await fetch("{NEW_API_ENDPOINT}", {{
          method: 'POST',
          headers: {{
            'Content-Type': 'application/json',
          }},
          body: JSON.stringify({{
            student_name: name,
            class_name: className,
            quiz_id: quizId,
            score: score,
            total: total,
            duration: duration
          }})
        }});
        
        const result = await response.json();
        
        if (result.success) {{
          document.getElementById('send-status').textContent = '✅ Đã lưu!';
          console.log('Saved:', result.data);
        }} else {{
          throw new Error(result.message);
        }}
        
      }} catch (e) {{
        console.error('Save error:', e);
        document.getElementById('send-status').textContent = '⚠️ Không lưu được';
      }}
    }}'''
        
        # Thay thế function sendResult nếu tìm thấy
        if re.search(r'async\s+function\s+sendResult', content):
            # Tìm toàn bộ function (có thể multi-line)
            old_pattern = r'async\s+function\s+sendResult\([^)]+\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
            if re.search(old_pattern, content, re.DOTALL):
                content = re.sub(old_pattern, new_send_result, content, flags=re.DOTALL)
            else:
                # Fallback: thay thế đơn giản hơn
                old_simple = r"const url=`[^`]+`;"
                if re.search(old_simple, content):
                    # Thay thế phần URL fetch
                    content = re.sub(
                        r"(async function sendResult\([^)]+\)\{[^}]*)(const url=`[^`]+`;)",
                        f"\\g<1>{new_send_result}",
                        content,
                        flags=re.DOTALL
                    )
        
        # Nếu có thay đổi, lưu file
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERROR] Lỗi khi xử lý {filepath}: {e}")
        return False


def main():
    """Hàm chính"""
    print("=" * 60)
    print("CAP NHAT ENDPOINT SANG PHP API")
    print("=" * 60)
    print(f"\nEndpoint moi: {NEW_API_ENDPOINT}")
    print(f"Endpoint cu: Google Sheets")
    print("\nDang tim cac file HTML...")
    
    # Tìm tất cả file HTML trong thư mục gốc
    html_files = []
    
    # Tìm file trong thư mục gốc
    patterns = [
        '*.html',
        'K6_*.html',
        'K7_*.html',
        'K6_KIEM_TRA_*.html',
    ]
    
    for pattern in patterns:
        html_files.extend(glob.glob(pattern))
    
    # Loại bỏ các file không cần thiết
    exclude_files = ['index.html', 'login.html', 'login_offline.html', 'quiz_template_with_images.html']
    html_files = [f for f in html_files if os.path.basename(f) not in exclude_files]
    
    # Loại bỏ trùng lặp
    html_files = list(set(html_files))
    
    print(f"\nTim thay {len(html_files)} file HTML")
    print("\nDang cap nhat...\n")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        if update_html_file(filepath):
            print(f"[OK] {filename}")
            updated += 1
        else:
            print(f"[SKIP] {filename} - Khong co thay doi")
            skipped += 1
    
    print("\n" + "=" * 60)
    print("HOAN THANH!")
    print("=" * 60)
    print(f"\nTong ket:")
    print(f"  - Da cap nhat: {updated} files")
    print(f"  - Bo qua: {skipped} files")
    print(f"  - Loi: {errors} files")
    
    if updated > 0:
        print(f"\n[THONG BAO]")
        print(f"  Da cap nhat {updated} file HTML sang endpoint moi!")
        print(f"  Endpoint: {NEW_API_ENDPOINT}")
        print(f"\n[LƯU Ý]")
        print(f"  1. Kiem tra lai cac file da cap nhat")
        print(f"  2. Test chuc nang luu ket qua")
        print(f"  3. Dang ky domain trong api/config.php neu chua co")
    
    print("\n[BUOC TIEP THEO]")
    print("  1. Upload backend_api/ len hosting")
    print("  2. Tao database bang create_database.sql")
    print("  3. Sua api/config.php voi thong tin database")
    print("  4. Test API endpoint")


if __name__ == '__main__':
    main()

