# 🔍 CÁC CÂU TRUY VẤN SPARQL MẪU - KHỐI 6

Tài liệu này chứa các câu truy vấn SPARQL để test và sử dụng Knowledge Graph trong GraphDB Desktop.

---

## 📋 Prefixes (Dùng chung cho tất cả truy vấn)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

---

## 1. 🔎 TRUY VẤN CƠ BẢN

### 1.1. Liệt kê tất cả kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?skill ?name ?grade WHERE {
  ?skill a edu:Skill ;
         edu:name ?name ;
         edu:grade ?grade .
}
ORDER BY ?name
```

### 1.2. Liệt kê tất cả học sinh

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?student ?studentId WHERE {
  ?student a edu:Student ;
           edu:studentId ?studentId .
}
ORDER BY ?studentId
LIMIT 20
```

### 1.3. Liệt kê tất cả tài nguyên học tập

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?resource ?title ?mediaType ?url WHERE {
  ?resource a edu:Resource ;
            edu:title ?title ;
            edu:mediaType ?mediaType ;
            edu:url ?url .
}
ORDER BY ?title
```

### 1.4. Đếm số lượng kỹ năng, học sinh, tài nguyên

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT 
  (COUNT(DISTINCT ?s) AS ?totalSkills)
  (COUNT(DISTINCT ?st) AS ?totalStudents)
  (COUNT(DISTINCT ?r) AS ?totalResources)
WHERE {
  { ?s a edu:Skill . }
  UNION
  { ?st a edu:Student . }
  UNION
  { ?r a edu:Resource . }
}
```

---

## 2. 📊 TRUY VẤN VỀ HỌC SINH YẾU

### 2.1. Tìm tất cả học sinh yếu (score < 0.5) cho một kỹ năng cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId ?skill ?skillName ?score WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  ?skill edu:name ?skillName .
  FILTER(?score < 0.5)
}
ORDER BY ?score ?studentId
LIMIT 50
```

### 2.2. Tìm học sinh yếu cho kỹ năng "Thông tin và xử lí" (A1)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId ?score WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill <https://example.org/kg/skill/A1_Thong_tin_va_xu_li> ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  FILTER(?score < 0.5)
}
ORDER BY ?score
```

### 2.3. Đếm số kỹ năng yếu của mỗi học sinh

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId (COUNT(?skill) AS ?weakSkillsCount) WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  FILTER(?score < 0.5)
}
GROUP BY ?student ?studentId
ORDER BY DESC(?weakSkillsCount)
```

### 2.4. Tìm tất cả kỹ năng yếu của một học sinh cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?skill ?skillName ?score WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?skill ;
           edu:score ?score .
  ?skill edu:name ?skillName .
  FILTER(?score < 0.5)
}
ORDER BY ?score
```

---

## 3. 📚 TRUY VẤN VỀ TÀI NGUYÊN HỌC TẬP

### 3.1. Tìm tài nguyên học tập cho một kỹ năng cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?resource ?title ?url ?coverage WHERE {
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill <https://example.org/kg/skill/A1_Thong_tin_va_xu_li> ;
         edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
}
ORDER BY DESC(?coverage)
```

### 3.2. Tìm tất cả kỹ năng được phủ bởi một tài nguyên

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?skill ?skillName ?coverage WHERE {
  ?cover a edu:Coverage ;
         edu:resource <https://example.org/kg/resource/R_K6_A1_HTML> ;
         edu:skill ?skill ;
         edu:coverage ?coverage .
  ?skill edu:name ?skillName .
}
ORDER BY DESC(?coverage)
```

---

## 4. 🎯 KHUYẾN NGHỊ TÀI NGUYÊN CHO HỌC SINH YẾU

### 4.1. Khuyến nghị tài nguyên cho học sinh yếu ở một kỹ năng cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?resource ?title ?url ?coverage ?score WHERE {
  # Tìm kỹ năng yếu của học sinh
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  
  # Tìm tài nguyên phủ kỹ năng yếu
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?weakSkill ;
        edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
}
ORDER BY DESC(?coverage) DESC(?score)
LIMIT 10
```

### 4.2. Khuyến nghị tài nguyên cho học sinh yếu (tất cả kỹ năng yếu)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?resource ?title ?url ?skillName (SUM(?coverage) AS ?totalCoverage) (COUNT(?weakSkill) AS ?skillsCovered) WHERE {
  # Tìm tất cả kỹ năng yếu của học sinh
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  ?weakSkill edu:name ?skillName .
  
  # Tìm tài nguyên phủ các kỹ năng yếu
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?weakSkill ;
        edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
}
GROUP BY ?resource ?title ?url ?skillName
ORDER BY DESC(?totalCoverage) DESC(?skillsCovered)
LIMIT 20
```

### 4.3. Khuyến nghị tài nguyên kèm kỹ năng tiên quyết

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?resource ?title ?url ?skillName ?prereqName WHERE {
  # Tìm kỹ năng yếu
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  ?weakSkill edu:name ?skillName .
  
  # Tìm kỹ năng tiên quyết
  OPTIONAL {
    ?prereq edu:prerequisiteOf ?weakSkill .
    ?prereq edu:name ?prereqName .
  }
  
  # Tìm tài nguyên phủ kỹ năng yếu hoặc tiên quyết
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?targetSkill ;
        edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
  FILTER(?targetSkill = ?weakSkill || ?targetSkill = ?prereq)
}
ORDER BY ?skillName ?prereqName
LIMIT 30
```

---

## 5. 🔗 TRUY VẤN VỀ QUAN HỆ TIÊN QUYẾT

### 5.1. Tìm tất cả quan hệ tiên quyết

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?prereq ?prereqName ?skill ?skillName WHERE {
  ?prereq edu:prerequisiteOf ?skill .
  ?prereq edu:name ?prereqName .
  ?skill edu:name ?skillName .
}
ORDER BY ?prereqName
```

