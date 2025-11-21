# 📋 GIẢI THÍCH CÁC TRƯỜNG TRONG FILE CSV - KHỐI 6

Tài liệu này giải thích chi tiết từng trường trong các file CSV và nguồn dữ liệu của chúng.

---

## 1. `skills.csv` - Danh mục Kỹ năng/Chủ đề

**Mục đích**: Lưu danh sách các kỹ năng/chủ đề học tập trong Khối 6.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `skillId` | String (PK) | Mã định danh duy nhất của kỹ năng (ví dụ: `A1_Thong_tin_va_xu_li`, `K6_A1`) | **Tự động trích xuất** từ cột `topic_id` trong các file `Bai_tap_Tin_6/K6_question_*.csv` |
| `name` | String | Tên hiển thị của kỹ năng | **Tự động sinh** từ `topic_id` (thay `_` thành khoảng trắng) |
| `domain` | String | Lĩnh vực/domain (ví dụ: "Hardware", "Software", "Algorithm") | **Cần điền thủ công** hoặc để trống |
| `bloomLevel` | String | Mức độ Bloom (ví dụ: "Nhận biết", "Thông hiểu", "Vận dụng") | **Tự động lấy** từ cột `difficulty` trong file câu hỏi (nếu có) |
| `grade` | Integer | Khối lớp (luôn = 6) | **Tự động gán** = "6" |
| `description` | String | Mô tả chi tiết về kỹ năng | **Tự động sinh** từ tên file CSV nguồn (ví dụ: "Auto from K6_question_A_full.csv") |

**Cách tạo**: Chạy `python KG_Design/grade6/build_grade6_inputs.py`

**Ví dụ dữ liệu**:
```csv
skillId,name,domain,bloomLevel,grade,description
A1_Thong_tin_va_xu_li,A1 Thong tin va xu li,,Nhận biết,6,Auto from K6_question_A_full.csv
```

---

## 2. `question_skill.csv` - Ánh xạ Câu hỏi → Kỹ năng

**Mục đích**: Liên kết mỗi câu hỏi với kỹ năng mà nó đo lường.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `q_id` | String (FK) | Mã câu hỏi (ví dụ: `K6A1_01`, `K6A1_02`) | **Tự động lấy** từ cột `q_id` trong `Bai_tap_Tin_6/K6_question_*.csv` |
| `skillId` | String (FK) | Mã kỹ năng mà câu hỏi này đo lường | **Tự động lấy** từ cột `topic_id` trong cùng file câu hỏi |

**Cách tạo**: Chạy `python KG_Design/grade6/build_grade6_inputs.py` (cùng script với skills.csv)

**Ví dụ dữ liệu**:
```csv
q_id,skillId
K6A1_01,A1_Thong_tin_va_xu_li
K6A1_02,A1_Thong_tin_va_xu_li
```

---

## 3. `prerequisites.csv` - Quan hệ Tiên quyết giữa Kỹ năng

**Mục đích**: Xác định kỹ năng nào cần học trước kỹ năng nào (ví dụ: A1 → A2 → A3).

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `fromSkillId` | String (FK) | Kỹ năng tiên quyết (cần học trước) | **Cần điền thủ công** hoặc dùng script `generate_prereq_baseline.py` |
| `toSkillId` | String (FK) | Kỹ năng đích (cần học sau) | **Cần điền thủ công** hoặc dùng script `generate_prereq_baseline.py` |
| `relationType` | String | Loại quan hệ (mặc định: `PREREQUISITE_OF`) | **Tự động gán** = "PREREQUISITE_OF" |
| `note` | String | Ghi chú (tùy chọn) | **Có thể để trống** |

**Cách tạo**: 
- **Tự động (baseline)**: Chạy `python KG_Design/grade6/generate_prereq_baseline.py` (tạo quan hệ 1→2→3 trong cùng nhóm A,B,C...)
- **Thủ công**: Điền trực tiếp vào file CSV dựa trên giáo án/chương trình

**Ví dụ dữ liệu**:
```csv
fromSkillId,toSkillId,relationType,note
K6_A1,K6_A2,PREREQUISITE_OF,
A1_Thong_tin_va_xu_li,A2_May_tinh_va_phan_mem,PREREQUISITE_OF,
```

---

## 4. `resources.csv` - Danh mục Tài nguyên Học tập

**Mục đích**: Lưu danh sách tài nguyên học tập (HTML, video, PDF, bài tập...).

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `resId` | String (PK) | Mã định danh tài nguyên (ví dụ: `R_K6_A1_HTML`) | **Tự động sinh** hoặc điền thủ công |
| `title` | String | Tiêu đề tài nguyên | **Điền thủ công** hoặc tự động từ tên file |
| `mediaType` | String | Loại media: `html`, `video`, `pdf`, `quiz`, `exercise` | **Điền thủ công** |
| `url` | String | Đường dẫn đến file/tài nguyên (ví dụ: `Web/K6_A1.html`) | **Lấy từ thư mục `Web/`** trong dự án |
| `difficulty` | Integer | Độ khó (1-5, 1=dễ nhất) | **Điền thủ công** (mặc định = 1) |
| `duration` | Integer | Thời lượng ước tính (phút) | **Điền thủ công** (mặc định = 10) |
| `grade` | Integer | Khối lớp (luôn = 6) | **Tự động gán** = 6 |

