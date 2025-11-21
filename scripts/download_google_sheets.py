"""
Script tự động tải kết quả từ Google Sheets
Yêu cầu: pip install gspread oauth2client pandas
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys
import os

def download_results(sheet_name='25-26-Ketqua_tracnghiem', credentials_file='credentials.json'):
    """
    Tải dữ liệu từ Google Sheets về file CSV
    
    Args:
        sheet_name: Tên file Google Sheets
        credentials_file: File credentials từ Google Cloud Console
    
    Returns:
        DataFrame chứa dữ liệu
    """
    
    print("=" * 60)
    print("📥 TẢI KẾT QUẢ TỪ GOOGLE SHEETS")
    print("=" * 60)
    
    # Kiểm tra file credentials
    if not os.path.exists(credentials_file):
        print(f"\n❌ KHÔNG TÌM THẤY FILE: {credentials_file}")
        print("\n📋 HƯỚNG DẪN TẠO CREDENTIALS:")
        print("1. Truy cập: https://console.cloud.google.com")
        print("2. Tạo project mới (hoặc chọn project có sẵn)")
        print("3. Enable Google Sheets API")
        print("4. Tạo Service Account:")
        print("   - IAM & Admin → Service Accounts → Create")
        print("   - Tải về file JSON, đổi tên thành 'credentials.json'")
        print("5. Copy email service account")
        print("6. Mở Google Sheets → Share → Dán email → Cấp quyền 'Editor'")
        print("\n⚠️  Sau khi hoàn thành, chạy lại script này.")
        sys.exit(1)
    
    print(f"✅ Tìm thấy credentials: {credentials_file}")
    
    # Kết nối Google Sheets
    try:
        print("🔗 Đang kết nối Google Sheets API...")
        
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        
        print(f"✅ Kết nối thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi khi kết nối: {e}")
        print("\n💡 KIỂM TRA:")
        print("- File credentials.json có đúng format không?")
        print("- Đã enable Google Sheets API chưa?")
        sys.exit(1)
    
    # Mở sheet
    try:
        print(f"📂 Đang mở sheet: {sheet_name}...")
        sheet = client.open(sheet_name).sheet1
        print(f"✅ Mở sheet thành công!")
        
    except Exception as e:
        print(f"❌ Không thể mở sheet: {e}")
        print("\n💡 KIỂM TRA:")
        print(f"- Tên sheet có đúng là '{sheet_name}' không?")
        print("- Đã share sheet với email service account chưa?")
        print(f"  (Email trong file {credentials_file}, field 'client_email')")
        sys.exit(1)
    
    # Lấy dữ liệu
    try:
        print("📊 Đang tải dữ liệu...")
        data = sheet.get_all_records()
        
        if len(data) == 0:
            print("⚠️  Sheet rỗng hoặc không có header!")
            sys.exit(1)
        
        df = pd.DataFrame(data)
        print(f"✅ Đã tải {len(df)} bản ghi")
        
        # Hiển thị 5 dòng đầu
        print("\n📋 Preview dữ liệu:")
        print("-" * 60)
        print(df.head())
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc dữ liệu: {e}")
        sys.exit(1)
    
    # Lưu file CSV
    output_file = '../test_results.csv'
    try:
        print(f"\n💾 Đang lưu file: {output_file}...")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Đã lưu thành công!")
        
        # Kiểm tra file
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📁 Kích thước file: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)
    print(f"📌 File đã được lưu tại: {output_file}")
    print("📌 Bước tiếp theo: Chạy pipeline xây dựng KG")
    print("   cd ../KG_Design")
    print("   python build_kg_grade7.py")
    print("=" * 60)
    
    return df

def main():
    """Hàm chính"""
    
    # Kiểm tra dependencies
    try:
        import gspread
        import oauth2client
    except ImportError:
        print("❌ Thiếu thư viện! Cài đặt:")
        print("pip install gspread oauth2client pandas")
        sys.exit(1)
    
    # Tải dữ liệu
    download_results()

if __name__ == '__main__':
    main()

