"""
Script export dữ liệu giáo viên từ Knowledge Graph sang JSON
Để sử dụng với dashboard HTML
"""

import sys
import io
import json
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

def export_teachers_to_json(kg_file='kg_grade7.ttl', output_file='teachers_data.json'):
    """Export dữ liệu giáo viên sang JSON"""
    
    print("=" * 70)
    print("📤 EXPORT DỮ LIỆU GIÁO VIÊN SANG JSON")
    print("=" * 70)
    
    # Tải KG
    print(f"\n📖 Đang tải Knowledge Graph từ {kg_file}...")
    g = Graph()
    g.parse(kg_file, format='turtle')
    g.bind('edu', EDU)
    g.bind('data', DATA)
    print(f"✅ Đã tải {len(g)} triples\n")
    
    # Truy vấn tất cả giáo viên và phân công lớp
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teacher ?name ?teacherId ?expertise ?className
    WHERE {{
        ?teacher a edu:Teacher .
        ?teacher rdfs:label ?name .
        OPTIONAL {{ ?teacher edu:teacherId ?teacherId . }}
        OPTIONAL {{ ?teacher edu:expertise ?expertise . }}
        OPTIONAL {{
            ?teacher edu:teaches ?class .
            ?class edu:className ?className .
        }}
    }}
    ORDER BY ?teacherId ?className
    """
    
    results = g.query(query)
    
    # Nhóm dữ liệu theo giáo viên
    teachers_dict = {}
    
    for row in results:
        teacher_id = str(row.teacherId) if row.teacherId else 'unknown'
        
        if teacher_id not in teachers_dict:
            teachers_dict[teacher_id] = {
                'teacherId': teacher_id,
                'name': str(row.name) if row.name else 'N/A',
                'expertise': str(row.expertise) if row.expertise else 'Tin học',
                'classes': []
            }
        
        if row.className and str(row.className) not in teachers_dict[teacher_id]['classes']:
            teachers_dict[teacher_id]['classes'].append(str(row.className))
    
    # Chuyển thành list và sắp xếp
    teachers_list = list(teachers_dict.values())
    teachers_list.sort(key=lambda x: x['teacherId'])
    
    # Tính toán thống kê
    total_teachers = len(teachers_list)
    total_assignments = sum(len(t['classes']) for t in teachers_list)
    avg_classes = total_assignments / total_teachers if total_teachers > 0 else 0
    
    stats = {
        'total_teachers': total_teachers,
        'total_assignments': total_assignments,
        'avg_classes_per_teacher': round(avg_classes, 2)
    }
    
    # Tạo dữ liệu JSON
    data = {
        'stats': stats,
        'teachers': teachers_list
    }
    
    # Ghi file JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Đã export dữ liệu:")
    print(f"   📊 Số giáo viên: {total_teachers}")
    print(f"   📚 Số phân công: {total_assignments}")
    print(f"   📈 Trung bình: {avg_classes:.2f} lớp/giáo viên")
    print(f"\n💾 Đã lưu vào file: {output_file}")
    print("=" * 70)
    
    return data

if __name__ == '__main__':
    export_teachers_to_json()

