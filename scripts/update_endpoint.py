#!/usr/bin/env python3
"""
Script tự động cập nhật ENDPOINT URL trong tất cả file HTML
Sử dụng sau khi tạo Google Apps Script mới
"""

import os
import re
import sys

# ============================================================================
# CẤU HÌNH - THAY ĐỔI URL MỚI TẠI ĐÂY
# ============================================================================

# Thay YOUR_NEW_ID bằng ID thực tế từ URL Web App của bạn
# Ví dụ: https://script.google.com/macros/s/AKfycby...YOUR_ID.../exec
NEW_ENDPOINT = "https://script.google.com/macros/s/YOUR_NEW_ID_HERE/exec"

# ============================================================================

# Pattern để tìm ENDPOINT cũ
OLD_PATTERN = r'const ENDPOINT="https://script\.google\.com/macros/s/[^"]+";'

def update_html_files(new_endpoint, directory='.', dry_run=False):
    """
    Cập nhật ENDPOINT trong tất cả file HTML
    
    Args:
        new_endpoint: URL endpoint mới
        directory: Thư mục chứa file HTML
        dry_run: Nếu True, chỉ hiển thị thay đổi mà không ghi file
    
    Returns:
        Tuple (số file đã cập nhật, tổng số file)
    """
    
    print("=" * 70)
    print("🔧 SCRIPT CẬP NHẬT ENDPOINT GOOGLE APPS SCRIPT")
    print("=" * 70)
    
    # Kiểm tra endpoint mới
    if "YOUR_NEW_ID_HERE" in new_endpoint:
        print("\n❌ LỖI: Bạn chưa thay thế NEW_ENDPOINT trong script!")
        print("\n📝 HƯỚNG DẪN:")
        print("1. Mở file: scripts/update_endpoint.py")
        print("2. Tìm dòng: NEW_ENDPOINT = ...")
        print("3. Thay 'YOUR_NEW_ID_HERE' bằng ID thực tế từ Google Apps Script")
        print("\nVí dụ:")
        print('   NEW_ENDPOINT = "https://script.google.com/macros/s/AKfycby...abc123.../exec"')
        sys.exit(1)
    
    print(f"\n✅ Endpoint mới: {new_endpoint}")
    
    # Tìm file HTML
    html_files = []
    for filename in os.listdir(directory):
        if filename.startswith('K6_') and filename.endswith('.html'):
            html_files.append(filename)
        elif filename.startswith('K7_') and filename.endswith('.html'):
            html_files.append(filename)
    
    html_files.sort()
    
    if not html_files:
        print("\n❌ Không tìm thấy file HTML nào!")
        print(f"   Thư mục hiện tại: {os.path.abspath(directory)}")
        sys.exit(1)
    
    print(f"\n📂 Tìm thấy {len(html_files)} file HTML")
    
    if dry_run:
        print("\n⚠️  CHẾ ĐỘ DRY-RUN: Sẽ không ghi file, chỉ hiển thị thay đổi")
    
    print("\n" + "=" * 70)
    print("Đang cập nhật...\n")
    
    updated_count = 0
    error_count = 0
    no_change_count = 0
    
    # Dòng thay thế mới
    new_line = f'const ENDPOINT="{new_endpoint}";'
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        
        try:
            # Đọc file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Tìm ENDPOINT cũ
            old_match = re.search(OLD_PATTERN, content)
            
            if not old_match:
                print(f"⚠️  {filename:20s} - Không tìm thấy ENDPOINT")
                no_change_count += 1
                continue
            
            old_endpoint = old_match.group(0)
            
            # Thay thế
            new_content = re.sub(OLD_PATTERN, new_line, content)
            
            if new_content == content:
                print(f"⚪ {filename:20s} - Đã có endpoint mới (bỏ qua)")
                no_change_count += 1
                continue
            
            # Ghi file (nếu không phải dry-run)
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ {filename:20s} - Đã cập nhật")
            else:
                print(f"🔍 {filename:20s} - Sẽ cập nhật")
                print(f"   Cũ: {old_endpoint}")
                print(f"   Mới: {new_line}")
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ {filename:20s} - Lỗi: {e}")
            error_count += 1
    
    # Tổng kết
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ:")
    print("=" * 70)
    print(f"✅ Đã cập nhật:     {updated_count} file")
    print(f"⚪ Không thay đổi:  {no_change_count} file")
    print(f"❌ Lỗi:             {error_count} file")
    print(f"📁 Tổng số file:    {len(html_files)} file")
    print("=" * 70)
    
    if dry_run:
        print("\n💡 Để thực sự cập nhật file, chạy lại script không có tham số --dry-run")
    elif updated_count > 0:
        print("\n✅ HOÀN THÀNH! Các file HTML đã được cập nhật endpoint mới.")
        print("\n📝 BƯỚC TIẾP THEO:")
        print("1. Mở một file HTML bất kỳ trong trình duyệt")
        print("2. Đăng nhập và làm bài trắc nghiệm")
        print("3. Kiểm tra xem có thông báo '✅ Đã lưu!' không")
        print("4. Kiểm tra Google Sheets để xác nhận dữ liệu đã được lưu")
    
    return updated_count, len(html_files)

def main():
    """Hàm chính"""
    
    # Kiểm tra tham số
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    # Di chuyển đến thư mục gốc nếu đang ở trong scripts/
    if os.path.basename(os.getcwd()) == 'scripts':
        os.chdir('..')
        print("📁 Đã chuyển đến thư mục gốc")
    
    # Cập nhật file
    try:
        update_html_files(NEW_ENDPOINT, dry_run=dry_run)
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng")
        sys.exit(1)

if __name__ == '__main__':
    main()

