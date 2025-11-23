"""
Script truy vấn Knowledge Graph bằng SPARQL
Minh họa các truy vấn hỗ trợ giáo viên
"""

import sys
import io
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
import pandas as pd

# Fix encoding cho Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

# ============================================
# 1. TẢI KNOWLEDGE GRAPH
# ============================================

def load_kg(kg_file='kg_grade7.ttl'):
    """Tải KG từ file"""
    print(f"📖 Đang tải Knowledge Graph từ {kg_file}...")
    g = Graph()
    g.parse(kg_file, format='turtle')
    g.bind("edu", EDU)
    g.bind("data", DATA)
    print(f"✅ Đã tải {len(g)} triples")
    return g

# ============================================
# 2. CÁC TRUY VẤN HỖ TRỢ GIÁO VIÊN
# ============================================

def query_students_by_class(g, class_name='7/19'):
    """
    Truy vấn: Danh sách học sinh trong một lớp
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?student ?name
    WHERE {
        ?class edu:className ?className .
        FILTER(?className = "{class_name}")
        
        ?student edu:belongsToClass ?class .
        ?student edu:fullName ?name .
    }
    ORDER BY ?name
    """
    
    results = g.query(query.format(class_name=class_name))
    
    print(f"\n📋 Danh sách học sinh lớp {class_name}:")
    print("-" * 50)
    for i, row in enumerate(results, 1):
        print(f"{i}. {row.name}")
    
    return results

def query_questions_by_lesson(g, lesson_id='A1'):
    """
    Truy vấn: Tất cả câu hỏi của một bài học
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?question ?text ?skill ?difficulty
    WHERE {
        data:lesson_7{lesson_id} a edu:Lesson .
        
        ?question edu:belongsToLesson data:lesson_7{lesson_id} .
        ?question rdfs:label ?text .
        ?question edu:requiresSkill ?skillNode .
        ?question edu:difficulty ?difficulty .
        
        ?skillNode rdfs:label ?skill .
    }
    """
    
    results = g.query(query.format(lesson_id=lesson_id))
    
    print(f"\n❓ Câu hỏi bài {lesson_id}:")
    print("-" * 80)
    for i, row in enumerate(results, 1):
        print(f"{i}. [{row.skill}] {row.text}")
    
    return results

def query_student_performance(g, student_name='Trần Thái', class_name='7/19'):
    """
    Truy vấn: Kết quả học tập của một học sinh
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?test ?score ?date
    WHERE {
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        ?student edu:fullName "{student_name}" .
        
        ?result edu:hasResult ?student .
        ?result edu:forTest ?test .
        ?result edu:score ?score .
        ?result edu:testDate ?date .
    }
    ORDER BY DESC(?date)
    """
    
    results = g.query(query.format(student_name=student_name, class_name=class_name))
    
    print(f"\n📊 Kết quả học tập của {student_name} (Lớp {class_name}):")
    print("-" * 60)
    
    if len(list(results)) == 0:
        print("⚠️  Chưa có dữ liệu kết quả")
    else:
        for row in results:
            print(f"Bài: {row.test.split('_')[-1]} | Điểm: {row.score} | Ngày: {row.date}")
    
    return results

def query_weak_students_in_topic(g, topic_id='A', min_score=5.0):
    """
    Truy vấn: Học sinh yếu ở một chủ đề
    (Yêu cầu đã chạy thuật toán KNN để gắn nhãn weakInTopic)
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?student ?name ?topic ?topicName
    WHERE {
        ?student edu:weakInTopic ?topic .
        ?student edu:fullName ?name .
        ?topic rdfs:label ?topicName .
        
        FILTER(CONTAINS(STR(?topic), "topic_7{topic_id}"))
    }
    ORDER BY ?name
    """
    
    results = g.query(query.format(topic_id=topic_id))
    
    print(f"\n⚠️  Học sinh yếu ở chủ đề {topic_id}:")
    print("-" * 60)
    
    if len(list(results)) == 0:
        print("ℹ️  Chưa chạy thuật toán KNN để xác định học sinh yếu")
    else:
        for i, row in enumerate(results, 1):
            print(f"{i}. {row.name}")
    
    return results

def query_recommended_lessons(g, student_name='Trần Thái', class_name='7/19'):
    """
    Truy vấn: Bài học được gợi ý cho học sinh
    (Yêu cầu đã chạy thuật toán PPR)
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?lesson ?lessonName
    WHERE {
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        ?student edu:fullName "{student_name}" .
        
        ?lesson edu:recommendedFor ?student .
        ?lesson rdfs:label ?lessonName .
    }
    """
    
    results = g.query(query.format(student_name=student_name, class_name=class_name))
    
    print(f"\n💡 Bài học được gợi ý cho {student_name}:")
    print("-" * 60)
    
    if len(list(results)) == 0:
        print("ℹ️  Chưa chạy thuật toán PPR để tạo gợi ý")
    else:
        for i, row in enumerate(results, 1):
            print(f"{i}. {row.lessonName}")
    
    return results

