"""
Demo script để chạy các truy vấn giáo viên trong Knowledge Graph
"""

import sys
import io

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from query_kg import load_kg, query_teacher_by_class, query_classes_by_teacher

def main():
    print("=" * 70)
    print("🔍 DEMO CÁC TRUY VẤN GIÁO VIÊN TRONG KNOWLEDGE GRAPH")
    print("=" * 70)
    
    # Tải KG
    g = load_kg('kg_grade7.ttl')
    
    # ============================================
    # 1. Truy vấn: Giáo viên dạy một lớp cụ thể
    # ============================================
    print("\n" + "=" * 70)
    print("📚 TRUY VẤN 1: Giáo viên dạy các lớp khác nhau")
    print("=" * 70)
    
    test_classes = ['7/19', '7/20', '6/14', '6/15']
    for class_name in test_classes:
        query_teacher_by_class(g, class_name)
    
    # ============================================
    # 2. Truy vấn: Các lớp một giáo viên dạy
    # ============================================
    print("\n" + "=" * 70)
    print("👨‍🏫 TRUY VẤN 2: Các lớp một giáo viên dạy")
    print("=" * 70)
    
    test_teachers = ['tin_01', 'tin_02', 'tin_03']
    for teacher_id in test_teachers:
        query_classes_by_teacher(g, teacher_id)
    
    # ============================================
    # 3. Truy vấn: Tất cả giáo viên và số lớp dạy
    # ============================================
    print("\n" + "=" * 70)
    print("📊 TRUY VẤN 3: Thống kê tất cả giáo viên")
    print("=" * 70)
    
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teacher ?name ?teacherId ?expertise (COUNT(?class) as ?num_classes)
    WHERE {
        ?teacher a edu:Teacher .
        ?teacher rdfs:label ?name .
        OPTIONAL { ?teacher edu:teacherId ?teacherId . }
        OPTIONAL { ?teacher edu:expertise ?expertise . }
        OPTIONAL { ?teacher edu:teaches ?class . }
    }
    GROUP BY ?teacher ?name ?teacherId ?expertise
    ORDER BY DESC(?num_classes)
    """
    
    results = g.query(query)
    
    print("\n📋 Thống kê giáo viên:")
    print("-" * 70)
    print(f"{'STT':<5} {'Tên giáo viên':<30} {'ID':<10} {'Chuyên môn':<15} {'Số lớp'}")
    print("-" * 70)
    
    for i, row in enumerate(results, 1):
        name = row.name if row.name else 'N/A'
        tid = row.teacherId if row.teacherId else 'N/A'
        exp = row.expertise if row.expertise else 'N/A'
        num_classes = int(row.num_classes) if row.num_classes else 0
        print(f"{i:<5} {name:<30} {tid:<10} {exp:<15} {num_classes}")
    
    # ============================================
    # 4. Truy vấn: Phân công lớp theo giáo viên
    # ============================================
    print("\n" + "=" * 70)
    print("📚 TRUY VẤN 4: Chi tiết phân công lớp của từng giáo viên")
    print("=" * 70)
    
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teacher ?name ?teacherId ?class ?className
    WHERE {{
        ?teacher a edu:Teacher .
        ?teacher rdfs:label ?name .
        ?teacher edu:teacherId ?teacherId .
        ?teacher edu:teaches ?class .
        ?class edu:className ?className .
    }}
    ORDER BY ?teacherId ?className
    """
    
    results = g.query(query)
    
    # Hiển thị với định dạng đẹp
    current_teacher = None
    class_list = []
    teacher_name = None
    
    for row in results:
        if current_teacher != row.teacherId:
            if current_teacher is not None and class_list:
                print(f"   {', '.join(class_list)} ({len(class_list)} lớp)")
                print()
            current_teacher = row.teacherId
            teacher_name = row.name
            print(f"👨‍🏫 {teacher_name} (ID: {row.teacherId}):")
            class_list = []
        class_list.append(row.className)
    
    if class_list and teacher_name:
        print(f"   {', '.join(class_list)} ({len(class_list)} lớp)")
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH DEMO CÁC TRUY VẤN")
    print("=" * 70)

if __name__ == '__main__':
    main()

