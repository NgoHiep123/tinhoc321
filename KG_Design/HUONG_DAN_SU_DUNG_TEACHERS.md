# Hướng dẫn sử dụng Dashboard và Truy vấn Giáo viên

## 📋 Tổng quan

Hệ thống đã được tích hợp thành công dữ liệu giáo viên từ file `teachers_assign.csv` vào Knowledge Graph.

## ✅ Kết quả tích hợp

- **7 giáo viên** đã được thêm vào Knowledge Graph
- **52 phân công lớp** đã được tạo
- **Tổng số triples**: 1,057 triples

### Danh sách giáo viên:

1. **Ngô Tiến Hiệp** (ID: tin_01) - 11 lớp
2. **Cô Hà** (ID: tin_02) - 7 lớp
3. **Trần Gia Huy** (ID: tin_03) - 13 lớp
4. **Tuấn Anh** (ID: tin_04) - 7 lớp
5. **Trần Thị Kim Thảo** (ID: tin_05) - 6 lớp
6. **Nguyễn Đình Nhân** (ID: tin_06) - 3 lớp
7. **Nguyễn Xuân Sơn** (ID: tin_07) - 5 lớp

## 🚀 Các bước sử dụng

### 1. Build Knowledge Graph

```bash
cd KG_Design
python build_kg_grade7.py
```

Kết quả: Tạo file `kg_grade7.ttl` chứa Knowledge Graph đã tích hợp giáo viên.

### 2. Export dữ liệu sang JSON (cho Dashboard)

```bash
cd KG_Design
python export_teachers_to_json.py
```

Kết quả: Tạo file `teachers_data.json` chứa dữ liệu giáo viên dạng JSON.

### 3. Xem Dashboard HTML

**Cách 1: Sử dụng local web server (khuyến nghị)**

```bash
cd KG_Design
python run_dashboard_server.py
```

Sau đó mở trình duyệt và truy cập:
```
http://localhost:8000/teachers_dashboard.html
```

**Cách 2: Mở trực tiếp file HTML**

- Nhấp đúp vào file `teachers_dashboard.html`
- **Lưu ý**: Cách này có thể gặp lỗi CORS khi load file JSON. Nên dùng cách 1.

### 4. Chạy các truy vấn SPARQL

#### 4.1. Demo tất cả truy vấn giáo viên

```bash
cd KG_Design
python demo_teacher_queries.py
```

Kết quả: Hiển thị các truy vấn mẫu:
- Giáo viên dạy một lớp cụ thể
- Các lớp một giáo viên dạy
- Thống kê tất cả giáo viên
- Chi tiết phân công lớp

#### 4.2. Sử dụng các hàm truy vấn trong code

```python
from query_kg import load_kg, query_teacher_by_class, query_classes_by_teacher

# Tải KG
g = load_kg('kg_grade7.ttl')

# Truy vấn: Giáo viên dạy lớp 7/19
query_teacher_by_class(g, '7/19')

# Truy vấn: Các lớp giáo viên tin_01 dạy
query_classes_by_teacher(g, 'tin_01')
```

#### 4.3. Chạy demo tất cả truy vấn (bao gồm giáo viên)

```bash
cd KG_Design
python query_kg.py
```

## 📁 Các file đã tạo/cập nhật

### Files mới:

1. **`KG_Design/test_teachers.py`** - Script kiểm tra dữ liệu giáo viên
2. **`KG_Design/demo_teacher_queries.py`** - Demo các truy vấn giáo viên
3. **`KG_Design/export_teachers_to_json.py`** - Export dữ liệu sang JSON
4. **`KG_Design/teachers_dashboard.html`** - Dashboard hiển thị giáo viên
5. **`KG_Design/run_dashboard_server.py`** - Local web server cho dashboard
6. **`KG_Design/teachers_data.json`** - Dữ liệu giáo viên dạng JSON (tạo tự động)
7. **`KG_Design/HUONG_DAN_SU_DUNG_TEACHERS.md`** - File hướng dẫn này

### Files đã cập nhật:

1. **`KG_Design/build_kg_grade7.py`** - Thêm hàm `add_teachers_to_kg()`
2. **`KG_Design/kg_schema_grade7.ttl`** - Thêm thuộc tính `teacherId` và `expertise`
3. **`KG_Design/query_kg.py`** - Thêm các hàm truy vấn giáo viên:
   - `query_teacher_by_class()` - Giáo viên dạy một lớp
   - `query_classes_by_teacher()` - Các lớp một giáo viên dạy

## 🔍 Các truy vấn SPARQL mẫu

### 1. Tìm giáo viên dạy một lớp

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?teacher ?name ?teacherId ?expertise
WHERE {
    ?class edu:className "7/19" .
    ?teacher edu:teaches ?class .
    ?teacher rdfs:label ?name .
    OPTIONAL { ?teacher edu:teacherId ?teacherId . }
    OPTIONAL { ?teacher edu:expertise ?expertise . }
}
```

### 2. Tìm các lớp một giáo viên dạy

```sparql
PREFIX edu: <http://education.vn/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?teacher ?name ?class ?className
WHERE {
    ?teacher edu:teacherId "tin_01" .
    ?teacher rdfs:label ?name .
    ?teacher edu:teaches ?class .
    ?class edu:className ?className .
}
ORDER BY ?className
```

### 3. Thống kê tất cả giáo viên

```sparql
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
```

## 📊 Tính năng Dashboard

- ✅ Hiển thị thống kê tổng quan (số giáo viên, số phân công, trung bình)
- ✅ Danh sách tất cả giáo viên với thông tin chi tiết
- ✅ Hiển thị các lớp mỗi giáo viên đang dạy
- ✅ Tìm kiếm giáo viên theo tên, ID, hoặc lớp
- ✅ Giao diện đẹp, responsive, dễ sử dụng

## 🎯 Ví dụ sử dụng

### Kiểm tra giáo viên dạy lớp 7/19:

```python
from query_kg import load_kg, query_teacher_by_class

g = load_kg('kg_grade7.ttl')
query_teacher_by_class(g, '7/19')
```

Kết quả:
```
👨‍🏫 Giáo viên dạy lớp 7/19:
------------------------------------------------------------
1. Ngô Tiến Hiệp (ID: tin_01) - Chuyên môn: Tin học
```

### Xem các lớp giáo viên tin_01 dạy:

```python
from query_kg import load_kg, query_classes_by_teacher

g = load_kg('kg_grade7.ttl')
query_classes_by_teacher(g, 'tin_01')
```

Kết quả:
```
📚 Các lớp giáo viên tin_01 dạy:
------------------------------------------------------------
Giáo viên: Ngô Tiến Hiệp
Số lớp: 11
  1. 6/14
  2. 6/15
  ...
```

## 🔧 Yêu cầu

- Python 3.8+
- RDFLib: `pip install rdflib`
- Trình duyệt web hiện đại (Chrome, Firefox, Edge...)

## 📝 Lưu ý

1. File `teachers_data.json` cần được tạo lại mỗi khi KG được cập nhật:
   ```bash
   python export_teachers_to_json.py
   ```

2. Khi chạy dashboard, đảm bảo file `teachers_data.json` nằm cùng thư mục với `teachers_dashboard.html`.

3. Nếu gặp lỗi CORS khi mở file HTML trực tiếp, hãy sử dụng local web server:
   ```bash
   python run_dashboard_server.py
   ```

## ✅ Hoàn thành

Tất cả các tính năng đã được triển khai và kiểm thử thành công!

