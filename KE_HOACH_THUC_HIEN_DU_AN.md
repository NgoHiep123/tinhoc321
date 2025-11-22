# 📋 KẾ HOẠCH THỰC HIỆN DỰ ÁN - THỨ TỰ ƯU TIÊN

## 🎯 CÂU HỎI: THU THẬP DỮ LIỆU HAY XÂY DỰNG KNOWLEDGE GRAPH TRƯỚC?

### ✅ **TRÌNH TỰ ĐÚNG:**

```
1. THU THẬP DỮ LIỆU KẾT QUẢ TỪ WEB (TRƯỚC) ← BẮT ĐẦU TẠI ĐÂY
   └─ Lý do: Cần dữ liệu THỰC để xây dựng KG
   
2. XÂY DỰNG KNOWLEDGE GRAPH
   └─ Lý do: KG cần dữ liệu làm đầu vào
   
3. CHẠY THUẬT TOÁN KNN/PPR
   └─ Lý do: Cần KG đã có dữ liệu
   
4. TRUY VẤN VÀ PHÂN TÍCH
   └─ Lý do: Có kết quả từ KNN/PPR
```

---

## 📊 TẠI SAO PHẢI THU THẬP DỮ LIỆU TRƯỚC?

### 🔍 **Knowledge Graph cần dữ liệu gì?**

```
┌─────────────────────────────────────────────────────────┐
│  KNOWLEDGE GRAPH CẦN 5 LOẠI DỮ LIỆU:                   │
├─────────────────────────────────────────────────────────┤
│  1. ✅ Học sinh (students.json) ← ĐÃ CÓ                │
│  2. ✅ Bài học (CSV câu hỏi) ← ĐÃ CÓ                   │
│  3. ✅ Kỹ năng (skills.csv) ← ĐÃ CÓ                    │
│  4. ❌ KẾT QUẢ HỌC SINH ← CHƯA CÓ (cần thu thập)      │
│  5. ❌ ĐIỂM MASTERY ← CHƯA CÓ (tính từ kết quả)       │
└─────────────────────────────────────────────────────────┘
```

**⚠️ Không có dữ liệu kết quả → Không chạy được KNN/PPR!**

---

## 🗺️ ROADMAP CHI TIẾT (4 GIAI ĐOẠN)

### 📍 **GIAI ĐOẠN 1: THU THẬP DỮ LIỆU** (1-2 tuần) ← BẮT ĐẦU TẠI ĐÂY

#### 🎯 Mục tiêu:
Thu thập kết quả làm bài của học sinh từ website

#### ✅ Công việc:

**Tuần 1: Setup hệ thống lưu kết quả**
- [ ] Chọn giải pháp: PHP API hoặc Firebase (theo `CHON_GIAI_PHAP_NÀO.md`)
- [ ] Deploy backend (API/Firebase)
- [ ] Cập nhật tất cả file HTML
- [ ] Test với 5-10 học sinh thử nghiệm
- [ ] Sửa lỗi nếu có

**Tuần 2: Thu thập dữ liệu thực**
- [ ] Cho học sinh làm bài trên website
- [ ] Theo dõi dữ liệu vào database
- [ ] Đảm bảo có ít nhất:
  - ✅ 100 học sinh
  - ✅ 10 bài quiz
  - ✅ 500+ lượt làm bài (càng nhiều càng tốt)

#### 📊 Dữ liệu cần có:

```sql
-- Bảng quiz_results cần có ít nhất 500 dòng
SELECT COUNT(*) FROM quiz_results;  -- Mục tiêu: >= 500

-- Phân bố theo học sinh
SELECT student_name, COUNT(*) as attempts 
FROM quiz_results 
GROUP BY student_name;  -- Mỗi HS làm ít nhất 3-5 bài

-- Phân bố theo bài quiz
SELECT quiz_id, COUNT(*) as attempts 
FROM quiz_results 
GROUP BY quiz_id;  -- Mỗi bài có ít nhất 30-50 lượt
```