def query_class_statistics(g, class_name='7/19'):
    """
    Truy vấn: Thống kê tổng quan một lớp
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    
    SELECT (COUNT(DISTINCT ?student) as ?total_students)
           (AVG(?score) as ?avg_score)
           (COUNT(DISTINCT ?result) as ?total_tests)
    WHERE {
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        
        OPTIONAL {
            ?result edu:hasResult ?student .
            ?result edu:score ?score .
        }
    }
    """
    
    results = g.query(query.format(class_name=class_name))
    
    print(f"\n📈 Thống kê lớp {class_name}:")
    print("-" * 60)
    
    for row in results:
        print(f"Tổng số học sinh: {row.total_students}")
        print(f"Điểm trung bình: {float(row.avg_score) if row.avg_score else 'N/A':.2f}")
        print(f"Số bài kiểm tra: {row.total_tests}")
    
    return results

def query_teacher_by_class(g, class_name='7/19'):
    """
    Truy vấn: Giáo viên dạy một lớp
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teacher ?name ?teacherId ?expertise
    WHERE {{
        ?class edu:className "{class_name}" .
        ?teacher edu:teaches ?class .
        ?teacher rdfs:label ?name .
        OPTIONAL {{ ?teacher edu:teacherId ?teacherId . }}
        OPTIONAL {{ ?teacher edu:expertise ?expertise . }}
    }}
    """
    
    results = g.query(query.format(class_name=class_name))
    
    print(f"\n👨‍🏫 Giáo viên dạy lớp {class_name}:")
    print("-" * 60)
    
    if len(list(results)) == 0:
        print("⚠️  Chưa có thông tin giáo viên")
    else:
        for i, row in enumerate(results, 1):
            teacher_info = f"{i}. {row.name}"
            if row.teacherId:
                teacher_info += f" (ID: {row.teacherId})"
            if row.expertise:
                teacher_info += f" - Chuyên môn: {row.expertise}"
            print(teacher_info)
    
    return results

def query_classes_by_teacher(g, teacher_id='tin_01'):
    """
    Truy vấn: Các lớp mà một giáo viên dạy
    """
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teacher ?name ?class ?className
    WHERE {{
        ?teacher edu:teacherId "{teacher_id}" .
        ?teacher rdfs:label ?name .
        ?teacher edu:teaches ?class .
        ?class edu:className ?className .
    }}
    ORDER BY ?className
    """
    
    results = g.query(query.format(teacher_id=teacher_id))
    
    print(f"\n📚 Các lớp giáo viên {teacher_id} dạy:")
    print("-" * 60)
    
    if len(list(results)) == 0:
        print("⚠️  Không tìm thấy giáo viên hoặc chưa có phân công lớp")
    else:
        teacher_name = None
        classes = []
        for row in results:
            if not teacher_name:
                teacher_name = row.name
            classes.append(row.className)
        
        print(f"Giáo viên: {teacher_name}")
        print(f"Số lớp: {len(classes)}")
        for i, class_name in enumerate(classes, 1):
            print(f"  {i}. {class_name}")
    
    return results

# ============================================
# 3. DEMO CÁC TRUY VẤN
# ============================================

def demo_queries(g):
    """Demo các truy vấn"""
    print("\n" + "=" * 80)
    print("🔍 DEMO CÁC TRUY VẤN SPARQL")
    print("=" * 80)
    
    # 1. Danh sách học sinh
    query_students_by_class(g, '7/19')
    
    # 2. Câu hỏi theo bài học
    query_questions_by_lesson(g, 'A1')
    
    # 3. Kết quả học tập
    query_student_performance(g, 'Trần Thái', '7/19')
    
    # 4. Học sinh yếu
    query_weak_students_in_topic(g, 'A')
    
    # 5. Gợi ý bài học
    query_recommended_lessons(g, 'Trần Thái', '7/19')
    
    # 6. Thống kê lớp
    query_class_statistics(g, '7/19')
    
    # 7. Giáo viên dạy lớp
    query_teacher_by_class(g, '7/19')
    
    # 8. Các lớp giáo viên dạy
    query_classes_by_teacher(g, 'tin_01')

# ============================================
# 4. MAIN
# ============================================

def main():
    """Hàm chính"""
    g = load_kg('kg_grade7.ttl')
    demo_queries(g)

if __name__ == '__main__':
    main()

