"""
Script chuyển đổi file Excel DSHS sang students.json
Tự động tạo mật khẩu hash cho học sinh
"""

import pandas as pd
import json
import hashlib
from collections import defaultdict

def hash_password(password):
    """
    Tạo SHA-256 hash cho mật khẩu
    Mật khẩu mặc định: 123456
    """
    return hashlib.sha256(password.encode()).hexdigest()

def convert_excel_to_json(excel_file='25_26_DSHS.xlsx', output_file='students.json'):
    """
    Chuyển đổi file Excel sang JSON
    
    Format Excel mong đợi:
    - Cột 1: Họ tên học sinh
    - Cột 2: Lớp (VD: 7/19, 6/14)
    - Các cột khác: Tùy chọn
    """
    
    print("=" * 60)
    print("CHUYỂN ĐỔI EXCEL SANG STUDENTS.JSON")
    print("=" * 60)
    
    # Đọc file Excel
    try:
        print(f"\n📂 Đang đọc file: {excel_file}")
        
        # Thử đọc tất cả sheets
        xl_file = pd.ExcelFile(excel_file)
        print(f"✅ Tìm thấy {len(xl_file.sheet_names)} sheets:")
        for i, sheet in enumerate(xl_file.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        # Đọc sheet đầu tiên (hoặc sheet có tên chứa "DSHS")
        sheet_name = None
        for name in xl_file.sheet_names:
            if 'DSHS' in name.upper() or 'DANH' in name.upper():
                sheet_name = name
                break
        
        if not sheet_name:
            sheet_name = xl_file.sheet_names[0]
        
        print(f"\n📊 Đang xử lý sheet: {sheet_name}")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        print(f"✅ Đã đọc {len(df)} dòng dữ liệu")
        print(f"\n📋 Các cột trong file:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {excel_file}")
        print("💡 Đảm bảo file Excel nằm trong thư mục gốc dự án")
        return
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")
        return
    
    # Xác định tên cột
    print("\n🔍 Đang phân tích cấu trúc dữ liệu...")
    
    # Tìm cột tên và lớp
    name_col = None
    class_col = None
    
    for col in df.columns:
        col_lower = str(col).lower()
        if 'tên' in col_lower or 'name' in col_lower or 'họ' in col_lower:
            name_col = col
        if 'lớp' in col_lower or 'class' in col_lower:
            class_col = col
    
    # Nếu không tìm thấy, dùng 2 cột đầu
    if name_col is None:
        name_col = df.columns[0]
        print(f"⚠️  Không tìm thấy cột 'Tên', sử dụng cột đầu tiên: {name_col}")
    
    if class_col is None and len(df.columns) > 1:
        class_col = df.columns[1]
        print(f"⚠️  Không tìm thấy cột 'Lớp', sử dụng cột thứ 2: {class_col}")
    
    print(f"\n✅ Cột Tên: {name_col}")
    print(f"✅ Cột Lớp: {class_col}")
    
    # Xử lý dữ liệu
    print("\n🔧 Đang xử lý dữ liệu...")
    
    students_data = defaultdict(lambda: defaultdict(list))
    default_password_hash = hash_password("123456")
    
    processed_count = 0
    skipped_count = 0
    
    for idx, row in df.iterrows():
        # Lấy tên và lớp
        name = row[name_col]
        class_name = row[class_col]
        
        # Bỏ qua dòng rỗng
        if pd.isna(name) or pd.isna(class_name):
            skipped_count += 1
            continue
        
        # Clean data
        name = str(name).strip()
        class_name = str(class_name).strip()
        
        # Bỏ qua tên không hợp lệ
        if not name or name.lower() in ['nan', 'none', '']:
            skipped_count += 1
            continue
        
        # Phân tích khối và lớp (VD: "7/19" -> khối 7, lớp 7/19)
        try:
            if '/' in class_name:
                grade = class_name.split('/')[0]
            else:
                # Nếu không có dấu /, thử extract số đầu
                grade = ''.join(filter(str.isdigit, class_name[:2]))
                if not grade:
                    print(f"⚠️  Không thể xác định khối cho lớp: {class_name}, bỏ qua")
                    skipped_count += 1
                    continue
            
            # Tạo student object
            student = {
                "name": name,
                "pass_hash": default_password_hash
            }
            
            students_data[grade][class_name].append(student)
            processed_count += 1
            
        except Exception as e:
            print(f"⚠️  Lỗi xử lý dòng {idx + 1}: {e}")
            skipped_count += 1
            continue
    
    print(f"\n✅ Đã xử lý: {processed_count} học sinh")
    print(f"⚠️  Bỏ qua: {skipped_count} dòng")
    
    # Thống kê
    print("\n📊 Thống kê theo khối:")
    for grade in sorted(students_data.keys()):
        total = sum(len(students) for students in students_data[grade].values())
        num_classes = len(students_data[grade])
        print(f"   Khối {grade}: {total} học sinh, {num_classes} lớp")
        for class_name in sorted(students_data[grade].keys()):
            print(f"      - {class_name}: {len(students_data[grade][class_name])} học sinh")
    
    # Chuyển đổi sang dict thông thường
    output_data = {
        grade: {
            class_name: students 
            for class_name, students in classes.items()
        }
        for grade, classes in students_data.items()
    }
    
    # Lưu file JSON
    try:
        print(f"\n💾 Đang lưu file: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu thành công!")
        print(f"📁 Vị trí: {output_file}")
        
        # Tính kích thước file
        import os
        file_size = os.path.getsize(output_file)
        print(f"📦 Kích thước: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)
    print("\n💡 LƯU Ý:")
    print("   - Mật khẩu mặc định cho tất cả học sinh: 123456")
    print("   - Hash: f88a9a2ca91a3889fd073583ea72735346bc8b34c1da7b55ca64390fa61bd953")
    print("   - File đã sẵn sàng sử dụng với web trắc nghiệm")
    print("\n📌 BƯỚC TIẾP THEO:")
    print("   1. Kiểm tra file students.json")
    print("   2. Test đăng nhập trên web")
    print("   3. Nếu cần đổi mật khẩu, sửa trong script này")

def main():
    """Hàm chính"""
    import sys
    import os
    
    # Fix encoding for Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Tìm file Excel - tìm trong thư mục cha (gốc dự án)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_files = ['25_26_DSHS.xlsx', '25-26-DSHS.xlsx', 'DSHS.xlsx']
    excel_file = None
    
    for file in excel_files:
        full_path = os.path.join(parent_dir, file)
        if os.path.exists(full_path):
            excel_file = full_path
            break
    
    if not excel_file:
        print("[ERROR] Khong tim thay file Excel!")
        print("\n[INFO] File can co mot trong cac ten sau:")
        for f in excel_files:
            print(f"   - {f}")
        print("\n[INFO] Dat file trong thu muc goc du an va chay lai script.")
        sys.exit(1)
    
    # Chạy conversion - output vào thư mục gốc
    output_file = os.path.join(parent_dir, 'students.json')
    convert_excel_to_json(excel_file, output_file)

if __name__ == '__main__':
    main()

