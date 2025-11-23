"""
Script test dữ liệu giáo viên trong Knowledge Graph
"""

import sys
import io
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

print("=" * 60)
print("🔍 KIỂM TRA DỮ LIỆU GIÁO VIÊN TRONG KNOWLEDGE GRAPH")
print("=" * 60)

# Tải KG
g = Graph()
g.parse('kg_grade7.ttl', format='turtle')
g.bind('edu', EDU)
g.bind('data', DATA)

# Đếm giáo viên và phân công lớp
teachers = list(g.subjects(RDF.type, EDU.Teacher))
teaches = list(g.subject_objects(EDU.teaches))

print(f"\n✅ Kết quả tích hợp:")
print(f"📊 Số giáo viên: {len(teachers)}")
print(f"📚 Số phân công lớp: {len(teaches)}")

# Liệt kê giáo viên
print(f"\n📋 Danh sách giáo viên:")
for i, teacher in enumerate(teachers, 1):
    name = g.value(teacher, RDFS.label)
    tid = g.value(teacher, EDU.teacherId)
    exp = g.value(teacher, EDU.expertise)
    print(f"  {i}. {name} (ID: {tid}) - {exp}")

# Ví dụ: Các lớp giáo viên tin_01 dạy
print(f"\n📚 Ví dụ: Các lớp giáo viên 'tin_01' dạy:")
teacher_uri = DATA['teacher_tin_01']
if (teacher_uri, RDF.type, EDU.Teacher) in g:
    teacher_name = g.value(teacher_uri, RDFS.label)
    classes = list(g.objects(teacher_uri, EDU.teaches))
    print(f"   Tên: {teacher_name}")
    print(f"   Số lớp: {len(classes)}")
    for i, class_uri in enumerate(classes[:10], 1):
        class_name = g.value(class_uri, EDU.className)
        print(f"   {i}. {class_name}")
    if len(classes) > 10:
        print(f"   ... và {len(classes) - 10} lớp khác")
else:
    print("   ⚠️ Không tìm thấy giáo viên tin_01")

print("\n" + "=" * 60)
print("✅ Hoàn thành kiểm tra!")
print("=" * 60)

