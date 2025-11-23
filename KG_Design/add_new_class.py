"""
Script để thêm lớp mới vào Knowledge Graph
Có thể thêm lớp bằng cách:
1. Thêm học sinh vào lớp mới
2. Phân công giáo viên dạy lớp mới
Sử dụng: python add_new_class.py
"""

import sys
import io
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def add_class_by_student(grade, class_name, student_names=None):
    """
    Thêm lớp mới bằng cách thêm học sinh vào lớp đó
    
    Args:
        grade: Khối (vd: '7', '6')
        class_name: Tên lớp (vd: '7/25')
        student_names: Danh sách học sinh (optional, có thể thêm sau)
    """
    from add_new_student import add_student, add_students_batch
    
    print(f"📚 Đang tạo lớp mới: {grade}/{class_name}")
    
    if student_names:
        # Thêm học sinh cùng lúc với tạo lớp
        add_students_batch(grade, class_name, student_names)
    else:
        # Tạo lớp rỗng (sẽ được tạo khi thêm học sinh đầu tiên)
        print(f"💡 Lớp sẽ được tạo khi bạn thêm học sinh đầu tiên vào lớp này.")
        print(f"   Sử dụng: python add_new_student.py {grade} {class_name} 'Tên học sinh'")
    
    return True

def add_class_by_teacher(teacher_id, teacher_name, class_name, expertise='Tin học'):
    """
    Thêm lớp mới bằng cách phân công giáo viên dạy lớp đó
    
    Args:
        teacher_id: ID giáo viên
        teacher_name: Tên giáo viên
        class_name: Tên lớp
        expertise: Chuyên môn
    """
    from add_new_teacher import add_teacher_assignment
    
    print(f"📚 Đang tạo lớp mới: {class_name}")
    print(f"   👨‍🏫 Giáo viên: {teacher_name} (ID: {teacher_id})")
    
    add_teacher_assignment(teacher_id, teacher_name, class_name, expertise)
    
    return True

def main():
    """Hàm chính"""
    print("=" * 60)
    print("📚 THÊM LỚP MỚI VÀO KNOWLEDGE GRAPH")
    print("=" * 60)
    
    print("\n💡 Có 2 cách để thêm lớp mới:")
    print("\n1️⃣  Thêm lớp bằng cách thêm học sinh:")
    print("   python add_new_class.py --by-student 7 7/25")
    print("   hoặc: python add_new_student.py 7 7/25 'Nguyễn Văn A'")
    
    print("\n2️⃣  Thêm lớp bằng cách phân công giáo viên:")
    print("   python add_new_class.py --by-teacher tin_08 'Nguyễn Thị B' 7/25")
    print("   hoặc: python add_new_teacher.py tin_08 'Nguyễn Thị B' 7/25")
    
    print("\n" + "=" * 60)
    print("💡 Sau khi thêm lớp, hãy chạy lại:")
    print("   python build_kg_grade7.py")
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--by-student' and len(sys.argv) >= 4:
            grade = sys.argv[2]
            class_name = sys.argv[3]
            student_names = sys.argv[4:] if len(sys.argv) > 4 else None
            add_class_by_student(grade, class_name, student_names)
        elif sys.argv[1] == '--by-teacher' and len(sys.argv) >= 5:
            teacher_id = sys.argv[2]
            teacher_name = sys.argv[3]
            class_name = sys.argv[4]
            expertise = sys.argv[5] if len(sys.argv) > 5 else 'Tin học'
            add_class_by_teacher(teacher_id, teacher_name, class_name, expertise)
        else:
            main()
    else:
        main()

