"""
Script để thêm học sinh mới vào students.json
Sử dụng: python add_new_student.py
"""

import sys
import io
import json
import os
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Đường dẫn đến file students.json (ở thư mục cha)
SCRIPT_DIR = Path(__file__).resolve().parent
STUDENTS_FILE = SCRIPT_DIR.parent / 'students.json'

def load_students():
    """Đọc dữ liệu học sinh từ file JSON"""
    if not STUDENTS_FILE.exists():
        print(f"⚠️  File {STUDENTS_FILE} không tồn tại!")
        return {}
    
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_students(data):
    """Lưu dữ liệu học sinh vào file JSON"""
    # Backup file cũ
    backup_file = STUDENTS_FILE.with_suffix('.json.bak')
    if STUDENTS_FILE.exists():
        import shutil
        shutil.copy2(STUDENTS_FILE, backup_file)
        print(f"💾 Đã tạo backup: {backup_file}")
    
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Đã lưu dữ liệu vào {STUDENTS_FILE}")

def add_student(grade, class_name, student_name):
    """
    Thêm một học sinh mới vào dữ liệu
    
    Args:
        grade: Khối (vd: '7', '6', '8')
        class_name: Tên lớp (vd: '7/19', '6/14')
        student_name: Tên học sinh
    """
    data = load_students()
    
    # Khởi tạo cấu trúc nếu chưa có
    if grade not in data:
        data[grade] = {}
    
    if class_name not in data[grade]:
        data[grade][class_name] = []
    
    # Kiểm tra học sinh đã tồn tại chưa
    existing_students = [s.get('name', '') for s in data[grade][class_name]]
    if student_name in existing_students:
        print(f"⚠️  Học sinh '{student_name}' đã tồn tại trong lớp {class_name}!")
        return False
    
    # Thêm học sinh mới (có thể tạo pass_hash sau)
    new_student = {
        'name': student_name,
        'pass_hash': ''  # Có thể cập nhật sau
    }
    
    data[grade][class_name].append(new_student)
    
    # Sắp xếp lại theo tên
    data[grade][class_name].sort(key=lambda x: x['name'])
    
    # Lưu file
    save_students(data)
    
    print(f"\n✅ Đã thêm học sinh:")
    print(f"   📝 Tên: {student_name}")
    print(f"   🏫 Khối: {grade}")
    print(f"   📚 Lớp: {class_name}")
    print(f"   👥 Tổng số học sinh trong lớp: {len(data[grade][class_name])}")
    
    return True

def add_students_batch(grade, class_name, student_names):
    """
    Thêm nhiều học sinh cùng lúc
    
    Args:
        grade: Khối
        class_name: Tên lớp
        student_names: Danh sách tên học sinh (list)
    """
    data = load_students()
    
    # Khởi tạo cấu trúc nếu chưa có
    if grade not in data:
        data[grade] = {}
    
    if class_name not in data[grade]:
        data[grade][class_name] = []
    
    # Lấy danh sách học sinh hiện có
    existing_students = [s.get('name', '') for s in data[grade][class_name]]
    
    # Thêm các học sinh mới
    added_count = 0
    skipped_count = 0
    
    for student_name in student_names:
        student_name = student_name.strip()
        if not student_name:
            continue
        
        if student_name in existing_students:
            print(f"⚠️  Bỏ qua '{student_name}' (đã tồn tại)")
            skipped_count += 1
            continue
        
        new_student = {
            'name': student_name,
            'pass_hash': ''  # Có thể cập nhật sau
        }
        data[grade][class_name].append(new_student)
        existing_students.append(student_name)
        added_count += 1
    
    # Sắp xếp lại theo tên
    data[grade][class_name].sort(key=lambda x: x['name'])
    
    # Lưu file
    save_students(data)
    
    print(f"\n✅ Đã thêm {added_count} học sinh mới")
    if skipped_count > 0:
        print(f"⚠️  Đã bỏ qua {skipped_count} học sinh (trùng lặp)")
    print(f"   📚 Lớp: {grade}/{class_name}")
    print(f"   👥 Tổng số học sinh trong lớp: {len(data[grade][class_name])}")
    
    return added_count

def add_students_from_file(csv_file):
    """
    Thêm học sinh từ file CSV
    
    Format CSV:
    grade,class,student_name
    7,7/19,Nguyễn Văn A
    7,7/19,Trần Thị B
    """
    import csv
    
    if not Path(csv_file).exists():
        print(f"❌ File không tồn tại: {csv_file}")
        return
    
    students_by_class = {}
    added_total = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            grade = row['grade'].strip()
            class_name = row['class'].strip()
            student_name = row['student_name'].strip()
            
            if not all([grade, class_name, student_name]):
                continue
            
            key = f"{grade}/{class_name}"
            if key not in students_by_class:
                students_by_class[key] = []
            
            students_by_class[key].append(student_name)
    
    # Thêm từng nhóm lớp
    for key, student_names in students_by_class.items():
        grade, class_name = key.split('/', 1)
        added = add_students_batch(grade, class_name, student_names)
        added_total += added
    
    print(f"\n{'='*60}")
    print(f"✅ Tổng cộng đã thêm {added_total} học sinh từ file CSV")

def main():
    """Hàm chính - có thể tùy chỉnh"""
    print("=" * 60)
    print("📝 THÊM HỌC SINH MỚI VÀO KNOWLEDGE GRAPH")
    print("=" * 60)
    
    # Ví dụ 1: Thêm một học sinh
    print("\n📌 Ví dụ 1: Thêm một học sinh")
    add_student('7', '7/19', 'Nguyễn Văn Mới')
    
    # Ví dụ 2: Thêm nhiều học sinh cùng lúc
    # print("\n📌 Ví dụ 2: Thêm nhiều học sinh")
    # add_students_batch('7', '7/19', [
    #     'Trần Thị Hoa',
    #     'Lê Văn Nam',
    #     'Phạm Thị Mai'
    # ])
    
    # Ví dụ 3: Thêm từ file CSV
    # print("\n📌 Ví dụ 3: Thêm từ file CSV")
    # add_students_from_file('new_students.csv')
    
    print("\n" + "=" * 60)
    print("💡 Sau khi thêm học sinh, hãy chạy lại:")
    print("   python build_kg_grade7.py")
    print("=" * 60)

if __name__ == '__main__':
    # Nếu có tham số dòng lệnh
    if len(sys.argv) >= 4:
        grade = sys.argv[1]
        class_name = sys.argv[2]
        student_name = sys.argv[3]
        add_student(grade, class_name, student_name)
    else:
        main()

