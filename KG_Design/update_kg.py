"""
Script tổng hợp để cập nhật Knowledge Graph sau khi thêm dữ liệu mới
Sử dụng: python update_kg.py
"""

import sys
import io
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import build script
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_kg_grade7 import main as build_kg

def update_kg():
    """Cập nhật Knowledge Graph từ dữ liệu mới"""
    print("=" * 70)
    print("🔄 CẬP NHẬT KNOWLEDGE GRAPH")
    print("=" * 70)
    
    print("\n📝 Đang xây dựng lại Knowledge Graph từ dữ liệu hiện tại...")
    print("-" * 70)
    
    try:
        build_kg()
        
        print("\n" + "=" * 70)
        print("✅ HOÀN THÀNH CẬP NHẬT KNOWLEDGE GRAPH")
        print("=" * 70)
        
        print("\n💡 Bước tiếp theo:")
        print("   1. Kiểm tra dữ liệu: python test_teachers.py")
        print("   2. Export JSON (nếu cần): python export_teachers_to_json.py")
        print("   3. Chạy truy vấn: python demo_teacher_queries.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Lỗi khi cập nhật Knowledge Graph: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Hàm chính"""
    update_kg()

if __name__ == '__main__':
    main()

