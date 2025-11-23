"""
Script xây dựng Knowledge Graph cho Tin học Khối 7
Sử dụng: Python 3.8+, RDFLib
"""

import json
import csv
import sys
import io
from datetime import datetime
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Fix encoding cho Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================
# 1. ĐỊNH NGHĨA NAMESPACE
# ============================================

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

# ============================================
# 2. KHỞI TẠO GRAPH
# ============================================

def create_knowledge_graph():
    """Tạo Knowledge Graph rỗng với schema"""
    g = Graph()
    g.bind("edu", EDU)
    g.bind("data", DATA)
    g.bind("xsd", XSD)
    
    return g

# ============================================
# 3. THÊM DỮ LIỆU HỌC SINH
# ============================================

def add_students_to_kg(g, students_file='../students.json'):
    """
    Thêm thông tin học sinh từ students.json vào KG
    
    Cấu trúc:
    - Student -> belongsToClass -> Class
    - Class -> belongsToGrade -> Grade
    """
    print("📚 Đang thêm dữ liệu học sinh...")
    
    with open(students_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    student_count = 0
    class_set = set()
    
    # Chỉ xử lý khối 7
    if '7' in data:
        grade_7 = data['7']
        
        # Tạo node Grade 7
        grade_uri = DATA['grade_7']
        g.add((grade_uri, RDF.type, EDU.Grade))
        g.add((grade_uri, RDFS.label, Literal("Khối 7", lang='vi')))
        
        for class_name, students in grade_7.items():
            # Tạo node Class
            class_id = class_name.replace('/', '_')
            class_uri = DATA[f'class_{class_id}']
            
            if class_uri not in class_set:
                g.add((class_uri, RDF.type, EDU.Class))
                g.add((class_uri, EDU.className, Literal(class_name)))
                g.add((class_uri, EDU.belongsToGrade, grade_uri))
                class_set.add(class_uri)
            
            # Thêm từng học sinh
            for student in students:
                student_id = f"student_{class_id}_{student['name'].replace(' ', '_')}"
                student_uri = DATA[student_id]
                
                g.add((student_uri, RDF.type, EDU.Student))
                g.add((student_uri, EDU.fullName, Literal(student['name'])))
                g.add((student_uri, EDU.belongsToClass, class_uri))
                
                student_count += 1
    
    print(f"✅ Đã thêm {student_count} học sinh, {len(class_set)} lớp")
    return g

# ============================================
# 4. THÊM DỮ LIỆU CHỦ ĐỀ & BÀI HỌC
# ============================================

def add_lessons_to_kg(g):
    """
    Thêm cấu trúc chủ đề và bài học Khối 7
    """
    print("📖 Đang thêm cấu trúc bài học...")
    
    # Khối 7
    grade_uri = DATA['grade_7']
    
    # Định nghĩa các chủ đề Khối 7
    topics = {
        'A': 'Máy tính và hệ điều hành',
        'B': 'Soạn thảo văn bản',
        'C': 'Mạng máy tính và Internet',
        'D': 'Trình chiếu',
        'E': 'Thuật toán và lập trình',
        'F': 'Dự án'
    }
    
    # Định nghĩa các bài học có trong dữ liệu
    lessons = {
        'A1': {'topic': 'A', 'name': 'Thiết bị vào-ra cơ bản'},
        'A2': {'topic': 'A', 'name': 'Các thiết bị vào-ra'},
        'A4': {'topic': 'A', 'name': 'Chức năng hệ điều hành'},
        'A5': {'topic': 'A', 'name': 'File Explorer'},
    }
    
    # Tạo các node Topic
    for topic_id, topic_name in topics.items():
        topic_uri = DATA[f'topic_7{topic_id}']
        g.add((topic_uri, RDF.type, EDU.Topic))
        g.add((topic_uri, RDFS.label, Literal(f"Chủ đề {topic_id}: {topic_name}", lang='vi')))
        g.add((topic_uri, EDU.forGrade, grade_uri))
    
    # Tạo các node Lesson
    for lesson_id, lesson_info in lessons.items():
        lesson_uri = DATA[f'lesson_7{lesson_id}']
        topic_uri = DATA[f'topic_7{lesson_info["topic"]}']
        
        g.add((lesson_uri, RDF.type, EDU.Lesson))
        g.add((lesson_uri, RDFS.label, Literal(f"Bài {lesson_id}: {lesson_info['name']}", lang='vi')))
        g.add((lesson_uri, EDU.belongsToTopic, topic_uri))
    
    print(f"✅ Đã thêm {len(topics)} chủ đề, {len(lessons)} bài học")
    return g

# ============================================
# 5. THÊM NGÂN HÀNG CÂU HỎI
# ============================================

def add_questions_to_kg(g, questions_file='../Bai_tap_Tin_7/question_bank_grade7_all_canonical.csv'):
    """
    Thêm câu hỏi từ CSV vào KG
    """
    print("❓ Đang thêm ngân hàng câu hỏi...")
    
    # Định nghĩa các kỹ năng
    skills = {
        'nhan_biet': 'Nhận biết',
        'thong_hieu': 'Thông hiểu',
        'van_dung': 'Vận dụng'
    }
    
    # Tạo node Skill
    for skill_id, skill_name in skills.items():
        skill_uri = DATA[f'skill_{skill_id}']
        g.add((skill_uri, RDF.type, EDU.Skill))
        g.add((skill_uri, RDFS.label, Literal(skill_name, lang='vi')))
    
    # Đọc câu hỏi từ CSV
    question_count = 0
    with open(questions_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            q_id = row['q_id']
            question_uri = DATA[f'question_{q_id}']
            
            # Xác định bài học từ topic_id
            topic_id = row['topic_id']
            if 'k7_a1' in topic_id.lower():
                lesson_id = 'A1'
            elif 'k7_a2' in topic_id.lower():
                lesson_id = 'A2'
            elif 'k7_a4' in topic_id.lower():
                lesson_id = 'A4'
            elif 'k7_a5' in topic_id.lower():
                lesson_id = 'A5'
            else:
                continue
            
            lesson_uri = DATA[f'lesson_7{lesson_id}']
            
            # Xác định kỹ năng
            difficulty = row['difficulty'].lower().strip()
            if 'nhận biết' in difficulty or 'nhan biet' in difficulty:
                skill_id = 'nhan_biet'
            elif 'thông hiểu' in difficulty or 'thong hieu' in difficulty:
                skill_id = 'thong_hieu'
            elif 'vận dụng' in difficulty or 'van dung' in difficulty:
                skill_id = 'van_dung'
            else:
                skill_id = 'nhan_biet'
            
            skill_uri = DATA[f'skill_{skill_id}']
            
            # Thêm câu hỏi vào KG
            g.add((question_uri, RDF.type, EDU.Question))
            g.add((question_uri, RDFS.label, Literal(row['question_text'], lang='vi')))
            g.add((question_uri, EDU.belongsToLesson, lesson_uri))
            g.add((question_uri, EDU.requiresSkill, skill_uri))
            g.add((question_uri, EDU.difficulty, Literal(row['difficulty'])))
            
            question_count += 1
    
    print(f"✅ Đã thêm {question_count} câu hỏi")
    return g

# ============================================
# 6. THÊM KẾT QUẢ HỌC TẬP (từ Google Sheets)
# ============================================

def add_test_results_to_kg(g, results_file='../test_results.csv'):
    """
    Thêm kết quả làm bài từ file CSV (export từ Google Sheets)
    
    Format mong đợi:
    timestamp, student_name, class_name, quiz_id, score, total, duration
    """
    print("📊 Đang thêm kết quả làm bài...")
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            result_count = 0
            
            for row in reader:
                # Tạo ID kết quả
                result_id = f"result_{row['student_name'].replace(' ', '_')}_{row['quiz_id']}_{row['timestamp']}"
                result_uri = DATA[result_id]
                
                # Tìm URI học sinh
                class_id = row['class_name'].replace('/', '_')
                student_id = f"student_{class_id}_{row['student_name'].replace(' ', '_')}"
                student_uri = DATA[student_id]
                
                # Tạo hoặc tìm Test URI
                test_uri = DATA[f"test_{row['quiz_id']}"]
                
                # Thêm kết quả
                g.add((result_uri, RDF.type, EDU.TestResult))
                g.add((result_uri, EDU.hasResult, student_uri))
                g.add((result_uri, EDU.forTest, test_uri))
                g.add((result_uri, EDU.score, Literal(float(row['score']), datatype=XSD.float)))
                g.add((result_uri, EDU.testDate, Literal(row['timestamp'], datatype=XSD.dateTime)))
                
                if 'duration' in row:
                    g.add((result_uri, EDU.duration, Literal(int(row['duration']), datatype=XSD.integer)))
                
                result_count += 1
            
            print(f"✅ Đã thêm {result_count} kết quả")
    except FileNotFoundError:
        print("⚠️  Chưa có file kết quả. Bỏ qua bước này.")
    
    return g

# ============================================
# 7. THÊM DỮ LIỆU GIÁO VIÊN
# ============================================

def add_teachers_to_kg(g, teachers_file='../teachers_assign.csv'):
    """
    Thêm thông tin giáo viên và phân công lớp từ CSV vào KG
    
    Cấu trúc:
    - Teacher -> teaches -> Class
    - Teacher có: Id_teacher, name, expertise
    """
    print("👨‍🏫 Đang thêm dữ liệu giáo viên...")
    
    try:
        teacher_set = set()  # Để tránh tạo trùng teacher
        assignment_count = 0
        
        with open(teachers_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig để xử lý BOM
            reader = csv.DictReader(f)
            
            for row in reader:
                teacher_id = row['Id_teacher'].strip()
                teacher_name = row['name'].strip()
                expertise = row['expertise'].strip() if 'expertise' in row else 'Tin học'
                class_name = row['class'].strip()
                
                # Tạo Teacher node (chỉ tạo 1 lần cho mỗi teacher_id)
                if teacher_id not in teacher_set:
                    teacher_uri = DATA[f'teacher_{teacher_id}']
                    g.add((teacher_uri, RDF.type, EDU.Teacher))
                    g.add((teacher_uri, RDFS.label, Literal(teacher_name, lang='vi')))
                    g.add((teacher_uri, EDU.teacherId, Literal(teacher_id)))
                    if expertise:
                        g.add((teacher_uri, EDU.expertise, Literal(expertise, lang='vi')))
                    teacher_set.add(teacher_id)
                
                # Tạo Class node nếu chưa có (có thể đã được tạo trong add_students_to_kg)
                class_id = class_name.replace('/', '_')
                class_uri = DATA[f'class_{class_id}']
                
                # Kiểm tra xem class đã tồn tại chưa bằng cách tìm triple (class_uri, RDF.type, EDU.Class)
                class_exists = (class_uri, RDF.type, EDU.Class) in g
                
                if not class_exists:
                    # Xác định grade từ class_name
                    if '/' in class_name:
                        grade_num = class_name.split('/')[0]
                    else:
                        grade_num = '7'  # Default
                    
                    grade_uri = DATA[f'grade_{grade_num}']
                    
                    # Tạo Grade nếu chưa có
                    if (grade_uri, RDF.type, EDU.Grade) not in g:
                        g.add((grade_uri, RDF.type, EDU.Grade))
                        g.add((grade_uri, RDFS.label, Literal(f"Khối {grade_num}", lang='vi')))
                    
                    # Tạo Class
                    g.add((class_uri, RDF.type, EDU.Class))
                    g.add((class_uri, EDU.className, Literal(class_name)))
                    g.add((class_uri, EDU.belongsToGrade, grade_uri))
                
                # Tạo relationship: Teacher teaches Class
                teacher_uri = DATA[f'teacher_{teacher_id}']
                g.add((teacher_uri, EDU.teaches, class_uri))
                assignment_count += 1
        
        print(f"✅ Đã thêm {len(teacher_set)} giáo viên, {assignment_count} phân công lớp")
        
    except FileNotFoundError:
        print(f"⚠️  Không tìm thấy file {teachers_file}. Bỏ qua bước này.")
    except Exception as e:
        print(f"⚠️  Lỗi khi đọc file giáo viên: {e}")
    
    return g

# ============================================
# 8. LƯU KNOWLEDGE GRAPH
# ============================================

def save_kg(g, output_file='kg_grade7.ttl'):
    """Lưu KG ra file Turtle"""
    print(f"💾 Đang lưu Knowledge Graph...")
    
    g.serialize(destination=output_file, format='turtle')
    
    print(f"✅ Đã lưu vào {output_file}")
    print(f"📈 Tổng số triples: {len(g)}")

# ============================================
# 8. MAIN FUNCTION
# ============================================

def main():
    """Hàm chính"""
    print("=" * 60)
    print("🚀 BẮT ĐẦU XÂY DỰNG KNOWLEDGE GRAPH KHỐI 7")
    print("=" * 60)
    
    # Tạo graph
    g = create_knowledge_graph()
    
    # Thêm dữ liệu
    g = add_students_to_kg(g)
    g = add_teachers_to_kg(g)  # Thêm giáo viên và phân công lớp
    g = add_lessons_to_kg(g)
    # g = add_questions_to_kg(g)  # Tạm thời bỏ qua vì thiếu file
    # g = add_test_results_to_kg(g)  # Tạm thời bỏ qua vì thiếu file
    
    # Lưu KG
    save_kg(g, 'kg_grade7.ttl')
    
    print("=" * 60)
    print("✅ HOÀN THÀNH XÂY DỰNG KNOWLEDGE GRAPH")
    print("=" * 60)

if __name__ == '__main__':
    main()