### 5.2. Tìm chuỗi tiên quyết của một kỹ năng (2 bậc)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?level1 ?level1Name ?level2 ?level2Name ?target ?targetName WHERE {
  ?level1 edu:prerequisiteOf ?level2 .
  ?level2 edu:prerequisiteOf <https://example.org/kg/skill/A5_He_dieu_hanh> .
  ?level1 edu:name ?level1Name .
  ?level2 edu:name ?level2Name .
  <https://example.org/kg/skill/A5_He_dieu_hanh> edu:name ?targetName .
  BIND(<https://example.org/kg/skill/A5_He_dieu_hanh> AS ?target)
}
```

### 5.3. Tìm tất cả kỹ năng cần học trước một kỹ năng cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?prereq ?prereqName WHERE {
  ?prereq edu:prerequisiteOf <https://example.org/kg/skill/A5_He_dieu_hanh> .
  ?prereq edu:name ?prereqName .
}
```

---

## 6. 📝 TRUY VẤN VỀ CÂU HỎI VÀ ĐÁNH GIÁ

### 6.1. Tìm tất cả câu hỏi đo lường một kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?question ?qId WHERE {
  ?question a edu:Question ;
            edu:qId ?qId ;
            edu:measures <https://example.org/kg/skill/A1_Thong_tin_va_xu_li> .
}
ORDER BY ?qId
```

### 6.2. Tìm kỹ năng được đo bởi một câu hỏi

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?skill ?skillName WHERE {
  <https://example.org/kg/question/K6A1_01> edu:measures ?skill .
  ?skill edu:name ?skillName .
}
```

---

## 7. 📈 TRUY VẤN THỐNG KÊ

### 7.1. Thống kê điểm thành thạo theo kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?skill ?skillName 
       (AVG(?score) AS ?avgScore)
       (MIN(?score) AS ?minScore)
       (MAX(?score) AS ?maxScore)
       (COUNT(?student) AS ?studentCount)
WHERE {
  ?mastery a edu:Mastery ;
           edu:skill ?skill ;
           edu:score ?score ;
           edu:student ?student .
  ?skill edu:name ?skillName .
}
GROUP BY ?skill ?skillName
ORDER BY ?avgScore
```

### 7.2. Top 10 học sinh có điểm thành thạo cao nhất

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId (AVG(?score) AS ?avgMastery) WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
}
GROUP BY ?student ?studentId
ORDER BY DESC(?avgMastery)
LIMIT 10
```

### 7.3. Top 10 học sinh yếu nhất (cần hỗ trợ)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId 
       (AVG(?score) AS ?avgMastery)
       (COUNT(?weakSkill) AS ?weakSkillsCount)
WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  FILTER(?score < 0.5)
}
GROUP BY ?student ?studentId
ORDER BY ?avgMastery
LIMIT 10
```

---

## 8. 🎓 TRUY VẤN TỔNG HỢP - LỘ TRÌNH HỌC TẬP

### 8.1. Lộ trình học tập cho học sinh yếu (kỹ năng yếu + tiên quyết + tài nguyên)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?weakSkillName ?prereqName ?resourceTitle ?resourceUrl ?coverage WHERE {
  # Tìm kỹ năng yếu
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  ?weakSkill edu:name ?weakSkillName .
  
  # Tìm tiên quyết
  OPTIONAL {
    ?prereq edu:prerequisiteOf ?weakSkill .
    ?prereq edu:name ?prereqName .
  }
  
  # Tìm tài nguyên cho kỹ năng yếu hoặc tiên quyết
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?targetSkill ;
        edu:coverage ?coverage .
  ?resource edu:title ?resourceTitle ;
            edu:url ?resourceUrl .
  FILTER(?targetSkill = ?weakSkill || ?targetSkill = ?prereq)
}
ORDER BY ?weakSkillName ?prereqName DESC(?coverage)
```

---

## 💡 HƯỚNG DẪN SỬ DỤNG

1. **Mở GraphDB Desktop** → Chọn repository đã import dữ liệu
2. **Vào tab "SPARQL"** hoặc "Query"
3. **Copy một trong các câu truy vấn trên** và paste vào editor
4. **Click "Run"** hoặc nhấn `Ctrl+Enter` để thực thi
5. **Xem kết quả** trong bảng hoặc dạng đồ thị

### Lưu ý:
- Thay `<https://example.org/kg/student/2324_0008>` bằng student ID thực tế khi test
- Thay `<https://example.org/kg/skill/A1_Thong_tin_va_xu_li>` bằng skill ID thực tế
- Điều chỉnh `LIMIT` nếu muốn xem nhiều kết quả hơn
- Có thể kết hợp nhiều truy vấn để tạo báo cáo phức tạp hơn

---

## 🔧 Tùy chỉnh truy vấn

Bạn có thể thay đổi:
- **Ngưỡng điểm yếu**: Thay `0.5` trong `FILTER(?score < 0.5)` bằng giá trị khác (ví dụ: `0.6`, `0.4`)
- **Số lượng kết quả**: Thay `LIMIT 10` bằng số khác
- **Sắp xếp**: Thay `ORDER BY DESC(?score)` bằng `ORDER BY ASC(?score)` để sắp xếp tăng dần

