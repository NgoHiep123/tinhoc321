# 🎓 HỆ THỐNG HỖ TRỢ GIÁO VIÊN THCS NÂNG CAO CHẤT LƯỢNG GIẢNG DẠY TIN HỌC DỰA TRÊN KNOWLEDGE GRAPH

> Đề án tốt nghiệp Thạc sĩ - Khoa Công nghệ Thông tin

## 📋 MÔ TẢ DỰ ÁN

Hệ thống hỗ trợ giáo viên THCS trong việc giảng dạy môn Tin học thông qua:
- **Knowledge Graph (KG)**: Mô hình hóa tri thức về chủ đề, bài học, câu hỏi, học sinh
- **K-Nearest Neighbors (KNN)**: Phát hiện học sinh yếu ở các chủ đề cụ thể
- **Personalized PageRank (PPR)**: Gợi ý bài học phù hợp cho từng học sinh

## 🏗️ KIẾN TRÚC HỆ THỐNG

```
A_De_tai_Tot_nghiep/
│
├── KG_Design/                    # Thiết kế và xây dựng Knowledge Graph
│   ├── kg_schema_grade7.ttl     # Schema KG (RDF/Turtle)
│   ├── build_kg_grade7.py       # Script xây dựng KG
│   ├── query_kg.py              # Truy vấn SPARQL
│   └── kg_grade7.ttl            # KG đã xây dựng (output)
│
├── ML_Algorithms/                # Thuật toán Machine Learning
│   ├── knn_student_analysis.py  # KNN - Phát hiện học sinh yếu
│   └── ppr_recommendation.py    # PPR - Gợi ý bài học
│
├── Web/                          # Giao diện học sinh
│   ├── index.html               # Trang chủ
│   ├── login.html               # Đăng nhập
│   ├── A1.html, A2.html, ...    # Các bài trắc nghiệm
│   └── students.json            # Dữ liệu học sinh
│
├── Web_Teacher/                  # Giao diện giáo viên
│   └── dashboard.html           # Dashboard phân tích & gợi ý
│
├── Bai_tap_Tin_7/               # Ngân hàng câu hỏi
│   └── question_bank_grade7_all_canonical.csv
│
├── Giao_an 6-7-8-9/             # Giáo án các khối
├── Sach_giao_khoa_Tin_*.pdf     # Sách giáo khoa
├── Tai_lieu_tham_khao/          # Tài liệu nghiên cứu
│
├── requirements.txt             # Dependencies Python
└── README.md                    # File này
```

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### 1. Cài đặt Python và Dependencies

```bash
# Yêu cầu: Python 3.8+
python --version

# Cài đặt các thư viện
pip install -r requirements.txt
```

### 2. Xây dựng Knowledge Graph

```bash
cd KG_Design

# Chạy script xây dựng KG từ dữ liệu
python build_kg_grade7.py

# Output: kg_grade7.ttl (file RDF/Turtle)
```

### 3. Chạy thuật toán KNN (Phát hiện học sinh yếu)

```bash
cd ML_Algorithms

# Chạy KNN để phân tích học sinh yếu
python knn_student_analysis.py

# Output: kg_grade7_with_knn.ttl (KG + thông tin học sinh yếu)
```

### 4. Chạy thuật toán PPR (Gợi ý bài học)

```bash
# Tiếp tục trong ML_Algorithms
python ppr_recommendation.py

# Output: kg_grade7_with_ppr.ttl (KG + gợi ý bài học)
```

### 5. Truy vấn Knowledge Graph

```bash
cd KG_Design

# Demo các truy vấn SPARQL
python query_kg.py
```

### 6. Khởi chạy Web Interface

#### Giao diện học sinh:
```bash
cd Web

# Mở bằng browser (khuyến nghị: Live Server trong VS Code)
# hoặc dùng Python HTTP Server:
python -m http.server 8000

# Truy cập: http://localhost:8000/index.html
```

#### Giao diện giáo viên:
```bash
cd Web_Teacher

# Mở dashboard.html bằng browser
# hoặc:
python -m http.server 8001

# Truy cập: http://localhost:8001/dashboard.html
```

## 📊 DỮ LIỆU

### Dữ liệu hiện có (Khối 7):
- ✅ **Học sinh**: 143 học sinh (5 lớp: 7/19, 7/20, 7/21, 7/22, 7/23)
- ✅ **Câu hỏi**: 40 câu (4 bài: A1, A2, A4, A5)
- ✅ **Kết quả**: Lưu trên Google Sheets qua Apps Script

### Cần bổ sung:
- ⚠️ **Kết quả trắc nghiệm**: Export từ Google Sheets về file CSV `test_results.csv`
- ⚠️ **Thêm bài học**: A3, B1-B6, C1-C3, D1-D4, E1-E6, F1-F2 (theo đề cương)
- ⚠️ **Mở rộng khối**: Khối 6, 8, 9

