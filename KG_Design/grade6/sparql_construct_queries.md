# 🎨 CÁC CÂU TRUY VẤN CONSTRUCT ĐỂ XEM VISUAL GRAPH - KHỐI 6

Trong GraphDB Desktop, để xem **Visual Graph**, bạn cần dùng truy vấn **CONSTRUCT** thay vì SELECT. File này chứa các truy vấn CONSTRUCT để tạo RDF graph.

---

## 📋 Prefixes

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

---

## 0. 🎯 CÂU LỆNH ĐƠN GIẢN NHẤT - XEM TẤT CẢ LỚP VÀ QUAN HỆ

### 0.1. Xem tất cả các lớp (Classes) và quan hệ (Relationships) - Đơn giản nhất

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

CONSTRUCT {
  ?s ?p ?o
}
WHERE {
  ?s ?p ?o
  FILTER(isURI(?o))
}
LIMIT 100
```

**Giải thích:**
- `?s ?p ?o`: Lấy tất cả các triple (chủ thể - thuộc tính - đối tượng)
- `FILTER(isURI(?o))`: Chỉ lấy các quan hệ với đối tượng là URI (không phải literal) để tạo graph liên kết
- `LIMIT 100`: Giới hạn 100 triple để graph không quá phức tạp khi visualize

**Cách xem:**
1. Chạy truy vấn trong GraphDB Desktop
2. Export kết quả dạng Turtle (.ttl)
3. Upload lên **WebVOWL** (http://vowl.visualdataweb.org/webvowl.html) để xem graph

---

### 0.2. Xem các lớp (Classes) và quan hệ giữa chúng - Rõ ràng hơn

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?s a ?class .
  ?s ?property ?o .
  ?o a ?oClass .
}
WHERE {
  ?s a ?class .
  ?s ?property ?o .
  FILTER(isURI(?o))
  OPTIONAL { ?o a ?oClass }
}
LIMIT 50
```

**Giải thích:**
- `?s a ?class`: Lấy loại (class) của mỗi resource
- `?s ?property ?o`: Lấy các quan hệ giữa các resource
- `?o a ?oClass`: Lấy loại của đối tượng liên quan

---

## 1. 🌳 ĐỒ THỊ HỌC SINH YẾU VÀ KỸ NĂNG

### 1.1. Tạo graph cho một học sinh và các kỹ năng yếu

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
  ?student a edu:Student ;
           edu:studentId ?studentId .
  ?skill a edu:Skill ;
         edu:name ?skillName .
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
}
WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?skill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  ?skill edu:name ?skillName .
  FILTER(?score < 0.5)
}
```

**Cách xem**: 
- Chạy truy vấn → Kết quả sẽ là RDF graph
- Trong GraphDB Desktop, sau khi chạy CONSTRUCT, bạn có thể:
  - **Export kết quả** và dùng công cụ visualization khác
  - Hoặc dùng tính năng **"Explore"** (nếu có)

---

### 1.2. Graph tất cả học sinh yếu và kỹ năng yếu

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
  ?student a edu:Student ;
           edu:studentId ?studentId .
  ?skill a edu:Skill ;
         edu:name ?skillName .
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
}
WHERE {
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?skill ;
           edu:score ?score .
  ?student edu:studentId ?studentId .
  ?skill edu:name ?skillName .
  FILTER(?score < 0.5)
}
LIMIT 50
```

---

## 2. 📚 ĐỒ THỊ TÀI NGUYÊN VÀ KỸ NĂNG

### 2.1. Graph tài nguyên và các kỹ năng mà chúng phủ

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