**Cách tạo**: 
- **Tự động (mẫu)**: Đã có sẵn một số HTML trong file (từ thư mục `Web/K6_*.html`)
- **Thủ công**: Thêm dòng mới cho video, PDF, bài tập khác

**Ví dụ dữ liệu**:
```csv
resId,title,mediaType,url,difficulty,duration,grade
R_K6_A1_HTML,Khối 6 - A1 (HTML),html,Web/K6_A1.html,1,10,6
```

---

## 5. `resource_skill.csv` - Ánh xạ Tài nguyên → Kỹ năng

**Mục đích**: Liên kết tài nguyên với các kỹ năng mà nó phủ sóng.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `resId` | String (FK) | Mã tài nguyên | **Lấy từ `resources.csv`** |
| `skillId` | String (FK) | Mã kỹ năng mà tài nguyên này dạy | **Lấy từ `skills.csv`** |
| `coverage` | Decimal (0-1) | Mức độ phủ sóng (0.0 = không phủ, 1.0 = phủ hoàn toàn) | **Điền thủ công** (mặc định = 0.8) |

**Cách tạo**: 
- **Tự động (mẫu)**: Đã có sẵn mapping cho các HTML (ví dụ: `R_K6_A1_HTML` → `K6_A1`)
- **Thủ công**: Thêm dòng mới khi có tài nguyên mới

**Ví dụ dữ liệu**:
```csv
resId,skillId,coverage
R_K6_A1_HTML,K6_A1,0.8
R_K6_A1_HTML,A1_Thong_tin_va_xu_li,0.8
```

---

## 6. `assessments.csv` - Danh mục Bài kiểm tra/Đề thi

**Mục đích**: Lưu danh sách các bài kiểm tra, đề thi.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `assessId` | String (PK) | Mã định danh bài kiểm tra | **Cần điền thủ công** (ví dụ: `ASSESS_K6_A1_2024`) |
| `name` | String | Tên bài kiểm tra | **Cần điền thủ công** |
| `date` | Date (YYYY-MM-DD) | Ngày tổ chức | **Cần điền thủ công** |
| `grade` | Integer | Khối lớp (luôn = 6) | **Tự động gán** = 6 |
| `type` | String | Loại: `quiz`, `midterm`, `final`, `homework` | **Cần điền thủ công** |
| `maxScore` | Decimal | Điểm tối đa (ví dụ: 10.0) | **Cần điền thủ công** |

**Cách tạo**: **Điền thủ công** dựa trên lịch kiểm tra thực tế

**Ví dụ dữ liệu**:
```csv
assessId,name,date,grade,type,maxScore
ASSESS_K6_A1_2024,Kiểm tra Chủ đề A1,2024-09-15,6,quiz,10.0
```

---

## 7. `questions_in_assessment.csv` - Ánh xạ Đề thi → Câu hỏi

**Mục đích**: Liên kết các câu hỏi với bài kiểm tra/đề thi.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `assessId` | String (FK) | Mã bài kiểm tra | **Lấy từ `assessments.csv`** |
| `q_id` | String (FK) | Mã câu hỏi | **Lấy từ `question_skill.csv` hoặc `Bai_tap_Tin_6/*.csv`** |
| `weight` | Decimal (0-1) | Trọng số của câu hỏi trong đề (mặc định = 1.0) | **Cần điền thủ công** (mặc định = 1.0) |

**Cách tạo**: **Điền thủ công** khi biết cấu trúc đề thi

**Ví dụ dữ liệu**:
```csv
assessId,q_id,weight
ASSESS_K6_A1_2024,K6A1_01,1.0
ASSESS_K6_A1_2024,K6A1_02,1.0
```

---

## 8. `student_assessment.csv` - Kết quả Học sinh làm Bài kiểm tra

**Mục đích**: Lưu điểm số của học sinh trong các bài kiểm tra.

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `studentId` | String (FK) | Mã học sinh (ví dụ: `2324_0001`) | **Lấy từ `students_grade_data.json`** (cột `student_id`) |
| `assessId` | String (FK) | Mã bài kiểm tra | **Lấy từ `assessments.csv`** |
| `score` | Decimal (0-1) | Điểm số đã chuẩn hóa (0.0 = 0 điểm, 1.0 = điểm tối đa) | **Tính từ điểm thô / maxScore** (ví dụ: 7.0/10.0 = 0.7) |
| `date` | Date (YYYY-MM-DD) | Ngày làm bài | **Lấy từ `assessments.csv` hoặc điền thủ công** |