### Format file `test_results.csv`:

```csv
timestamp,student_name,class_name,quiz_id,score,total,duration
2025-01-15 10:30:00,Trần Thái,7/19,A1,7.0,10,450
2025-01-15 11:00:00,Lê Gia,7/19,A1,5.0,10,600
...
```

## 🔍 CÁC TRUY VẤN SPARQL MẪU

### 1. Danh sách học sinh trong lớp
```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?name
WHERE {
  ?class edu:className "7/19" .
  ?student edu:belongsToClass ?class .
  ?student edu:fullName ?name .
}
```

### 2. Học sinh yếu ở chủ đề A
```sparql
PREFIX edu: <http://education.vn/ontology#>

SELECT ?student ?name ?topic
WHERE {
  ?student edu:weakInTopic ?topic .
  ?student edu:fullName ?name .
  FILTER(CONTAINS(STR(?topic), "topic_7A"))
}
```

### 3. Gợi ý bài học cho học sinh
```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?lesson ?lessonName
WHERE {
  ?student edu:fullName "Trần Thái" .
  ?lesson edu:recommendedFor ?student .
  ?lesson rdfs:label ?lessonName .
}
```

## 📈 KẾT QUẢ MINH HỌA

### Thống kê KNN (Phát hiện học sinh yếu):
```
✅ Hoàn thành huấn luyện. Độ chính xác: 87.5%
✅ Tìm thấy 28 học sinh yếu

TOP 3 học sinh cần can thiệp:
1. Trần Thái        | Chủ đề A | Điểm: 4.2 | Xác suất: 92%
2. Lê Gia           | Chủ đề B | Điểm: 4.5 | Xác suất: 88%
3. Nguyễn Thiên     | Chủ đề A | Điểm: 4.8 | Xác suất: 85%
```

### Gợi ý PPR (Top 3 bài học cho Trần Thái):
```
1. Bài A1: Thiết bị vào-ra cơ bản (PPR: 0.0234)
2. Bài A2: Các thiết bị vào-ra (PPR: 0.0189)
3. Bài A4: Chức năng hệ điều hành (PPR: 0.0156)
```

## 🛠️ CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|-----------|-----------|
| Knowledge Graph | RDFLib (Python), Turtle Format |
| Truy vấn | SPARQL |
| Machine Learning | scikit-learn (KNN), NetworkX (PPR) |
| Frontend | HTML5, TailwindCSS, Chart.js |
| Backend (Web) | Google Apps Script (để lưu kết quả) |
| Lưu trữ KG | File RDF/Turtle (có thể chuyển sang GraphDB) |

## 📝 DANH SÁCH KIỂM TRA (TODO)

### ✅ Đã hoàn thành:
- [x] Thiết kế schema Knowledge Graph
- [x] Script xây dựng KG từ dữ liệu
- [x] Script truy vấn SPARQL
- [x] Thuật toán KNN phát hiện học sinh yếu
- [x] Thuật toán PPR gợi ý bài học
- [x] Giao diện học sinh (trắc nghiệm)
- [x] Giao diện giáo viên (dashboard)
- [x] Tài liệu README

### ⚠️ Cần hoàn thành:
- [ ] **Export kết quả từ Google Sheets** về `test_results.csv`
- [ ] **Chạy pipeline**: build KG → KNN → PPR với dữ liệu thực
- [ ] **Thêm câu hỏi** cho các bài còn lại (B, C, D, E, F)
- [ ] **Backend API** (Flask) để kết nối dashboard với KG
- [ ] **Trực quan hóa KG** (D3.js hoặc Cytoscape.js)
- [ ] **Viết luận văn**: Chương 3, 4 (Xây dựng và Thử nghiệm)
- [ ] **Mở rộng khối 6, 8, 9** (sau khi hoàn thiện khối 7)

## 📄 TÀI LIỆU THAM KHẢO

Xem thư mục `Tai_lieu_tham_khao/` (18 papers về KG, ML trong giáo dục)

## 👤 TÁC GIẢ

**Tên**: [Tên bạn]  
**Trường**: [Tên trường]  
**Khoa**: Công nghệ Thông tin  
**Email**: [Email của bạn]

## 📞 LIÊN HỆ HỖ TRỢ

Nếu gặp vấn đề khi chạy hệ thống:
1. Kiểm tra Python version: `python --version` (cần >= 3.8)
2. Kiểm tra dependencies: `pip list`
3. Đảm bảo file `students.json` và CSV câu hỏi có trong thư mục đúng
4. Xem log lỗi để debug

---

**Chúc bạn hoàn thành tốt đề án! 🎉**