CONSTRUCT {
  ?resource a edu:Resource ;
            edu:title ?title ;
            edu:url ?url .
  ?skill a edu:Skill ;
         edu:name ?skillName .
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill ?skill ;
         edu:coverage ?coverage .
}
WHERE {
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill ?skill ;
         edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
  ?skill edu:name ?skillName .
}
LIMIT 30
```

---

### 2.2. Graph khuyến nghị tài nguyên cho học sinh yếu

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
  ?student a edu:Student ;
           edu:studentId ?studentId .
  ?weakSkill a edu:Skill ;
             edu:name ?weakSkillName .
  ?resource a edu:Resource ;
            edu:title ?title ;
            edu:url ?url .
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill ?weakSkill ;
         edu:coverage ?coverage .
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?weakSkill ;
           edu:score ?score .
}
WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  ?student edu:studentId ?studentId .
  ?weakSkill edu:name ?weakSkillName .
  
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?weakSkill ;
        edu:coverage ?coverage .
  ?resource edu:title ?title ;
            edu:url ?url .
}
LIMIT 50
```

---

## 3. 🔗 ĐỒ THỊ QUAN HỆ TIÊN QUYẾT

### 3.1. Graph toàn bộ quan hệ tiên quyết

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

CONSTRUCT {
  ?prereq a edu:Skill ;
          edu:name ?prereqName .
  ?skill a edu:Skill ;
        edu:name ?skillName .
  ?prereq edu:prerequisiteOf ?skill .
}
WHERE {
  ?prereq edu:prerequisiteOf ?skill .
  ?prereq edu:name ?prereqName .
  ?skill edu:name ?skillName .
}
```

---

### 3.2. Graph chuỗi tiên quyết của một kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

CONSTRUCT {
  ?level1 a edu:Skill ;
          edu:name ?name1 .
  ?level2 a edu:Skill ;
          edu:name ?name2 .
  ?target a edu:Skill ;
          edu:name ?targetName .
  ?level1 edu:prerequisiteOf ?level2 .
  ?level2 edu:prerequisiteOf ?target .
}
WHERE {
  ?level1 edu:prerequisiteOf ?level2 .
  ?level2 edu:prerequisiteOf <https://example.org/kg/skill/A5_He_dieu_hanh> .
  ?level1 edu:name ?name1 .
  ?level2 edu:name ?name2 .
  <https://example.org/kg/skill/A5_He_dieu_hanh> edu:name ?targetName .
  BIND(<https://example.org/kg/skill/A5_He_dieu_hanh> AS ?target)
}
```

---

## 4. 🎯 ĐỒ THỊ LỘ TRÌNH HỌC TẬP HOÀN CHỈNH

### 4.1. Graph đầy đủ: Học sinh → Kỹ năng yếu → Tiên quyết → Tài nguyên

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
  ?student a edu:Student ;
           edu:studentId ?studentId .
  ?weakSkill a edu:Skill ;
             edu:name ?weakSkillName .
  ?prereq a edu:Skill ;
          edu:name ?prereqName .
  ?resource a edu:Resource ;
            edu:title ?title ;
            edu:url ?url .
  ?mastery a edu:Mastery ;
           edu:student ?student ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  ?prereq edu:prerequisiteOf ?weakSkill .
  ?cover a edu:Coverage ;
         edu:resource ?resource ;
         edu:skill ?targetSkill ;
         edu:coverage ?coverage .
}
WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?weakSkill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  ?student edu:studentId ?studentId .
  ?weakSkill edu:name ?weakSkillName .
  
  OPTIONAL {
    ?prereq edu:prerequisiteOf ?weakSkill .
    ?prereq edu:name ?prereqName .
  }
  
  ?cover a edu:Coverage ;
        edu:resource ?resource ;
        edu:skill ?targetSkill ;
        edu:coverage ?coverage .
  FILTER(?targetSkill = ?weakSkill || ?targetSkill = ?prereq)
  ?resource edu:title ?title ;
            edu:url ?url .
}
LIMIT 100
```

---

## 5. 📊 ĐỒ THỊ CÂU HỎI VÀ KỸ NĂNG

### 5.1. Graph câu hỏi và kỹ năng

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

CONSTRUCT {
  ?question a edu:Question ;
            edu:qId ?qId .
  ?skill a edu:Skill ;
         edu:name ?skillName .
  ?question edu:measures ?skill .
}
WHERE {
  ?question a edu:Question ;
            edu:qId ?qId ;
            edu:measures ?skill .
  ?skill edu:name ?skillName .
}
LIMIT 50
```

