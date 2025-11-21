# ⚡ QUICK REFERENCE - TÓM TẮT NHANH

## 🎯 3 BƯỚC THÊM CÂU HỎI

```
1. Mở: Web/Teacher_Tools/them_cau_hoi.html
2. Điền form → Click "Tạo Code"
3. Copy code → Paste vào file HTML
```

---

## 🖼️ 2 CÁCH THÊM ẢNH

### Cách 1: Upload (Đơn giản)
```
📁 Upload → Chọn ảnh → Tạo Code
✅ Ưu: Dễ
❌ Nhược: File nặng, giới hạn 2MB
```

### Cách 2: URL (Linh hoạt)
```
1. Upload ảnh lên Imgur: https://imgur.com
2. Copy link ảnh
3. 🔗 URL → Paste link → Tạo Code
✅ Ưu: File nhẹ, ảnh chất lượng cao
❌ Nhược: Cần upload trước
```

---

## 📤 UPLOAD ẢNH LÊN IMGUR (ĐỀ XUẤT)

```bash
1. Vào: https://imgur.com
2. Click "New post"
3. Kéo thả ảnh
4. Right click → "Copy image address"
5. Paste vào tool
```

---

## 💻 FORMAT CODE

### Câu hỏi thường:
```javascript
{
  question: "Màn hình là thiết bị gì?",
  options: ["Vào", "Ra", "Lưu trữ", "Xử lí"],
  answer: 1
}
```

### Câu hỏi + Ảnh:
```javascript
{
  question: "Thiết bị nào là bàn phím?",
  image: "https://i.imgur.com/abc123.png",
  options: ["A", "B", "C", "D"],
  answer: 1
}
```

### Câu hỏi + Ảnh + Giải thích:
```javascript
{
  question: "Icon nào là thư mục?",
  image: "https://i.imgur.com/icons.png",
  options: ["📁", "📄", "🗑️", "💾"],
  answer: 0,
  explanation: "📁 là thư mục chứa file"
}
```

---

## 🔧 PASTE CODE VÀO FILE HTML

### Tìm đoạn này:
```javascript
const quizData = [
  {question: "...", options: [...], answer: 0},
  // ← PASTE VÀO ĐÂY (trước dấu ])
];
```

### Sau khi paste:
```javascript
const quizData = [
  {question: "Câu cũ...", options: [...], answer: 0},
  {question: "Câu mới...", image: "...", options: [...], answer: 1} // ← Câu mới
];
```

**Lưu ý**: Thêm dấu phẩy `,` sau câu trước!

---

## ✅ CHECKLIST

- [ ] Đã điền đầy đủ 4 đáp án
- [ ] Đã chọn đáp án đúng (radio button)
- [ ] Nếu có ảnh: Đã xem preview
- [ ] Đã click "Tạo Code"
- [ ] Đã copy code
- [ ] Đã paste vào đúng vị trí trong file HTML
- [ ] Đã thêm dấu phẩy `,` giữa các câu
- [ ] Đã lưu file và test

---

## 🆘 XỬ LÝ LỖI NHANH

| Lỗi | Giải pháp |
|-----|-----------|
| Ảnh không hiển thị | Kiểm tra link, mở trong tab mới |
| Code không chạy | Kiểm tra dấu `,` và `}` |
| File quá lớn | Dùng URL thay vì upload |
| Google Drive không load | Đổi `/file/d/ID/view` → `/uc?id=ID` |

---

## 📱 CONTACT

- 📧 Email: [email giáo viên]
- 💬 Zalo: [số điện thoại]
- 📁 Hướng dẫn đầy đủ: `HUONG_DAN_THEM_CAU_HOI.md`

---

**🚀 START NOW:** `Web/Teacher_Tools/them_cau_hoi.html`

