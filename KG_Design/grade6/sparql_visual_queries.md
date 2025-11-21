# 🎨 CÁC CÂU TRUY VẤN SPARQL CHO VISUAL GRAPH - KHỐI 6

Tài liệu này chứa các câu truy vấn SPARQL được tối ưu để hiển thị dạng **Visual Graph** trong GraphDB Desktop.

**Lưu ý**: Trong GraphDB Desktop, chọn tab **"Graph"** hoặc **"Visualization"** sau khi chạy truy vấn để xem kết quả dạng đồ thị.

---

## 📋 Prefixes (Dùng chung)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

---

## 1. 🌳 ĐỒ THỊ HỌC SINH YẾU VÀ KỸ NĂNG YẾU

### 1.1. Hiển thị học sinh yếu và các kỹ năng yếu của họ

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?skill ?mastery ?score WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  FILTER(?score < 0.5)
}
LIMIT 50
```

**Cách xem**: Chạy truy vấn → Chọn tab **"Graph"** → GraphDB sẽ hiển thị:
- **Nút tròn**: Học sinh và Kỹ năng
- **Cạnh**: Quan hệ `edu:student` và `edu:skill` từ node Mastery

---

### 1.2. Đồ thị một học sinh cụ thể và tất cả kỹ năng (yếu + tốt)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?skill ?mastery ?score WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?skill ;
           edu:score ?score .
}
```

**Màu sắc trong GraphDB**:
- Cạnh đỏ: score < 0.5 (yếu)
- Cạnh xanh: score >= 0.5 (tốt)

---

## 2. 📚 ĐỒ THỊ TÀI NGUYÊN VÀ KỸ NĂNG

### 2.1. Hiển thị tài nguyên và các kỹ năng mà nó phủ

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?resource ?skill ?coverage WHERE {
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill ?skill ;
         edu:coverage ?coverage .
}
LIMIT 30
```

**Kết quả**: Đồ thị hiển thị:
- **Nút Resource** (hình vuông)
- **Nút Skill** (hình tròn)
- **Cạnh Coverage** với giá trị coverage

---

### 2.2. Đồ thị tài nguyên khuyến nghị cho một học sinh yếu

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?weakSkill ?resource ?coverage ?mastery ?score WHERE {
  # Tìm kỹ năng yếu
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
  
  # Giữ lại node student để hiển thị
  BIND(<https://example.org/kg/student/2324_0008> AS ?student)
}
LIMIT 50
```

**Kết quả**: Đồ thị hiển thị:
- **Học sinh** (trung tâm)
- **Kỹ năng yếu** (nối với học sinh qua Mastery)
- **Tài nguyên** (nối với kỹ năng qua Coverage)

---

## 3. 🔗 ĐỒ THỊ QUAN HỆ TIÊN QUYẾT

### 3.1. Hiển thị toàn bộ quan hệ tiên quyết giữa các kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?prereq ?skill WHERE {
  ?prereq edu:prerequisiteOf ?skill .
}
```

**Kết quả**: Đồ thị hiển thị **DAG (Directed Acyclic Graph)**:
- **Nút Skill**: Các kỹ năng
- **Cạnh có mũi tên**: Quan hệ `edu:prerequisiteOf` (từ tiên quyết → kỹ năng đích)

---

### 3.2. Đồ thị chuỗi tiên quyết của một kỹ năng (3 bậc)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?level1 ?level2 ?level3 WHERE {
  ?level1 edu:prerequisiteOf ?level2 .
  ?level2 edu:prerequisiteOf <https://example.org/kg/skill/A5_He_dieu_hanh> .
  OPTIONAL {
    ?level3 edu:prerequisiteOf ?level1 .
  }
  BIND(<https://example.org/kg/skill/A5_He_dieu_hanh> AS ?target)
}
```

**Kết quả**: Đồ thị hiển thị chuỗi tiên quyết dạng cây:
```
level3 → level1 → level2 → A5_He_dieu_hanh
```

---

## 4. 🎯 ĐỒ THỊ KHUYẾN NGHỊ HOÀN CHỈNH

### 4.1. Đồ thị lộ trình học tập cho học sinh yếu (kỹ năng yếu + tiên quyết + tài nguyên)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?weakSkill ?prereq ?resource ?mastery ?coverage WHERE {
  # Học sinh yếu
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  
  # Kỹ năng tiên quyết
  OPTIONAL {
    ?prereq edu:prerequisiteOf ?weakSkill .
  }
  
  # Tài nguyên cho kỹ năng yếu hoặc tiên quyết
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?targetSkill .
  FILTER(?targetSkill = ?weakSkill || ?targetSkill = ?prereq)
  
  BIND(<https://example.org/kg/student/2324_0008> AS ?student)
}
LIMIT 100
```

**Kết quả**: Đồ thị hiển thị mạng lưới:
- **Học sinh** (trung tâm, màu đỏ nếu yếu)
- **Kỹ năng yếu** (nối với học sinh)
- **Kỹ năng tiên quyết** (nối với kỹ năng yếu)
- **Tài nguyên** (nối với cả kỹ năng yếu và tiên quyết)

---

### 4.2. Đồ thị khuyến nghị tài nguyên cho top 5 học sinh yếu nhất

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?studentId ?weakSkill ?resource ?coverage ?score WHERE {
  {
    # Tìm top 5 học sinh yếu nhất
    SELECT ?student ?studentId (AVG(?s) AS ?avgScore) WHERE {
      ?m a edu:Mastery ;
         edu:student ?student ;
         edu:score ?s .
      ?student edu:studentId ?studentId .
      FILTER(?s < 0.5)
    }
    GROUP BY ?student ?studentId
    ORDER BY ?avgScore
    LIMIT 5
  }
  
  # Tìm kỹ năng yếu của các học sinh này
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  
  # Tìm tài nguyên
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?weakSkill ;
        edu:coverage ?coverage .
}
LIMIT 100
```

