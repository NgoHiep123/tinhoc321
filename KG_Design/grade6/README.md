## Khối 6 - Hồ sơ dữ liệu để nạp vào GraphDB

Thứ tự thực hiện:
1) Sinh tự động danh mục kỹ năng và ánh xạ câu hỏi:
   - Chạy: `python KG_Design/grade6/build_grade6_inputs.py`
   - Kết quả: `skills.csv`, `question_skill.csv` (nằm cùng thư mục này).
2) Điền các file còn lại:
   - `prerequisites.csv`: quan hệ tiên quyết giữa các `skillId` khối 6.
   - `resources.csv` và `resource_skill.csv`: gắn HTML/quiz/video khối 6 vào kỹ năng.
   - (tuỳ chọn) `assessments.csv`, `questions_in_assessment.csv`, `student_assessment.csv`.
3) Xuất RDF (OntoRefine hoặc script) và import vào GraphDB.

Quy ước:
- skillId lấy từ `topic_id` trong các CSV câu hỏi K6 (Bai_tap_Tin_6/*.csv).
- score chuẩn hoá [0,1]. Dùng `studentId` thống nhất toàn dự án.

### Xuất TTL nhanh và import vào GraphDB Desktop
1. Tạo TTL:
```bash
python KG_Design/grade6/export_ttl.py
```
   - File TTL nằm ở `KG_Design/grade6/out/`:
     - `skills.ttl`, `resources.ttl`, `resource_skill.ttl`, `prerequisites.ttl`, `question_skill.ttl`
2. Trong GraphDB Desktop:
   - New repository (OWL-Horst khuyến nghị).
   - Tab Import → chọn các file TTL ở thư mục `out/` → Import.

