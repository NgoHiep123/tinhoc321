"""
Client để truy vấn GraphDB qua SPARQL endpoint
Thay thế cho việc đọc file Turtle local
"""

import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# Load biến môi trường
load_dotenv()

class GraphDBClient:
    """Client để kết nối và truy vấn GraphDB"""
    
    def __init__(self):
        """Khởi tạo client với cấu hình từ .env"""
        self.server = os.getenv('GRAPHDB_SERVER', 'http://localhost:7200')
        self.repository = os.getenv('GRAPHDB_REPOSITORY', 'tin_hoc_thcs')
        self.username = os.getenv('GRAPHDB_USERNAME', 'admin')
        self.password = os.getenv('GRAPHDB_PASSWORD', 'root')
        
        self.sparql_endpoint = f"{self.server}/repositories/{self.repository}/sparql"
        self.update_endpoint = f"{self.server}/repositories/{self.repository}/statements"
    
    def query(self, sparql_query: str, output_format: str = 'json') -> List[Dict[str, Any]]:
        """
        Thực hiện SPARQL SELECT query
        
        Args:
            sparql_query: Câu truy vấn SPARQL
            output_format: 'json' hoặc 'csv'
        
        Returns:
            List các dictionary chứa kết quả
        """
        params = {
            'query': sparql_query
        }
        
        headers = {
            'Accept': 'application/sparql-results+json' if output_format == 'json' else 'text/csv'
        }
        
        try:
            response = requests.get(
                self.sparql_endpoint,
                params=params,
                headers=headers,
                auth=(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 200:
                if output_format == 'json':
                    data = response.json()
                    # Chuyển đổi format
                    results = []
                    for binding in data.get('results', {}).get('bindings', []):
                        row = {}
                        for key, value in binding.items():
                            row[key] = value.get('value', '')
                        results.append(row)
                    return results
                else:
                    return response.text
            else:
                print(f"❌ Lỗi query: {response.status_code}")
                print(f"   Response: {response.text}")
                return []
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Không thể kết nối đến GraphDB tại {self.server}")
            print("💡 Hãy đảm bảo GraphDB Desktop đã được khởi động")
            return []
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return []
    
    def update(self, sparql_update: str) -> bool:
        """
        Thực hiện SPARQL UPDATE query (INSERT, DELETE, etc.)
        
        Args:
            sparql_update: Câu lệnh SPARQL UPDATE
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        headers = {
            'Content-Type': 'application/sparql-update'
        }
        
        try:
            response = requests.post(
                self.update_endpoint,
                data=sparql_update.encode('utf-8'),
                headers=headers,
                auth=(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 204:
                return True
            else:
                print(f"❌ Lỗi update: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Không thể kết nối đến GraphDB")
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def count_triples(self) -> int:
        """Đếm tổng số triples trong repository"""
        query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
        results = self.query(query)
        
        if results and 'count' in results[0]:
            return int(results[0]['count'])
        return 0
    
    def test_connection(self) -> bool:
        """Kiểm tra kết nối đến GraphDB"""
        try:
            count = self.count_triples()
            print(f"✅ Kết nối thành công!")
            print(f"   Server: {self.server}")
            print(f"   Repository: {self.repository}")
            print(f"   Số triples: {count}")
            return True
        except:
            print(f"❌ Không thể kết nối đến GraphDB")
            return False


# ============================================
# CÁC HÀM TRUY VẤN HỖ TRỢ GIÁO VIÊN
# ============================================

def query_students_by_class(client: GraphDBClient, class_name: str = '7/19') -> List[Dict]:
    """Truy vấn danh sách học sinh trong một lớp"""
    query = f"""
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?student ?name
    WHERE {{
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        ?student edu:fullName ?name .
    }}
    ORDER BY ?name
    """
    
    return client.query(query)

def query_weak_students(client: GraphDBClient, topic_id: str = 'A') -> List[Dict]:
    """Truy vấn học sinh yếu ở một chủ đề"""
    query = f"""
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?student ?name ?topic ?topicName
    WHERE {{
        ?student edu:weakInTopic ?topic .
        ?student edu:fullName ?name .
        ?topic rdfs:label ?topicName .
        FILTER(CONTAINS(STR(?topic), "topic_7{topic_id}"))
    }}
    ORDER BY ?name
    """
    
    return client.query(query)

def query_recommended_lessons(client: GraphDBClient, student_name: str, class_name: str = '7/19') -> List[Dict]:
    """Truy vấn bài học được gợi ý cho học sinh"""
    query = f"""
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?lesson ?lessonName
    WHERE {{
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        ?student edu:fullName "{student_name}" .
        
        ?lesson edu:recommendedFor ?student .
        ?lesson rdfs:label ?lessonName .
    }}
    """
    
    return client.query(query)

def query_student_performance(client: GraphDBClient, student_name: str, class_name: str = '7/19') -> List[Dict]:
    """Truy vấn kết quả học tập của một học sinh"""
    query = f"""
    PREFIX edu: <http://education.vn/ontology#>
    PREFIX data: <http://education.vn/data/>
    
    SELECT ?test ?score ?date
    WHERE {{
        ?class edu:className "{class_name}" .
        ?student edu:belongsToClass ?class .
        ?student edu:fullName "{student_name}" .
        
        ?result edu:hasResult ?student .
        ?result edu:forTest ?test .
        ?result edu:score ?score .
        ?result edu:testDate ?date .
    }}
    ORDER BY DESC(?date)
    """
    
    return client.query(query)


# ============================================
# DEMO
# ============================================

def main():
    """Hàm demo"""
    print("=" * 60)
    print("🔍 DEMO TRUY VẤN GRAPHDB")
    print("=" * 60)
    
    # Khởi tạo client
    client = GraphDBClient()
    
    # Kiểm tra kết nối
    if not client.test_connection():
        return
    
    print("\n" + "-" * 60)
    print("📋 Danh sách học sinh lớp 7/19:")
    print("-" * 60)
    students = query_students_by_class(client, '7/19')
    for i, student in enumerate(students[:10], 1):  # Hiển thị 10 học sinh đầu
        print(f"{i}. {student.get('name', 'N/A')}")
    
    print("\n" + "-" * 60)
    print("⚠️  Học sinh yếu ở chủ đề A:")
    print("-" * 60)
    weak_students = query_weak_students(client, 'A')
    if weak_students:
        for i, student in enumerate(weak_students[:5], 1):
            print(f"{i}. {student.get('name', 'N/A')}")
    else:
        print("ℹ️  Chưa có dữ liệu (cần chạy KNN trước)")
    
    print("\n" + "-" * 60)
    print("💡 Gợi ý bài học:")
    print("-" * 60)
    # Lấy học sinh đầu tiên để demo
    if students:
        first_student = students[0].get('name', '')
        recommendations = query_recommended_lessons(client, first_student, '7/19')
        if recommendations:
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec.get('lessonName', 'N/A')}")
        else:
            print("ℹ️  Chưa có gợi ý (cần chạy PPR trước)")

if __name__ == '__main__':
    main()

