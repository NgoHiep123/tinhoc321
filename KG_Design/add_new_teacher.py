"""
Script để thêm giáo viên mới hoặc phân công lớp vào teachers_assign.csv
Sử dụng: python add_new_teacher.py
"""

import sys
import io
import csv
import os
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Đường dẫn đến file teachers_assign.csv (ở thư mục cha)
SCRIPT_DIR = Path(__file__).resolve().parent
TEACHERS_FILE = SCRIPT_DIR.parent / 'teachers_assign.csv'

def load_teachers():
    """Đọc dữ liệu giáo viên từ file CSV"""
    teachers = []
    
    if not TEACHERS_FILE.exists():
        print(f"⚠️  File {TEACHERS_FILE} không tồn tại! Tạo file mới...")
        return teachers
    
    with open(TEACHERS_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            teachers.append({
                'Id_teacher': row['Id_teacher'].strip(),
                'name': row['name'].strip(),
                'expertise': row.get('expertise', 'Tin học').strip(),
                'class': row['class'].strip()
            })
    
    return teachers

def save_teachers(teachers):
    """Lưu dữ liệu giáo viên vào file CSV"""
    # Backup file cũ
    backup_file = TEACHERS_FILE.with_suffix('.csv.bak')
    if TEACHERS_FILE.exists():
        import shutil
        shutil.copy2(TEACHERS_FILE, backup_file)
        print(f"💾 Đã tạo backup: {backup_file}")
    
    # Sắp xếp theo teacher_id và class
    teachers.sort(key=lambda x: (x['Id_teacher'], x['class']))
    
    # Ghi file CSV
    with open(TEACHERS_FILE, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['Id_teacher', 'name', 'expertise', 'class']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for teacher in teachers:
            writer.writerow(teacher)
    
    print(f"✅ Đã lưu dữ liệu vào {TEACHERS_FILE}")

def add_teacher_assignment(teacher_id, teacher_name, class_name, expertise='Tin học'):
    """
    Thêm một phân công lớp cho giáo viên
    
    Args:
        teacher_id: ID giáo viên (vd: 'tin_08')
        teacher_name: Tên giáo viên
        class_name: Tên lớp (vd: '7/19')
        expertise: Chuyên môn (mặc định: 'Tin học')
    """
    teachers = load_teachers()
    
    # Kiểm tra phân công đã tồn tại chưa
    for teacher in teachers:
        if (teacher['Id_teacher'] == teacher_id and 
            teacher['class'] == class_name):
            print(f"⚠️  Phân công '{teacher_id}' - '{class_name}' đã tồn tại!")
            return False
    
    # Thêm phân công mới
    teachers.append({
        'Id_teacher': teacher_id,
        'name': teacher_name,
        'expertise': expertise,
        'class': class_name
    })
    
    # Lưu file
    save_teachers(teachers)
    
    # Thống kê
    teacher_classes = [t['class'] for t in teachers if t['Id_teacher'] == teacher_id]
    
    print(f"\n✅ Đã thêm phân công lớp:")
    print(f"   👨‍🏫 Giáo viên: {teacher_name} (ID: {teacher_id})")
    print(f"   📚 Lớp: {class_name}")
    print(f"   📖 Chuyên môn: {expertise}")
    print(f"   📊 Tổng số lớp giáo viên này dạy: {len(teacher_classes)}")
    
    return True

def add_teacher_assignments_batch(teacher_id, teacher_name, class_names, expertise='Tin học'):
    """
    Thêm nhiều phân công lớp cho một giáo viên
    
    Args:
        teacher_id: ID giáo viên
        teacher_name: Tên giáo viên
        class_names: Danh sách lớp (list)
        expertise: Chuyên môn
    """
    teachers = load_teachers()
    
    # Lấy danh sách phân công hiện có của giáo viên này
    existing_classes = [
        t['class'] for t in teachers 
        if t['Id_teacher'] == teacher_id
    ]
    
    # Thêm các phân công mới
    added_count = 0
    skipped_count = 0
    
    for class_name in class_names:
        class_name = class_name.strip()
        if not class_name:
            continue
        
        if class_name in existing_classes:
            print(f"⚠️  Bỏ qua '{class_name}' (đã phân công)")
            skipped_count += 1
            continue
        
        teachers.append({
            'Id_teacher': teacher_id,
            'name': teacher_name,
            'expertise': expertise,
            'class': class_name
        })
        existing_classes.append(class_name)
        added_count += 1
    
    # Lưu file
    save_teachers(teachers)
    
    print(f"\n✅ Đã thêm {added_count} phân công lớp")
    if skipped_count > 0:
        print(f"⚠️  Đã bỏ qua {skipped_count} lớp (trùng lặp)")
    print(f"   👨‍🏫 Giáo viên: {teacher_name} (ID: {teacher_id})")
    print(f"   📊 Tổng số lớp giáo viên này dạy: {len(existing_classes)}")
    
    return added_count

def add_teacher_from_file(csv_file):
    """
    Thêm giáo viên/phân công từ file CSV
    
    Format CSV:
    Id_teacher,name,expertise,class
    tin_08,Trần Văn A,Tin học,7/25
    tin_08,Trần Văn A,Tin học,8/30
    """
    if not Path(csv_file).exists():
        print(f"❌ File không tồn tại: {csv_file}")
        return
    
    teachers = load_teachers()
    existing_assignments = {
        (t['Id_teacher'], t['class']) 
        for t in teachers
    }
    
    added_count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            teacher_id = row['Id_teacher'].strip()
            teacher_name = row['name'].strip()
            expertise = row.get('expertise', 'Tin học').strip()
            class_name = row['class'].strip()
            
            if not all([teacher_id, teacher_name, class_name]):
                continue
            
            # Kiểm tra trùng lặp
            key = (teacher_id, class_name)
            if key in existing_assignments:
                print(f"⚠️  Bỏ qua '{teacher_id}' - '{class_name}' (đã tồn tại)")
                continue
            
            teachers.append({
                'Id_teacher': teacher_id,
                'name': teacher_name,
                'expertise': expertise,
                'class': class_name
            })
            existing_assignments.add(key)
            added_count += 1
    
    # Lưu file
    save_teachers(teachers)
    
    print(f"\n{'='*60}")
    print(f"✅ Tổng cộng đã thêm {added_count} phân công từ file CSV")

def main():
    """Hàm chính - có thể tùy chỉnh"""
    print("=" * 60)
    print("👨‍🏫 THÊM GIÁO VIÊN/PHÂN CÔNG LỚP MỚI")
    print("=" * 60)
    
    # Ví dụ 1: Thêm một phân công lớp
    print("\n📌 Ví dụ 1: Thêm một phân công lớp")
    add_teacher_assignment(
        teacher_id='tin_08',
        teacher_name='Nguyễn Thị Mới',
        class_name='7/25',
        expertise='Tin học'
    )
    
    # Ví dụ 2: Thêm nhiều phân công cho một giáo viên
    # print("\n📌 Ví dụ 2: Thêm nhiều phân công")
    # add_teacher_assignments_batch(
    #     teacher_id='tin_08',
    #     teacher_name='Nguyễn Thị Mới',
    #     class_names=['7/25', '7/26', '8/29'],
    #     expertise='Tin học'
    # )
    
    # Ví dụ 3: Thêm từ file CSV
    # print("\n📌 Ví dụ 3: Thêm từ file CSV")
    # add_teacher_from_file('new_teachers.csv')
    
    print("\n" + "=" * 60)
    print("💡 Sau khi thêm giáo viên, hãy chạy lại:")
    print("   python build_kg_grade7.py")
    print("=" * 60)

if __name__ == '__main__':
    # Nếu có tham số dòng lệnh
    if len(sys.argv) >= 4:
        teacher_id = sys.argv[1]
        teacher_name = sys.argv[2]
        class_name = sys.argv[3]
        expertise = sys.argv[4] if len(sys.argv) > 4 else 'Tin học'
        add_teacher_assignment(teacher_id, teacher_name, class_name, expertise)
    else:
        main()

