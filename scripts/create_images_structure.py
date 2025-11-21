"""
Script tạo cấu trúc thư mục hình ảnh cho các bài học
"""

import os
from pathlib import Path

# Thư mục gốc
BASE_DIR = Path(__file__).parent.parent
WEB_DIR = BASE_DIR / "Web"
IMAGES_DIR = WEB_DIR / "images"

# Cấu trúc thư mục cần tạo
STRUCTURE = {
    "K6": [
        "A1", "A2", "A3", "A4", "A5", "A6",
        "B1", "B2", "B3", "B4",
        "C1", "C2", "C3", "C4", "C5", "C6",
        "D1", "D2", "D3",
        "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
        "F1", "F2", "F3", "F4", "F5"
    ],
    "K7": [
        "A1", "A2", "A3", "A4", "A5", "A6",
        "B1", "B2", "B3",
        "C1", "C2", "C3",
        "D1", "D2", "D3", "D4",
        "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15",
        "F1", "F2", "F3", "F4", "F5"
    ],
    "common": []  # Thư mục dùng chung
}

def create_structure():
    """Tạo cấu trúc thư mục hình ảnh"""
    print("=" * 60)
    print("📁 TẠO CẤU TRÚC THƯ MỤC HÌNH ẢNH")
    print("=" * 60)
    
    # Tạo thư mục images chính
    IMAGES_DIR.mkdir(exist_ok=True)
    print(f"✅ Đã tạo: {IMAGES_DIR}")
    
    # Tạo thư mục cho từng khối
    for grade, lessons in STRUCTURE.items():
        grade_dir = IMAGES_DIR / grade
        grade_dir.mkdir(exist_ok=True)
        print(f"\n📂 Khối {grade}:")
        
        # Tạo thư mục cho từng bài
        for lesson in lessons:
            lesson_dir = grade_dir / lesson
            lesson_dir.mkdir(exist_ok=True)
            
            # Tạo file README.md trong mỗi thư mục
            readme_file = lesson_dir / "README.md"
            if not readme_file.exists():
                readme_content = f"""# Hình ảnh cho bài {grade} - {lesson}

## Hướng dẫn:

1. Đặt các file ảnh vào thư mục này
2. Đặt tên file rõ ràng: `question1.jpg`, `keyboard.png`, etc.
3. Sử dụng trong code: `image: "images/{grade}/{lesson}/question1.jpg"`

## Format khuyến nghị:

- **Format**: JPG, PNG, WebP
- **Kích thước**: < 500KB mỗi ảnh
- **Độ phân giải**: 800x600 hoặc 1200x800px
"""
                readme_file.write_text(readme_content, encoding='utf-8')
                print(f"  ✅ {grade}/{lesson}/")
    
    # Tạo thư mục common
    common_dir = IMAGES_DIR / "common"
    common_dir.mkdir(exist_ok=True)
    print(f"\n📂 Hình ảnh dùng chung:")
    print(f"  ✅ common/")
    
    # Tạo file .gitkeep để giữ thư mục trong git
    gitkeep = IMAGES_DIR / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("# Thư mục chứa hình ảnh cho câu hỏi\n")
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH TẠO CẤU TRÚC")
    print("=" * 60)
    print(f"\n📁 Thư mục gốc: {IMAGES_DIR}")
    print(f"\n💡 Bây giờ bạn có thể:")
    print("   1. Đặt hình ảnh vào các thư mục tương ứng")
    print("   2. Sử dụng trong code: image: 'images/K6/A1/question1.jpg'")
    print("   3. Xem hướng dẫn: HUONG_DAN_HINH_ANH.md")

if __name__ == '__main__':
    create_structure()


