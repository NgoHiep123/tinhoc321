"""
Script import Knowledge Graph vào GraphDB Desktop
Sử dụng REST API của GraphDB để upload dữ liệu
"""

import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Cấu hình GraphDB
GRAPHDB_SERVER = os.getenv('GRAPHDB_SERVER', 'http://localhost:7200')
GRAPHDB_REPOSITORY = os.getenv('GRAPHDB_REPOSITORY', 'tin_hoc_thcs')
GRAPHDB_USERNAME = os.getenv('GRAPHDB_USERNAME', 'admin')
GRAPHDB_PASSWORD = os.getenv('GRAPHDB_PASSWORD', 'root')

def check_repository_exists():
    """Kiểm tra repository có tồn tại không"""
    url = f"{GRAPHDB_SERVER}/rest/repositories"
    
    try:
        response = requests.get(url, auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD))
        if response.status_code == 200:
            repos = response.json()
            repo_ids = [repo['id'] for repo in repos]
            
            if GRAPHDB_REPOSITORY in repo_ids:
                print(f"✅ Repository '{GRAPHDB_REPOSITORY}' đã tồn tại")
                return True
            else:
                print(f"⚠️  Repository '{GRAPHDB_REPOSITORY}' chưa tồn tại")
                print(f"📋 Danh sách repository hiện có: {', '.join(repo_ids)}")
                return False
        else:
            print(f"❌ Lỗi kết nối GraphDB: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Không thể kết nối đến GraphDB tại {GRAPHDB_SERVER}")
        print("💡 Hãy đảm bảo GraphDB Desktop đã được khởi động")
        return False

def clear_repository():
    """Xóa tất cả dữ liệu trong repository (tùy chọn)"""
    url = f"{GRAPHDB_SERVER}/repositories/{GRAPHDB_REPOSITORY}/statements"
    
    response = requests.delete(url, auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD))
    
    if response.status_code == 204:
        print("🗑️  Đã xóa dữ liệu cũ trong repository")
        return True
    else:
        print(f"⚠️  Không thể xóa dữ liệu cũ: {response.status_code}")
        return False

def import_turtle_file(turtle_file, clear_first=False):
    """
    Import file Turtle vào GraphDB
    
    Args:
        turtle_file: Đường dẫn đến file .ttl
        clear_first: Có xóa dữ liệu cũ trước khi import không
    """
    # Kiểm tra file tồn tại
    if not os.path.exists(turtle_file):
        print(f"❌ File không tồn tại: {turtle_file}")
        return False
    
    # Kiểm tra repository
    if not check_repository_exists():
        print("❌ Vui lòng tạo repository trước trong GraphDB Desktop")
        return False
    
    # Xóa dữ liệu cũ nếu cần
    if clear_first:
        clear_repository()
    
    # Đọc file Turtle
    print(f"📖 Đang đọc file: {turtle_file}")
    with open(turtle_file, 'r', encoding='utf-8') as f:
        turtle_content = f.read()
    
    # URL để import
    url = f"{GRAPHDB_SERVER}/repositories/{GRAPHDB_REPOSITORY}/statements"
    
    # Headers
    headers = {
        'Content-Type': 'application/x-turtle'
    }
    
    print(f"📤 Đang upload lên GraphDB...")
    print(f"   Server: {GRAPHDB_SERVER}")
    print(f"   Repository: {GRAPHDB_REPOSITORY}")
    
    # Upload
    response = requests.post(
        url,
        data=turtle_content.encode('utf-8'),
        headers=headers,
        auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD)
    )
    
    if response.status_code == 204:
        print("✅ Import thành công!")
        
        # Đếm số triples
        count = count_triples()
        print(f"📊 Tổng số triples trong repository: {count}")
        return True
    else:
        print(f"❌ Lỗi khi import: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def count_triples():
    """Đếm số triples trong repository"""
    query = "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
    
    url = f"{GRAPHDB_SERVER}/repositories/{GRAPHDB_REPOSITORY}/sparql"
    
    params = {
        'query': query
    }
    
    try:
        response = requests.get(
            url,
            params=params,
            headers={'Accept': 'application/sparql-results+json'},
            auth=(GRAPHDB_USERNAME, GRAPHDB_PASSWORD)
        )
        
        if response.status_code == 200:
            data = response.json()
            count = data['results']['bindings'][0]['count']['value']
            return int(count)
        else:
            return 0
    except:
        return 0

def main():
    """Hàm chính"""
    print("=" * 60)
    print("🚀 IMPORT KNOWLEDGE GRAPH VÀO GRAPHDB")
    print("=" * 60)
    
    # Tìm file Turtle
    turtle_files = [
        'kg_grade7.ttl',
        'kg_grade7_with_knn.ttl',
        'kg_grade7_with_ppr.ttl'
    ]
    
    # Tìm file nào có sẵn
    available_file = None
    for file in turtle_files:
        if os.path.exists(file):
            available_file = file
            break
    
    if not available_file:
        print("❌ Không tìm thấy file Turtle nào!")
        print("💡 Hãy chạy build_kg_grade7.py trước để tạo file KG")
        return
    
    print(f"📁 File sẽ import: {available_file}")
    
    # Hỏi có muốn xóa dữ liệu cũ không
    print("\n⚠️  Bạn có muốn xóa dữ liệu cũ trong repository không?")
    print("   (Nhấn Enter để bỏ qua, gõ 'yes' để xóa)")
    choice = input("   > ").strip().lower()
    
    clear_first = (choice == 'yes')
    
    # Import
    success = import_turtle_file(available_file, clear_first=clear_first)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ HOÀN THÀNH IMPORT")
        print("=" * 60)
        print(f"\n💡 Bạn có thể kiểm tra trong GraphDB Desktop:")
        print(f"   - Mở repository '{GRAPHDB_REPOSITORY}'")
        print(f"   - Vào tab 'SPARQL' để chạy query")
    else:
        print("\n" + "=" * 60)
        print("❌ IMPORT THẤT BẠI")
        print("=" * 60)
        print("\n💡 Kiểm tra:")
        print("   1. GraphDB Desktop đã khởi động chưa?")
        print("   2. Repository đã được tạo chưa?")
        print("   3. Thông tin trong file .env có đúng không?")

if __name__ == '__main__':
    main()