---

## 💡 CÁCH XEM VISUAL GRAPH TRONG GRAPHDB DESKTOP

### Phương pháp 1: Dùng tính năng "Explore" (nếu có)

1. Chạy truy vấn CONSTRUCT
2. Click vào một **URI** trong kết quả
3. Tìm nút **"Explore"** hoặc **"Visualize"** (nếu có)
4. GraphDB sẽ hiển thị đồ thị xung quanh URI đó

### Phương pháp 2: Export và dùng công cụ khác

1. **Export kết quả CONSTRUCT**:
   - Sau khi chạy CONSTRUCT, click **"Download result"**
   - Chọn format: **Turtle (.ttl)** hoặc **RDF/XML**
   - Lưu file

2. **Dùng công cụ visualization**:
   - **yEd Graph Editor** (miễn phí): Import RDF → Visualize
   - **Gephi** (miễn phí): Import RDF → Force-directed layout
   - **WebVOWL** (online): Upload file TTL → Xem graph
   - **RDF Grapher** (online): Paste RDF → Visualize

### Phương pháp 3: Dùng SPARQL với DESCRIBE

```sparql
PREFIX ex:  <https://example.org/kg/>
PREFIX edu: <https://example.org/edu#>

DESCRIBE ?student ?skill WHERE {
  ?mastery a edu:Mastery ;
           edu:student <https://example.org/kg/student/2324_0008> ;
           edu:skill ?skill ;
           edu:score ?score .
  FILTER(?score < 0.5)
  BIND(<https://example.org/kg/student/2324_0008> AS ?student)
}
```

**DESCRIBE** sẽ trả về tất cả thông tin liên quan đến các resource, có thể dễ visualize hơn.

---

## 🌐 CÔNG CỤ ONLINE ĐỂ VISUALIZE RDF GRAPH

### 1. WebVOWL (Khuyến nghị)
- URL: http://vowl.visualdataweb.org/webvowl.html
- Cách dùng:
  1. Export kết quả CONSTRUCT dạng TTL
  2. Mở WebVOWL
  3. Click "Load" → Chọn file TTL
  4. Xem graph tương tác

### 2. RDF Grapher
- URL: https://www.ldf.fi/service/rdf-grapher
- Cách dùng:
  1. Copy kết quả CONSTRUCT (dạng Turtle)
  2. Paste vào RDF Grapher
  3. Click "Draw Graph"

### 3. LodLive
- URL: http://en.lodlive.it/
- Cách dùng:
  1. Nhập URI của một resource (ví dụ: `https://example.org/kg/student/2324_0008`)
  2. LodLive sẽ tự động crawl và hiển thị graph

---

## 📝 HƯỚNG DẪN NHANH

**Bước 1**: Chạy một trong các truy vấn CONSTRUCT ở trên

**Bước 2**: Export kết quả:
- Click **"Download result"** 
- Chọn **"Turtle"** hoặc **"RDF/XML"**

**Bước 3**: Visualize:
- **WebVOWL**: Upload file TTL → Xem graph
- **RDF Grapher**: Copy-paste nội dung TTL → Draw graph

**Hoặc** dùng DESCRIBE query và click vào các URI để explore trong GraphDB.

---

## 🎯 TRUY VẤN ĐƯỢC KHUYẾN NGHỊ

**Để bắt đầu, hãy thử:**

1. **Truy vấn 1.1**: Graph một học sinh và kỹ năng yếu (đơn giản nhất)
2. **Truy vấn 4.1**: Graph lộ trình học tập hoàn chỉnh (đầy đủ nhất)
3. **Truy vấn 3.1**: Graph quan hệ tiên quyết (rõ ràng nhất)

Sau đó export và visualize bằng WebVOWL hoặc RDF Grapher! 🎨

