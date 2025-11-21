## Quy trình từng bước để chuẩn bị dữ liệu và import GraphDB

1) Chuẩn bị môi trường
- Cài Neo4j Desktop hoặc Neo4j + GDS. Xem `HUONG_DAN_GRAPHDB.md`.
- Python 3.10+ và các thư viện trong `requirements.txt`.

2) Sinh danh mục kỹ năng và ánh xạ câu hỏi → kỹ năng
- Chạy script:
```bash
python KG_Design/build_inputs_from_existing.py
```
- Kết quả sinh ra trong `KG_Design/generated/`:
  - `skills.csv`: danh mục `skillId` lấy từ `topic_id`.
  - `question_skill.csv`: ánh xạ `q_id` → `skillId`.

3) Hoàn thiện các file dữ liệu còn thiếu (templates)
- Mở thư mục `KG_Design/data_templates/` và điền dữ liệu thật:
  - `prerequisites.csv`: quan hệ tiền đề giữa các `skillId`.
  - `resources.csv`, `resource_skill.csv`: tài nguyên học và mức bao phủ kỹ năng.
  - (tuỳ chọn) `assessments.csv`, `questions_in_assessment.csv`, `student_assessment.csv`.
  - (tuỳ chọn) `classes.csv`, `enrollments.csv`, `teachers.csv`.
- Quy ước:
  - `score` chuẩn hoá vào [0,1].
  - Dùng cùng `studentId` như trong `students_grade_data.json`.

4) Import vào Neo4j (phác thảo Cypher)
```cypher
// Constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Student) REQUIRE s.studentId IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (k:Skill)   REQUIRE k.skillId   IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:Resource) REQUIRE r.resId     IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (a:Assessment) REQUIRE a.assessId IS UNIQUE;

// Nodes
LOAD CSV WITH HEADERS FROM 'file:///skills.csv' AS row
MERGE (k:Skill {skillId: row.skillId})
SET   k.name = row.name, k.domain = row.domain, k.bloomLevel = row.bloomLevel, k.grade = toInteger(row.grade), k.description = row.description;

LOAD CSV WITH HEADERS FROM 'file:///resources.csv' AS row
MERGE (r:Resource {resId: row.resId})
SET   r.title = row.title, r.mediaType = row.mediaType, r.url = row.url, r.difficulty = toInteger(row.difficulty), r.duration = toInteger(row.duration), r.grade = toInteger(row.grade);

// Relationships
LOAD CSV WITH HEADERS FROM 'file:///resource_skill.csv' AS row
MATCH (r:Resource {resId: row.resId}), (k:Skill {skillId: row.skillId})
MERGE (r)-[c:COVERS]->(k)
SET c.coverage = toFloat(row.coverage);

LOAD CSV WITH HEADERS FROM 'file:///prerequisites.csv' AS row
MATCH (p:Skill {skillId: row.fromSkillId}), (q:Skill {skillId: row.toSkillId})
MERGE (p)-[:PREREQUISITE_OF]->(q);
```

5) Tạo projection GDS để xếp hạng khuyến nghị
```cypher
CALL gds.graph.project(
  'skill_resource_graph',
  ['Skill','Resource'],
  {
    COVERS: {orientation: 'UNDIRECTED'},
    PREREQUISITE_OF: {orientation: 'NATURAL'}
  }
);
```

6) Truy vấn khuyến nghị cho học sinh yếu
```cypher
// Ví dụ: tìm các skill yếu (score < 0.5) rồi PageRank cá nhân hoá trên đồ thị skill-resource
MATCH (s:Student {studentId: $studentId})- [m:MASTERY]->(k:Skill)
WHERE m.score < 0.5
WITH collect(k) AS weakSkills
CALL gds.pageRank.stream('skill_resource_graph', {sourceNodes: weakSkills, maxIterations: 20, dampingFactor: 0.85})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS n, score
WHERE n:Resource
RETURN n AS resource, score
ORDER BY score DESC LIMIT 10;
```

7) Kiểm thử nhanh
- Sau khi import, chạy truy vấn Cypher ở bước 6 với một `studentId` thật.
- Nếu chưa có cạnh `MASTERY`, có thể tạm tạo từ `students_grade_data.json` với quy tắc: `score = cn/10`.

8) Lộ trình hoàn thiện
- Bổ sung `prerequisites.csv` theo chương trình học.
- Liên tục mở rộng `resources.csv` và độ phủ `resource_skill.csv`.
- Nâng cấp sang đánh giá theo từng `Assessment`/`Question` khi sẵn sàng.