**Cách tạo**: **Điền thủ công** hoặc import từ file điểm (nếu có)

**Ví dụ dữ liệu**:
```csv
studentId,assessId,score,date
2324_0001,ASSESS_K6_A1_2024,0.7,2024-09-15
2324_0002,ASSESS_K6_A1_2024,0.9,2024-09-15
```

---

## 9. `student_mastery.csv` - Mức độ Thành thạo Kỹ năng của Học sinh

**Mục đích**: Lưu điểm thành thạo của mỗi học sinh cho từng kỹ năng (dùng để xác định học sinh yếu).

| Trường | Kiểu | Mô tả | Nguồn dữ liệu |
|--------|------|-------|---------------|
| `studentId` | String (FK) | Mã học sinh | **Tự động lấy** từ `students_grade_data.json` (cột `student_id`, lọc `year="2023-2024"` và `class` bắt đầu bằng `"6/"`) |
| `skillId` | String (FK) | Mã kỹ năng | **Tự động lấy** từ `skills.csv` |
| `score` | Decimal (0-1) | Điểm thành thạo (0.0 = yếu nhất, 1.0 = thành thạo hoàn toàn) | **Tự động tính** từ điểm cả năm (`cn`) trong `students_grade_data.json`: `score = min(max(cn / 10.0, 0.0), 1.0)` |
| `lastUpdated` | Date (YYYY-MM-DD) | Ngày cập nhật cuối | **Tự động gán** = ngày hôm nay |

**Cách tạo**: Chạy `python KG_Design/grade6/build_student_mastery.py`

**Lưu ý**: Script này tạo điểm thành thạo **đồng nhất cho tất cả kỹ năng** dựa trên điểm cả năm. Để chính xác hơn, bạn nên tính điểm riêng cho từng kỹ năng từ các bài kiểm tra cụ thể.

**Ví dụ dữ liệu**:
```csv
studentId,skillId,score,lastUpdated
2324_0001,A1_Thong_tin_va_xu_li,0.88,2025-01-15
2324_0001,K6_A1,0.88,2025-01-15
```

---

## 📊 TÓM TẮT NGUỒN DỮ LIỆU

| File CSV | Nguồn dữ liệu chính | Cách tạo |
|----------|---------------------|----------|
| `skills.csv` | `Bai_tap_Tin_6/K6_question_*.csv` → cột `topic_id` | **Tự động** (script) |
| `question_skill.csv` | `Bai_tap_Tin_6/K6_question_*.csv` → cột `q_id`, `topic_id` | **Tự động** (script) |
| `prerequisites.csv` | Giáo án/chương trình | **Thủ công** hoặc script baseline |
| `resources.csv` | Thư mục `Web/K6_*.html` | **Thủ công** (đã có mẫu) |
| `resource_skill.csv` | Mapping tài nguyên → kỹ năng | **Thủ công** (đã có mẫu) |
| `assessments.csv` | Lịch kiểm tra thực tế | **Thủ công** |
| `questions_in_assessment.csv` | Cấu trúc đề thi | **Thủ công** |
| `student_assessment.csv` | File điểm kiểm tra | **Thủ công** hoặc import |
| `student_mastery.csv` | `students_grade_data.json` → `cn` (điểm cả năm) | **Tự động** (script) |

---

## 🔄 QUY TRÌNH TẠO DỮ LIỆU ĐẦY ĐỦ

1. **Chạy script tự động**:
   ```bash
   python KG_Design/grade6/build_grade6_inputs.py          # Tạo skills.csv, question_skill.csv
   python KG_Design/grade6/generate_prereq_baseline.py    # Tạo prerequisites.csv (baseline)
   python KG_Design/grade6/build_student_mastery.py       # Tạo student_mastery.csv
   ```

2. **Điền thủ công các file còn lại**:
   - `resources.csv` (bổ sung video, PDF nếu có)
   - `resource_skill.csv` (điều chỉnh coverage nếu cần)
   - `assessments.csv` (nếu có lịch kiểm tra)
   - `questions_in_assessment.csv` (nếu có cấu trúc đề)
   - `student_assessment.csv` (nếu có điểm kiểm tra chi tiết)

3. **Xuất TTL để import vào GraphDB**:
   ```bash
   python KG_Design/grade6/export_ttl.py
   ```

---

## ⚠️ LƯU Ý QUAN TRỌNG

- **Điểm số**: Tất cả điểm trong Knowledge Graph được **chuẩn hóa về [0, 1]** (0.0 = 0 điểm, 1.0 = điểm tối đa).
- **studentId**: Phải **thống nhất** giữa tất cả file (dùng `student_id` từ `students_grade_data.json`).
- **skillId**: Phải **thống nhất** giữa `skills.csv`, `question_skill.csv`, `prerequisites.csv`, `resource_skill.csv`, `student_mastery.csv`.
- **Định dạng ngày**: Dùng `YYYY-MM-DD` (ví dụ: `2024-09-15`).

