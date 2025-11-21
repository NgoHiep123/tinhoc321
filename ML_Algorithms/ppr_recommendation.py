"""
Thuật toán Personalized PageRank (PPR)
Mục đích: Gợi ý bài học phù hợp cho học sinh dựa trên chủ đề yếu
"""

import numpy as np
import networkx as nx
from rdflib import Graph, Namespace, URIRef
from collections import defaultdict

EDU = Namespace("http://education.vn/ontology#")
DATA = Namespace("http://education.vn/data/")

# ============================================
# 1. CHUYỂN ĐỔI KG THÀNH NETWORKX GRAPH
# ============================================

def kg_to_networkx(kg_file='../KG_Design/kg_grade7_with_knn.ttl'):
    """
    Chuyển đổi RDF Knowledge Graph thành NetworkX directed graph
    """
    print("🔄 Đang chuyển đổi KG sang NetworkX graph...")
    
    # Đọc KG
    g_rdf = Graph()
    g_rdf.parse(kg_file, format='turtle')
    
    # Tạo NetworkX graph
    G = nx.DiGraph()
    
    # Thêm các node và edge
    for s, p, o in g_rdf:
        # Chỉ thêm các triple có object là URI (không phải literal)
        if isinstance(o, URIRef):
            G.add_edge(str(s), str(o), relation=str(p))
    
    print(f"✅ Đã tạo graph với {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    return G, g_rdf

# ============================================
# 2. TRÍCH XUẤT HỌC SINH YẾU TỪ KG
# ============================================

def extract_weak_students(g_rdf):
    """
    Lấy danh sách (học sinh, chủ đề yếu) từ KG
    """
    print("📋 Đang trích xuất học sinh yếu...")
    
    query = """
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?student ?studentName ?topic ?topicName
    WHERE {
        ?student edu:weakInTopic ?topic .
        ?student edu:fullName ?studentName .
        
        OPTIONAL {
            ?topic rdfs:label ?topicName .
        }
    }
    """
    
    results = g_rdf.query(query)
    
    weak_pairs = []
    for row in results:
        weak_pairs.append({
            'student': str(row.student),
            'student_name': str(row.studentName),
            'topic': str(row.topic),
            'topic_name': str(row.topicName) if row.topicName else ''
        })
    
    print(f"✅ Tìm thấy {len(weak_pairs)} cặp (học sinh, chủ đề yếu)")
    
    if len(weak_pairs) == 0:
        print("⚠️  Không có dữ liệu học sinh yếu. Chạy KNN trước!")
    
    return weak_pairs

# ============================================
# 3. THUẬT TOÁN PERSONALIZED PAGERANK
# ============================================

def personalized_pagerank(G, start_nodes, alpha=0.85, max_iter=100):
    """
    Chạy PPR từ các start_nodes
    
    Args:
        G: NetworkX graph
        start_nodes: List các node khởi đầu (học sinh, chủ đề yếu)
        alpha: Tham số damping (0.85 là giá trị phổ biến)
        max_iter: Số vòng lặp tối đa
    
    Returns:
        scores: Dict {node: PPR_score}
    """
    # Tạo personalization vector
    personalization = {node: 0 for node in G.nodes()}
    for node in start_nodes:
        if node in personalization:
            personalization[node] = 1.0 / len(start_nodes)
    
    # Chạy PPR
    try:
        scores = nx.pagerank(G, alpha=alpha, personalization=personalization, max_iter=max_iter)
    except Exception as e:
        print(f"⚠️  Lỗi khi chạy PPR: {e}")
        scores = {}
    
    return scores

# ============================================
# 4. LỌC VÀ XẾP HẠNG BÀI HỌC
# ============================================

def rank_lessons_for_student(G, g_rdf, student_uri, topic_uri, top_k=5):
    """
    Gợi ý top-k bài học phù hợp nhất cho học sinh yếu ở chủ đề
    
    Args:
        G: NetworkX graph
        g_rdf: RDF graph (để query metadata)
        student_uri: URI của học sinh
        topic_uri: URI của chủ đề yếu
        top_k: Số bài học gợi ý
    
    Returns:
        recommendations: List các bài học được xếp hạng
    """
    # Chạy PPR từ 2 node: student và topic
    start_nodes = [student_uri, topic_uri]
    scores = personalized_pagerank(G, start_nodes)
    
    # Lọc các node là Lesson
    lesson_scores = {}
    for node, score in scores.items():
        if 'lesson_7' in node:  # Chỉ lấy lessons khối 7
            lesson_scores[node] = score
    
    # Sắp xếp theo điểm PPR giảm dần
    sorted_lessons = sorted(lesson_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Lấy top-k
    top_lessons = sorted_lessons[:top_k]
    
    # Lấy metadata của lessons
    recommendations = []
    for lesson_uri, score in top_lessons:
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {{
            <{lesson_uri}> rdfs:label ?label .
        }}
        """
        result = g_rdf.query(query)
        
        label = "Unknown"
        for row in result:
            label = str(row.label)
            break
        
        recommendations.append({
            'lesson_uri': lesson_uri,
            'lesson_name': label,
            'ppr_score': score
        })
    
    return recommendations

# ============================================
# 5. TẠO GỢI Ý CHO TẤT CẢ HỌC SINH YẾU
# ============================================

def generate_recommendations_for_all(G, g_rdf, weak_pairs, top_k=3):
    """
    Tạo gợi ý cho tất cả học sinh yếu
    """
    print(f"💡 Đang tạo gợi ý (top-{top_k}) cho các học sinh yếu...")
    
    all_recommendations = []
    
    for i, pair in enumerate(weak_pairs, 1):
        student_uri = pair['student']
        topic_uri = pair['topic']
        
        recommendations = rank_lessons_for_student(G, g_rdf, student_uri, topic_uri, top_k)
        
        all_recommendations.append({
            'student_name': pair['student_name'],
            'student_uri': student_uri,
            'topic_name': pair['topic_name'],
            'topic_uri': topic_uri,
            'recommendations': recommendations
        })
        
        if i % 10 == 0:
            print(f"   Đã xử lý {i}/{len(weak_pairs)} học sinh...")
    
    print(f"✅ Hoàn thành tạo gợi ý cho {len(all_recommendations)} học sinh")
    
    return all_recommendations

# ============================================
# 6. CẬP NHẬT KG VỚI GỢI Ý
# ============================================

def update_kg_with_recommendations(g_rdf, all_recommendations, output_file='../KG_Design/kg_grade7_with_ppr.ttl'):
    """
    Thêm quan hệ recommendedFor vào KG
    """
    print("💾 Đang cập nhật KG với gợi ý...")
    
    g_rdf.bind("edu", EDU)
    g_rdf.bind("data", DATA)
    
    count = 0
    for rec in all_recommendations:
        student_uri = URIRef(rec['student_uri'])
        
        for lesson in rec['recommendations']:
            lesson_uri = URIRef(lesson['lesson_uri'])
            g_rdf.add((lesson_uri, EDU.recommendedFor, student_uri))
            count += 1
    
    # Lưu KG
    g_rdf.serialize(destination=output_file, format='turtle')
    
    print(f"✅ Đã thêm {count} gợi ý vào KG")
    print(f"💾 KG mới được lưu tại: {output_file}")

# ============================================
# 7. BÁO CÁO GỢI Ý
# ============================================

def generate_report(all_recommendations):
    """
    Tạo báo cáo gợi ý cho giáo viên
    """
    print("\n" + "=" * 80)
    print("📊 BÁO CÁO GỢI Ý BÀI HỌC CÁ NHÂN HÓA")
    print("=" * 80)
    
    # Hiển thị 10 gợi ý đầu tiên
    print("\n💡 10 GỢI Ý ĐẦU TIÊN:")
    print("-" * 80)
    
    for i, rec in enumerate(all_recommendations[:10], 1):
        topic_id = rec['topic_uri'].split('_')[-1]
        
        print(f"\n{i}. {rec['student_name']} - Yếu ở chủ đề {topic_id}")
        print("   Bài học được gợi ý:")
        
        for j, lesson in enumerate(rec['recommendations'], 1):
            lesson_id = lesson['lesson_uri'].split('_')[-1]
            print(f"      {j}. Bài {lesson_id}: {lesson['lesson_name']} (PPR: {lesson['ppr_score']:.4f})")
    
    # Thống kê
    total_recommendations = sum(len(r['recommendations']) for r in all_recommendations)
    print(f"\n📈 TỔNG KẾT:")
    print(f"   - Số học sinh nhận gợi ý: {len(all_recommendations)}")
    print(f"   - Tổng số gợi ý: {total_recommendations}")
    print(f"   - Trung bình: {total_recommendations / len(all_recommendations):.1f} gợi ý/học sinh")
    
    print("\n" + "=" * 80)

# ============================================
# 8. MAIN FUNCTION
# ============================================

def main():
    """Hàm chính"""
    print("=" * 80)
    print("🚀 THUẬT TOÁN PPR - GỢI Ý BÀI HỌC CÁ NHÂN HÓA")
    print("=" * 80)
    
    # 1. Chuyển đổi KG sang NetworkX
    G, g_rdf = kg_to_networkx()
    
    # 2. Trích xuất học sinh yếu
    weak_pairs = extract_weak_students(g_rdf)
    
    if len(weak_pairs) == 0:
        print("⚠️  Không có dữ liệu. Vui lòng chạy KNN trước!")
        return
    
    # 3. Tạo gợi ý
    all_recommendations = generate_recommendations_for_all(G, g_rdf, weak_pairs, top_k=3)
    
    # 4. Cập nhật KG
    update_kg_with_recommendations(g_rdf, all_recommendations)
    
    # 5. Báo cáo
    generate_report(all_recommendations)
    
    print("\n✅ HOÀN THÀNH!")

if __name__ == '__main__':
    main()

