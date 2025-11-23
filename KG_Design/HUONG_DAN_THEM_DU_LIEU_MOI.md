# Hướng dẫn Thêm Dữ Liệu Mới vào Knowledge Graph

## 📋 Tổng quan

Hướng dẫn chi tiết cách thêm **học sinh mới**, **giáo viên mới**, và **lớp mới** vào Knowledge Graph.

---

## 👥 1. Thêm Học Sinh Mới

### Cách 1: Thêm một học sinh

**Sử dụng script:**

```bash
cd KG_Design
python add_new_student.py <khối> <tên_lớp> <tên_học_sinh>
```

**Ví dụ:**

```bash
python add_new_student.py 7 7/19 "Nguyễn Văn Mới"
```

**Kết quả:**
- Học sinh được thêm vào `students.json`
- File được backup tự động (`.json.bak`)
- Dữ liệu được sắp xếp theo tên

### Cách 2: Thêm nhiều học sinh cùng lúc

**Sửa file `add_new_student.py`** trong hàm `main()`:

```python
# Thêm nhiều học sinh
add_students_batch('7', '7/19', [
    'Trần Thị Hoa',
    'Lê Văn Nam',
    'Phạm Thị Mai'
])
```

Sau đó chạy:
```bash
python add_new_student.py
```

### Cách 3: Thêm từ file CSV

**Tạo file CSV** với format:

```csv
grade,class,student_name
7,7/19,Nguyễn Văn A
7,7/19,Trần Thị B
7,7/20,Lê Văn C
```

**Chạy script:**

```bash
python add_new_student.py
```

Và uncomment phần code trong hàm `main()`:
```python
add_students_from_file('new_students.csv')
```

### Cách 4: Sửa trực tiếp file `students.json`

**Cấu trúc file:**

```json
{
  "7": {
    "7/19": [
      {
        "name": "Nguyễn Văn A",
        "pass_hash": ""
      }
    ]
  }
}
```

**Lưu ý:**
- Thêm học sinh vào đúng khối và lớp
- Sắp xếp theo tên để dễ quản lý
- `pass_hash` có thể để trống hoặc thêm sau

---

## 👨‍🏫 2. Thêm Giáo Viên Mới / Phân Công Lớp

### Cách 1: Thêm một phân công lớp

**Sử dụng script:**

```bash
cd KG_Design
python add_new_teacher.py <teacher_id> <tên_gv> <tên_lớp> [chuyên_môn]
```

**Ví dụ:**

```bash
python add_new_teacher.py tin_08 "Nguyễn Thị Mới" 7/25 "Tin học"
```

**Kết quả:**
- Phân công được thêm vào `teachers_assign.csv`
- File được backup tự động (`.csv.bak`)
- Dữ liệu được sắp xếp theo teacher_id và class

### Cách 2: Thêm nhiều phân công cho một giáo viên

**Sửa file `add_new_teacher.py`** trong hàm `main()`:

```python
# Thêm nhiều phân công
add_teacher_assignments_batch(
    teacher_id='tin_08',
    teacher_name='Nguyễn Thị Mới',
    class_names=['7/25', '7/26', '8/29'],
    expertise='Tin học'
)
```

Sau đó chạy:
```bash
python add_new_teacher.py
```

### Cách 3: Thêm từ file CSV

**Tạo file CSV** với format:

```csv
Id_teacher,name,expertise,class
tin_08,Nguyễn Thị Mới,Tin học,7/25
tin_08,Nguyễn Thị Mới,Tin học,7/26
tin_09,Trần Văn A,Tin học,8/30
```

**Chạy script:**

```bash
python add_new_teacher.py
```

Và uncomment phần code trong hàm `main()`:
```python
add_teacher_from_file('new_teachers.csv')
```

### Cách 4: Sửa trực tiếp file `teachers_assign.csv`

**Cấu trúc file:**

```csv
Id_teacher,name,expertise,class
tin_08,Nguyễn Thị Mới,Tin học,7/25
tin_08,Nguyễn Thị Mới,Tin học,7/26
```

**Lưu ý:**
- Mỗi dòng = một phân công lớp
- Nếu giáo viên dạy nhiều lớp, thêm nhiều dòng với cùng `Id_teacher`
- File phải có header: `Id_teacher,name,expertise,class`

---

## 📚 3. Thêm Lớp Mới

Lớp mới sẽ **tự động được tạo** khi bạn:

### Cách 1: Thêm học sinh vào lớp mới

```bash
python add_new_student.py 7 7/25 "Nguyễn Văn A"
```

→ Lớp `7/25` sẽ được tạo tự động trong Knowledge Graph

### Cách 2: Phân công giáo viên dạy lớp mới

```bash
python add_new_teacher.py tin_08 "Nguyễn Thị Mới" 7/25
```

→ Lớp `7/25` sẽ được tạo tự động trong Knowledge Graph

### Cách 3: Sử dụng script riêng (tùy chọn)

```bash
python add_new_class.py --by-student 7 7/25
# hoặc
python add_new_class.py --by-teacher tin_08 "Nguyễn Thị Mới" 7/25
```

---

## 🔄 4. Cập Nhật Knowledge Graph

Sau khi thêm dữ liệu mới, **bắt buộc phải** cập nhật Knowledge Graph:

### Cách nhanh nhất:

```bash
cd KG_Design
python update_kg.py
```

Script này sẽ:
- ✅ Tự động build lại Knowledge Graph từ dữ liệu mới
- ✅ Cập nhật file `kg_grade7.ttl`
- ✅ Hiển thị thống kê cập nhật

### Hoặc chạy trực tiếp:

```bash
cd KG_Design
python build_kg_grade7.py
```

---

## 📊 5. Kiểm Tra Dữ Liệu Sau Khi Thêm

