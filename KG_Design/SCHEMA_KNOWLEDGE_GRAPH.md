# 📊 SCHEMA KNOWLEDGE GRAPH - MÔ TẢ CHÍNH THỨC

## 🎯 TỔNG QUAN

Knowledge Graph mô hình hóa hệ thống giáo dục Tin học THCS với các thực thể và quan hệ sau:

---

## 📦 CÁC THỰC THỂ (ENTITIES/CLASSES)

### 1. **Student** (Học sinh)
- **Thuộc tính:**
  - `fullName` (string) - Họ và tên
  - `studentId` (string) - Mã học sinh (unique)
- **Quan hệ:**
  - `belongsToClass` → Class
  - `takeTest` → Test
  - `hasResult` → TestResult
  - `weakInTopic` → Topic (được xác định bởi KNN)

### 2. **Class** (Lớp học)
- **Thuộc tính:**
  - `className` (string) - Tên lớp (ví dụ: "6/14", "7/19")
- **Quan hệ:**
  - `belongsToGrade` → Grade

### 3. **Grade** (Khối lớp)
- **Thuộc tính:**
  - `grade` (integer) - Số khối (6, 7, 8, 9)
- **Quan hệ:**
  - Không có (node gốc)

### 4. **Topic** (Chủ đề)
- **Thuộc tính:**
  - `label` (string) - Tên chủ đề (ví dụ: "Chủ đề A: Máy tính và cộng đồng")
  - `topicId` (string) - Mã chủ đề (A, B, C, D, E, F)
- **Quan hệ:**
  - `forGrade` → Grade
  - Có quan hệ với Lesson (thông qua belongsToTopic)

### 5. **Lesson** (Bài học)
- **Thuộc tính:**
  - `label` (string) - Tên bài học (ví dụ: "Bài A1: Thông tin và xử lí")
  - `lessonId` (string) - Mã bài học (A1, A2, B1, ...)
- **Quan hệ:**
  - `belongsToTopic` → Topic
  - `recommendedFor` → Student (được xác định bởi PPR)

### 6. **Skill** (Kỹ năng)
- **Thuộc tính:**
  - `skillId` (string) - Mã kỹ năng (unique)
  - `name` (string) - Tên kỹ năng
  - `bloomLevel` (string) - Mức độ Bloom: "Nhận biết", "Thông hiểu", "Vận dụng"
  - `domain` (string) - Lĩnh vực
  - `grade` (integer) - Khối lớp
- **Quan hệ:**
  - `PREREQUISITE_OF` → Skill (Skill này là tiên quyết của Skill kia)
  - Có quan hệ với Resource (thông qua resource_skill)

### 7. **Question** (Câu hỏi)
- **Thuộc tính:**
  - `q_id` (string) - Mã câu hỏi (ví dụ: "K6A1_01")
  - `question_text` (string) - Nội dung câu hỏi
  - `difficulty` (string) - Độ khó: "Nhận biết", "Thông hiểu", "Vận dụng"
  - `correct_option` (string) - Đáp án đúng (A, B, C, D)
- **Quan hệ:**
  - `belongsToLesson` → Lesson (hoặc có thể belongsToSkill → Skill trong Khối 6)
  - `requiresSkill` → Skill

### 8. **Resource** (Tài nguyên học tập)
- **Thuộc tính:**
  - `resId` (string) - Mã tài nguyên (unique)
  - `title` (string) - Tiêu đề
  - `mediaType` (string) - Loại: "html", "video", "pdf"
  - `url` (string) - Đường dẫn (ví dụ: "K6_A1.html")
  - `difficulty` (integer) - Độ khó 1-5
  - `duration` (integer) - Thời lượng (phút)
- **Quan hệ:**
  - `COVERS` → Skill (với coverage 0.0-1.0)

### 9. **Test** (Bài kiểm tra)
- **Thuộc tính:**
  - `testId` (string) - Mã bài kiểm tra
  - `name` (string) - Tên bài kiểm tra
- **Quan hệ:**
  - `hasQuestion` → Question

### 10. **TestResult** (Kết quả)
- **Thuộc tính:**
  - `score` (float) - Điểm số
  - `duration` (integer) - Thời gian làm bài (giây)
  - `testDate` (dateTime) - Ngày làm bài
- **Quan hệ:**
  - `forTest` → Test

### 11. **Teacher** (Giáo viên) - Tùy chọn
- **Thuộc tính:**
  - `fullName` (string) - Họ và tên
- **Quan hệ:**
  - `teaches` → Class

---

## 🔗 QUAN HỆ CHÍNH (RELATIONSHIPS)