---

## 5. 📊 ĐỒ THỊ CÂU HỎI VÀ KỸ NĂNG

### 5.1. Hiển thị câu hỏi và kỹ năng mà chúng đo lường

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?question ?skill WHERE {
  ?question a edu:Question ;
            edu:measures ?skill .
}
LIMIT 50
```

**Kết quả**: Đồ thị hiển thị:
- **Nút Question** (hình thoi)
- **Nút Skill** (hình tròn)
- **Cạnh**: `edu:measures`

---

### 5.2. Đồ thị câu hỏi cho một kỹ năng cụ thể

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?question ?skill ?qId WHERE {
  ?question a edu:Question ;
            edu:qId ?qId ;
            edu:measures <https://example.org/kg/skill/A1_Thong_tin_va_xu_li> .
  BIND(<https://example.org/kg/skill/A1_Thong_tin_va_xu_li> AS ?skill)
}
```

---

## 6. 🌐 ĐỒ THỊ TỔNG QUAN TOÀN BỘ KNOWLEDGE GRAPH

### 6.1. Đồ thị tổng quan (tất cả entities và relationships)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?s ?p ?o WHERE {
  {
    # Tất cả Skills
    ?s a edu:Skill .
  }
  UNION
  {
    # Tất cả Students
    ?s a edu:Student .
  }
  UNION
  {
    # Tất cả Resources
    ?s a edu:Resource .
  }
  UNION
  {
    # Tất cả Mastery relationships
    ?s a edu:Mastery .
    ?s ?p ?o .
  }
  UNION
  {
    # Tất cả Coverage relationships
    ?s a edu:Coverage .
    ?s ?p ?o .
  }
  UNION
  {
    # Tất cả Prerequisite relationships
    ?s edu:prerequisiteOf ?o .
  }
  UNION
  {
    # Tất cả Question-Skill relationships
    ?s a edu:Question .
    ?s edu:measures ?o .
  }
}
LIMIT 200
```

**⚠️ Lưu ý**: Truy vấn này có thể trả về nhiều kết quả. Giảm `LIMIT` nếu đồ thị quá phức tạp.

---

### 6.2. Đồ thị tập trung vào một học sinh (tất cả quan hệ)

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?student ?skill ?resource ?prereq ?mastery ?coverage ?prereqRel WHERE {
  # Học sinh
  BIND(<https://example.org/kg/student/2324_0008> AS ?student)
  
  # Kỹ năng của học sinh
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill .
  
  # Tài nguyên cho các kỹ năng
  OPTIONAL {
    ?coverage a edu:Coverage ;
              edu:resource ?resource ;
              edu:skill ?skill .
  }
  
  # Tiên quyết của các kỹ năng
  OPTIONAL {
    ?prereq edu:prerequisiteOf ?skill .
  }
  
  # Quan hệ tiên quyết (để hiển thị cạnh)
  OPTIONAL {
    ?prereqRel edu:prerequisiteOf ?skill .
  }
}
LIMIT 150
```

---

## 7. 🎨 ĐỒ THỊ THEO CHỦ ĐỀ (A, B, C, D, E, F)

### 7.1. Đồ thị tất cả kỹ năng và quan hệ trong Chủ đề A

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

SELECT ?skill1 ?skill2 ?prereq WHERE {
  {
    # Tất cả skills bắt đầu bằng "A"
    ?skill1 a edu:Skill ;
            edu:skillId ?id1 .
    FILTER(STRSTARTS(?id1, "A"))
  }
  UNION
  {
    # Quan hệ tiên quyết giữa các skills A
    ?skill1 edu:prerequisiteOf ?skill2 .
    ?skill1 edu:skillId ?id1 .
    ?skill2 edu:skillId ?id2 .
    FILTER(STRSTARTS(?id1, "A") && STRSTARTS(?id2, "A"))
    BIND(?skill1 AS ?prereq)
  }
}
```

---

## 💡 HƯỚNG DẪN SỬ DỤNG VISUAL GRAPH TRONG GRAPHDB

### Cách xem đồ thị:

1. **Mở GraphDB Desktop** → Chọn repository
2. **Vào tab "SPARQL"** hoặc **"Query"**
3. **Copy một câu truy vấn** từ file này
4. **Paste và chạy** (Ctrl+Enter)
5. **Chọn tab "Graph"** hoặc **"Visualization"** để xem đồ thị

### Tùy chỉnh hiển thị:

- **Zoom**: Scroll chuột hoặc dùng thanh zoom
- **Di chuyển**: Click và kéo nút để di chuyển
- **Xem chi tiết**: Click vào nút để xem properties
- **Màu sắc**: GraphDB tự động phân màu theo loại entity
- **Layout**: Chọn layout khác nhau (Force-directed, Hierarchical, v.v.)

### Mẹo tối ưu:

- **Giảm LIMIT** nếu đồ thị quá phức tạp (ví dụ: LIMIT 30 thay vì 100)
- **Tập trung vào một học sinh/kỹ năng** để đồ thị rõ ràng hơn
- **Dùng truy vấn 4.1** để xem lộ trình học tập đầy đủ nhất

---

## 🎯 TRUY VẤN ĐƯỢC KHUYẾN NGHỊ

**Để bắt đầu, hãy thử:**

1. **Truy vấn 1.2**: Xem một học sinh và tất cả kỹ năng
2. **Truy vấn 4.1**: Xem lộ trình học tập hoàn chỉnh
3. **Truy vấn 3.1**: Xem quan hệ tiên quyết giữa các kỹ năng

Những truy vấn này cho đồ thị rõ ràng và dễ hiểu nhất! 🎨