#### 📤 Output:
- `quiz_results.csv` hoặc database MySQL với dữ liệu đầy đủ

---

### 📍 **GIAI ĐOẠN 2: XÂY DỰNG KNOWLEDGE GRAPH** (1 tuần)

#### 🎯 Mục tiêu:
Xây dựng KG từ dữ liệu đã thu thập

#### ✅ Công việc:

**Bước 1: Chuẩn bị dữ liệu**
```bash
cd KG_Design/grade6

# 1. Export kết quả từ database/Firebase
python export_results_to_csv.py
# Output: student_assessment.csv

# 2. Tính student mastery từ kết quả
python build_student_mastery.py
# Output: student_mastery.csv

# 3. Kiểm tra dữ liệu
python validate_data.py
```

**Bước 2: Build Knowledge Graph**
```bash
# Tạo file TTL từ CSV
python export_ttl.py

# Kiểm tra các file TTL
ls out/
# → skills.ttl
# → resources.ttl
# → students.ttl
# → student_mastery.ttl
# → prerequisites.ttl
```

**Bước 3: Import vào GraphDB**
```bash
# Cách 1: GraphDB Desktop (dễ nhất)
1. Mở GraphDB Desktop
2. Create Repository: "tinhoc321_grade6"
3. Import → Chọn tất cả file .ttl trong out/
4. Import

# Cách 2: Script (tự động)
python import_to_graphdb.py
```

#### 📊 Kiểm tra KG:

```sparql
# Query 1: Đếm số entities
PREFIX edu: <http://education.vn/ontology#>

SELECT (COUNT(?s) as ?total) WHERE {
  ?s ?p ?o
}
# Kỳ vọng: >5000 triples

# Query 2: Đếm học sinh có kết quả
SELECT (COUNT(DISTINCT ?student) as ?total) WHERE {
  ?student edu:hasMastery ?mastery
}
# Kỳ vọng: >= 100 học sinh

# Query 3: Kiểm tra dữ liệu mastery
SELECT ?student ?skill ?score WHERE {
  ?student edu:fullName ?name .
  ?mastery edu:student ?student .
  ?mastery edu:skill ?skill .
  ?mastery edu:masteryScore ?score .
}
LIMIT 20
```

#### 📤 Output:
- Knowledge Graph đầy đủ trong GraphDB
- File backup: `kg_grade6_full.ttl`

---

### 📍 **GIAI ĐOẠN 3: CHẠY THUẬT TOÁN ML** (3-5 ngày)

#### 🎯 Mục tiêu:
Phát hiện học sinh yếu (KNN) và gợi ý tài nguyên (PPR)

#### ✅ Công việc:

**Bước 1: Chạy KNN**
```bash
cd ML_Algorithms

python knn_student_analysis.py

# Output:
# - weak_students.csv (danh sách HS yếu)
# - kg_with_knn.ttl (KG + kết quả KNN)
```

**Kiểm tra kết quả KNN:**
```python
import pandas as pd

df = pd.read_csv('weak_students.csv')
print(f"Số học sinh yếu: {len(df)}")
print(df.head(10))

# Ví dụ output:
#   student_name  | weak_skill        | avg_score | prediction
#   Nguyễn Văn A  | k6_b3_ket_noi_mang| 4.2       | 0.92
```

**Bước 2: Chạy PPR**
```bash
python ppr_recommendation.py

# Output:
# - recommendations.csv (gợi ý cho từng HS)
# - kg_with_ppr.ttl (KG + kết quả PPR)
```

**Kiểm tra kết quả PPR:**
```python
df = pd.read_csv('recommendations.csv')
print(df.head())

# Ví dụ output:
#   student_name  | quiz_id | resource_name           | ppr_score
#   Nguyễn Văn A  | K6_B3   | Bài học mạng có dây     | 0.0234
```

#### 📊 Đánh giá mô hình:

```python
# Đánh giá KNN
from sklearn.metrics import accuracy_score, precision_score

# Test trên 20% dữ liệu
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print(f"KNN Accuracy: {accuracy:.2%}")  # Kỳ vọng: >80%
print(f"KNN Precision: {precision:.2%}") # Kỳ vọng: >75%
```

#### 📤 Output:
- Danh sách học sinh yếu
- Danh sách gợi ý tài nguyên
- KG đầy đủ với thông tin KNN/PPR

---

### 📍 **GIAI ĐOẠN 4: TRUY VẤN & DASHBOARD** (3-5 ngày)

#### 🎯 Mục tiêu:
Tạo dashboard cho giáo viên xem kết quả

#### ✅ Công việc:

**Bước 1: Các truy vấn SPARQL quan trọng**

```sparql
# Query 1: Top học sinh yếu nhất
PREFIX edu: <http://education.vn/ontology#>

SELECT ?name ?skill ?score
WHERE {
  ?student edu:fullName ?name .
  ?student edu:weakInTopic ?skill .
  ?mastery edu:student ?student .
  ?mastery edu:skill ?skill .
  ?mastery edu:masteryScore ?score .
}
ORDER BY ?score
LIMIT 10
```

```sparql
# Query 2: Gợi ý cho một học sinh cụ thể
PREFIX edu: <http://education.vn/ontology#>

SELECT ?resource ?resourceName ?pprScore
WHERE {
  ?student edu:fullName "Nguyễn Văn A" .
  ?resource edu:recommendedFor ?student .
  ?resource rdfs:label ?resourceName .
  ?resource edu:pprScore ?pprScore .
}
ORDER BY DESC(?pprScore)
LIMIT 5
```

```sparql
# Query 3: Thống kê theo lớp
SELECT ?className (AVG(?score) as ?avgScore)
WHERE {
  ?class edu:className ?className .
  ?student edu:belongsToClass ?class .
  ?mastery edu:student ?student .
  ?mastery edu:masteryScore ?score .
}
GROUP BY ?className
ORDER BY ?avgScore
```

**Bước 2: Tạo Dashboard**

```bash
# Cập nhật Web_Teacher/dashboard.html
# Tích hợp với GraphDB API hoặc query results
```

#### 📤 Output:
- Dashboard giáo viên hoàn chỉnh
- Báo cáo học sinh yếu
- Gợi ý can thiệp

---

## 📊 TIMELINE TỔNG THỂ

```
Tuần 1-2:  THU THẬP DỮ LIỆU ← BẮT ĐẦU
           └─ Setup API/Firebase
           └─ Học sinh làm bài
           └─ Thu thập 500+ results
           
Tuần 3:    XÂY DỰNG KG
           └─ Chuẩn bị dữ liệu
           └─ Build & import KG
           └─ Validate KG
           
Tuần 4:    CHẠY ML
           └─ KNN → Phát hiện HS yếu
           └─ PPR → Gợi ý tài nguyên
           └─ Đánh giá mô hình
           
Tuần 5:    DASHBOARD & BÁO CÁO
           └─ Truy vấn SPARQL
           └─ Dashboard giáo viên
           └─ Viết báo cáo luận văn
```

**⏱️ Tổng thời gian: 4-5 tuần**

---

## ⚠️ VẤN ĐỀ QUAN TRỌNG

### 🔴 **Nếu chưa có dữ liệu kết quả:**

```
❌ KHÔNG THỂ:
   - Xây dựng KG đầy đủ (thiếu student_mastery)
   - Chạy KNN (không có dữ liệu điểm)
   - Chạy PPR (không biết HS nào yếu)
   - Tạo dashboard có ý nghĩa
   
✅ CHỈ CÓ THỂ:
   - Xây dựng KG "skeleton" (chỉ có skills, resources)
   - Viết code KNN/PPR (nhưng không test được)
   - Tạo dashboard demo (với dữ liệu giả)
```

### 🟢 **Nếu đã có dữ liệu kết quả:**