### Quan hệ phân cấp:
```
Grade
  └─ Class (belongsToGrade)
      └─ Student (belongsToClass)

Grade
  └─ Topic (forGrade)
      └─ Lesson (belongsToTopic)
          └─ Question (belongsToLesson)
```

### Quan hệ kỹ năng:
```
Skill ← PREREQUISITE_OF → Skill
Resource → COVERS → Skill
Question → requiresSkill → Skill
```

### Quan hệ đánh giá:
```
Student → takeTest → Test
Test → hasQuestion → Question
Student → hasResult → TestResult
TestResult → forTest → Test
```

### Quan hệ ML (Machine Learning):
```
Student → weakInTopic → Topic  (KNN phát hiện)
Lesson → recommendedFor → Student  (PPR gợi ý)
```

---

## 📊 SƠ ĐỒ QUAN HỆ TỔNG QUAN

```
                    ┌─────────┐
                    │  Grade  │
                    └────┬────┘
                         │
            ┌────────────┼────────────┐
            │                        │
      ┌─────▼─────┐          ┌───────▼──────┐
      │   Class   │          │    Topic     │
      └─────┬─────┘          └───────┬──────┘
            │                        │
      ┌─────▼─────┐          ┌───────▼──────┐
      │  Student  │          │    Lesson    │
      └─────┬─────┘          └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            │                │   Question   │
            │                └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            │                │    Skill     │
            │                └───────┬──────┘
            │                        │
            │                ┌───────▼──────┐
            └───────────────►│   Resource   │
                             └──────────────┘

         ┌─────────┐       ┌──────────┐
         │   Test  │──────►│ Question │
         └────┬────┘       └──────────┘
              │
         ┌────▼────────┐
         │  TestResult │
         └─────────────┘
```

---

## 📋 SO SÁNH VỚI CHƯƠNG TRÌNH THỰC TẾ

### **Khối 6:**
- **Chủ đề A**: Máy tính và cộng đồng (5 bài: A1-A5)
- **Chủ đề B**: Mạng máy tính và Internet (4 bài: B1-B4)
- **Chủ đề C**: Tổ chức lưu trữ, tìm kiếm thông tin (6 bài: C1-C6)
- **Chủ đề D**: Đạo đức và pháp luật (3 bài: D1-D3)
- **Chủ đề E**: Ứng dụng tin học (8 bài: E1-E8)
- **Chủ đề F**: Giải quyết vấn đề với sự trợ giúp của máy tính (5 bài: F1-F5)

**Tổng: 6 chủ đề, 31 bài học**

### **Khối 7:**
- **Chủ đề A**: Máy tính và hệ điều hành (4 bài: A1, A2, A4, A5)
- **Chủ đề B**: Soạn thảo văn bản
- **Chủ đề C**: Mạng máy tính và Internet
- **Chủ đề D**: Trình chiếu
- **Chủ đề E**: Thuật toán và lập trình
- **Chủ đề F**: Dự án

---

## ✅ KIỂM TRA SCHEMA

Để kiểm tra file hình `Knowledge_graph.png` có đúng không, hãy xem:

### **Các thực thể cần có:**
- [ ] Student (Học sinh)
- [ ] Class (Lớp)
- [ ] Grade (Khối)
- [ ] Topic (Chủ đề)
- [ ] Lesson (Bài học)
- [ ] Question (Câu hỏi)
- [ ] Skill (Kỹ năng)
- [ ] Resource (Tài nguyên)
- [ ] Test (Bài kiểm tra)
- [ ] TestResult (Kết quả)
- [ ] Teacher (Giáo viên) - Tùy chọn

### **Các quan hệ cần có:**
- [ ] Student → belongsToClass → Class
- [ ] Class → belongsToGrade → Grade
- [ ] Lesson → belongsToTopic → Topic
- [ ] Topic → forGrade → Grade
- [ ] Question → belongsToLesson → Lesson
- [ ] Question → requiresSkill → Skill
- [ ] Resource → COVERS → Skill
- [ ] Skill → PREREQUISITE_OF → Skill
- [ ] Student → takeTest → Test
- [ ] Test → hasQuestion → Question
- [ ] Student → hasResult → TestResult
- [ ] Student → weakInTopic → Topic (ML - KNN)
- [ ] Lesson → recommendedFor → Student (ML - PPR)

---

## 🎯 FILE THAM KHẢO

- **Schema chính:** `KG_Design/kg_schema_grade7.ttl`
- **Script build:** `KG_Design/build_kg_grade7.py`
- **Export Khối 6:** `KG_Design/grade6/export_ttl.py`
- **Output files:** `KG_Design/grade6/out/*.ttl`

---

**Cập nhật:** $(date)

