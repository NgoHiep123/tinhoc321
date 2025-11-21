"""
Script kiểm tra kết nối đến GraphDB
"""

from query_graphdb import GraphDBClient

def main():
    print("=" * 60)
    print("🔌 KIỂM TRA KẾT NỐI GRAPHDB")
    print("=" * 60)
    
    client = GraphDBClient()
    
    print(f"\n📡 Thông tin kết nối:")
    print(f"   Server: {client.server}")
    print(f"   Repository: {client.repository}")
    print(f"   Username: {client.username}")
    
    print(f"\n🔄 Đang kiểm tra kết nối...")
    
    # Test 1: Kiểm tra kết nối cơ bản
    if client.test_connection():
        print("\n✅ Kết nối thành công!")
        
        # Test 2: Đếm triples
        count = client.count_triples()
        print(f"📊 Số triples: {count}")
        
        # Test 3: Query đơn giản
        print(f"\n🔍 Test query đơn giản...")
        query = """
        PREFIX edu: <http://education.vn/ontology#>
        SELECT (COUNT(DISTINCT ?s) as ?count)
        WHERE {
            ?s a edu:Student .
        }
        """
        results = client.query(query)
        if results:
            student_count = results[0].get('count', '0')
            print(f"   Số học sinh: {student_count}")
        
        print("\n" + "=" * 60)
        print("✅ TẤT CẢ KIỂM TRA THÀNH CÔNG")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ KẾT NỐI THẤT BẠI")
        print("=" * 60)
        print("\n💡 Kiểm tra:")
        print("   1. GraphDB Desktop đã khởi động chưa?")
        print("   2. Repository đã được tạo chưa?")
        print("   3. File .env có đúng cấu hình không?")
        print("   4. Đã import dữ liệu vào repository chưa?")

if __name__ == '__main__':
    main()