```
✅ CÓ THỂ:
   - Xây dựng KG hoàn chỉnh
   - Chạy KNN với dữ liệu thực
   - Chạy PPR với kết quả KNN thực
   - Tạo dashboard với insights thực tế
   - Viết luận văn với kết quả có ý nghĩa
```

---

## 🎯 KHUYẾN NGHỊ CỦA TÔI

### 📋 **HÀNH ĐỘNG NGAY LẬP TỨC:**

#### **Option 1: Có học sinh sẵn sàng làm bài** (Lý tưởng)

```bash
# NGÀY 1-3: Setup hệ thống
1. Chọn giải pháp lưu kết quả (PHP API recommended)
2. Deploy backend
3. Cập nhật file HTML
4. Test kỹ với 3-5 học sinh

# NGÀY 4-14: Thu thập dữ liệu
1. Cho học sinh làm bài (3-5 bài/người)
2. Theo dõi dữ liệu
3. Mục tiêu: 100 HS × 5 bài = 500 results

# SAU ĐÓ: Xây dựng KG + ML
```

#### **Option 2: Chưa có học sinh** (Dùng dữ liệu có sẵn)

```bash
# Bạn ĐÃ CÓ:
- students_grade_data.json (898 học sinh với điểm)
- result_thcs.xlsx (có vẻ là kết quả cũ)

# NGAY BÂY GIỜ:
1. Chuyển đổi dữ liệu cũ sang format mới
2. Import vào database
3. Tiếp tục với Giai đoạn 2 (Build KG)

# Script:
python scripts/convert_old_results.py
```

---

## 🔍 KIỂM TRA DỮ LIỆU CÓ SẴN

Để tôi xem bạn đã có dữ liệu gì:

```bash
# Kiểm tra file có sẵn
ls -lh students_grade_data.json
ls -lh result_thcs.xlsx

# Nếu có, đọc nội dung:
python -c "
import json
with open('students_grade_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Số học sinh: {len(data)}')
    print(f'Sample: {data[0]}')
"
```

---

## 💡 KẾ HOẠCH KẾT HỢP

### **PHƯƠNG ÁN TỐI ƯU:**

```
SONG SONG:

Track 1 (Backend):          Track 2 (KG Research):
├─ Tuần 1-2: Setup API      ├─ Nghiên cứu GraphDB
├─ Thu thập dữ liệu         ├─ Thiết kế schema
└─ Đợi đủ 500 results       ├─ Viết script build KG
                            └─ Test với dữ liệu mẫu

KẾT HỢP Tuần 3:
└─ Build KG với dữ liệu THỰC từ Track 1
```

---

## 🎯 KẾT LUẬN

### ✅ **TRÁCH NHIỆM NGAY BÂY GIỜ:**

```
1. THU THẬP DỮ LIỆU KẾT QUẢ TRƯỚC ← ƯU TIÊN SỐ 1
   
   Lý do:
   - Không có dữ liệu → KG không có giá trị
   - KNN/PPR cần dữ liệu thực để validate
   - Luận văn cần kết quả thực tế
   
2. XÂY DỰNG KG SAU
   
   Lý do:
   - Cần dữ liệu từ bước 1
   - Có thể nghiên cứu song song nhưng build sau
```

---

## 📞 BƯỚC TIẾP THEO

Bạn cho tôi biết:

1. **Bạn có học sinh sẵn sàng làm bài không?**
   - ✅ Có → Setup API ngay
   - ❌ Chưa → Dùng dữ liệu cũ (students_grade_data.json)

2. **Bạn đã có dữ liệu kết quả cũ không?**
   - Kiểm tra: `result_thcs.xlsx`
   - Nếu có → Tôi viết script chuyển đổi

3. **Bạn muốn bắt đầu từ đâu?**
   - Option A: Setup API thu thập dữ liệu mới
   - Option B: Chuyển đổi dữ liệu cũ sang KG
   - Option C: Cả hai song song

Tôi sẽ hỗ trợ chi tiết tùy theo lựa chọn của bạn! 🚀