### Kiểm tra giáo viên:

```bash
python test_teachers.py
```

### Chạy các truy vấn demo:

```bash
python demo_teacher_queries.py
```

### Export JSON (nếu cần cho dashboard):

```bash
python export_teachers_to_json.py
```

---

## 🔄 6. Quy Trình Hoàn Chỉnh

### Ví dụ: Thêm một lớp mới với học sinh và giáo viên

```bash
# Bước 1: Thêm giáo viên dạy lớp mới (tạo lớp)
python add_new_teacher.py tin_08 "Nguyễn Thị Mới" 7/25 "Tin học"

# Bước 2: Thêm học sinh vào lớp mới
python add_new_student.py 7 7/25 "Nguyễn Văn A"
python add_new_student.py 7 7/25 "Trần Thị B"
python add_new_student.py 7 7/25 "Lê Văn C"

# Bước 3: Cập nhật Knowledge Graph
python update_kg.py

# Bước 4: Kiểm tra dữ liệu
python test_teachers.py
python demo_teacher_queries.py
```

### Ví dụ: Thêm học sinh mới vào lớp đã có

```bash
# Bước 1: Thêm học sinh
python add_new_student.py 7 7/19 "Nguyễn Văn Mới"

# Bước 2: Cập nhật Knowledge Graph
python update_kg.py

# Bước 3: Kiểm tra
python demo_teacher_queries.py
```

### Ví dụ: Thêm phân công lớp cho giáo viên đã có

```bash
# Bước 1: Thêm phân công
python add_new_teacher.py tin_01 "Ngô Tiến Hiệp" 7/25 "Tin học"

# Bước 2: Cập nhật Knowledge Graph
python update_kg.py

# Bước 3: Kiểm tra
python test_teachers.py
```

---

## 📁 7. Cấu Trúc File Dữ Liệu

### `students.json`

```json
{
  "7": {
    "7/19": [
      {
        "name": "Nguyễn Văn A",
        "pass_hash": ""
      }
    ],
    "7/20": [...]
  },
  "6": {
    "6/14": [...]
  }
}
```

### `teachers_assign.csv`

```csv
Id_teacher,name,expertise,class
tin_01,Ngô Tiến Hiệp,Tin học,6/14
tin_01,Ngô Tiến Hiệp,Tin học,6/15
tin_02,Cô Hà,Tin học,6/5
```

---

## ⚠️ 8. Lưu Ý Quan Trọng

1. **Backup tự động**: Mỗi khi sửa file, script tự động tạo backup (`.bak`)

2. **Kiểm tra trùng lặp**: Script tự động kiểm tra và bỏ qua dữ liệu trùng

3. **Sắp xếp tự động**: Dữ liệu được sắp xếp để dễ quản lý

4. **Cập nhật KG**: **Bắt buộc** chạy `update_kg.py` sau khi thêm dữ liệu

5. **Định dạng tên lớp**: Phải đúng format `khối/lớp` (vd: `7/19`, `6/14`)

6. **Encoding**: File CSV phải dùng UTF-8 (script tự xử lý BOM)

---

## 🆘 9. Xử Lý Lỗi

### Lỗi: File không tồn tại

```
⚠️  File students.json không tồn tại!
```

**Giải pháp:** Kiểm tra đường dẫn file. Script tìm file ở thư mục cha (parent directory).

### Lỗi: Dữ liệu trùng lặp

```
⚠️  Học sinh 'Nguyễn Văn A' đã tồn tại trong lớp 7/19!
```

**Giải pháp:** Đây là cảnh báo, không phải lỗi. Script bỏ qua dữ liệu trùng.

### Lỗi: Cập nhật KG không thành công

**Giải pháp:**
1. Kiểm tra file dữ liệu (JSON/CSV) có đúng format không
2. Xem log lỗi chi tiết
3. Kiểm tra file backup (`.bak`) để khôi phục nếu cần

---

## 📞 10. Tổng Kết

### Scripts có sẵn:

- ✅ `add_new_student.py` - Thêm học sinh mới
- ✅ `add_new_teacher.py` - Thêm giáo viên/phân công lớp
- ✅ `add_new_class.py` - Thêm lớp mới (wrapper script)
- ✅ `update_kg.py` - Cập nhật Knowledge Graph
- ✅ `test_teachers.py` - Kiểm tra dữ liệu giáo viên
- ✅ `demo_teacher_queries.py` - Demo truy vấn

### Quy trình chuẩn:

1. ✅ Thêm dữ liệu (học sinh/giáo viên/lớp)
2. ✅ Cập nhật Knowledge Graph
3. ✅ Kiểm tra dữ liệu
4. ✅ Export JSON (nếu cần)

---

## 🎯 Ví Dụ Thực Tế

### Tình huống: Có lớp 7/25 mới, cần thêm 30 học sinh và phân công giáo viên

**Bước 1: Tạo file CSV cho học sinh (`new_class_7_25.csv`):**

```csv
grade,class,student_name
7,7/25,Nguyễn Văn A
7,7/25,Trần Thị B
... (30 dòng)
```

**Bước 2: Thêm học sinh từ CSV:**

Sửa `add_new_student.py`, uncomment:
```python
add_students_from_file('new_class_7_25.csv')
```

Chạy:
```bash
python add_new_student.py
```

**Bước 3: Phân công giáo viên:**

```bash
python add_new_teacher.py tin_08 "Nguyễn Thị Mới" 7/25
```

**Bước 4: Cập nhật KG:**

```bash
python update_kg.py
```

**Bước 5: Kiểm tra:**

```bash
python test_teachers.py
```

---

✅ **Hoàn thành!** Dữ liệu mới đã được thêm vào Knowledge Graph!

