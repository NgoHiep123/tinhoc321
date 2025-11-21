# 📝 HƯỚNG DẪN THÊM CÂU HỎI CÓ HÌNH ẢNH

## 🎯 TỔNG QUAN

Hệ thống cho phép giáo viên dễ dàng thêm câu hỏi trắc nghiệm **có hoặc không có hình ảnh** thông qua công cụ trực quan.

---

## 🚀 CÁCH SỬ DỤNG NHANH

### Bước 1: Mở công cụ thêm câu hỏi
```
Mở file: Web/Teacher_Tools/them_cau_hoi.html
```

### Bước 2: Điền thông tin
1. ❓ **Câu hỏi**: Nhập nội dung câu hỏi
2. 🖼️ **Hình ảnh** (tùy chọn):
   - **Upload**: Chọn ảnh từ máy tính
   - **URL**: Dán link ảnh từ Internet
3. 📝 **4 đáp án**: Điền A, B, C, D
4. ✅ **Chọn đáp án đúng**: Click radio button
5. 💡 **Giải thích** (tùy chọn): Thêm giải thích

### Bước 3: Xem trước
Click nút **"👁️ Xem trước"** để kiểm tra câu hỏi hiển thị như thế nào.

### Bước 4: Tạo code
Click **"🚀 Tạo Code"** → Copy code JavaScript → Paste vào file HTML.

---

## 🖼️ CÁCH THÊM HÌNH ẢNH

### Phương pháp 1: Upload từ máy tính (Đơn giản)

#### ✅ Ưu điểm:
- Dễ dàng nhất
- Không cần upload lên server
- Ảnh đi kèm code (Base64)

#### ⚠️ Nhược điểm:
- File HTML sẽ nặng hơn
- Giới hạn 2MB/ảnh

#### 📋 Các bước:
1. Click tab **"📁 Upload"**
2. Click **"Choose File"** → Chọn ảnh (JPG/PNG/GIF)
3. Xem trước ảnh
4. Click **"Tạo Code"**

#### 💻 Code được tạo:
```javascript
{
  question: "Trong hình dưới đây, thiết bị nào là thiết bị vào?",
  image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  options: ["Màn hình", "Bàn phím", "Chuột", "Loa"],
  answer: 1
}
```

---

### Phương pháp 2: Dùng URL (Linh hoạt)

#### ✅ Ưu điểm:
- File HTML nhẹ
- Dễ thay đổi ảnh sau này
- Có thể dùng ảnh chất lượng cao

#### ⚠️ Nhược điểm:
- Cần upload ảnh lên server trước
- Phụ thuộc vào link ảnh

#### 📋 Các bước:
1. Upload ảnh lên:
   - Google Drive (public)
   - Imgur
   - GitHub
   - Server riêng
2. Copy link ảnh
3. Trong tool, click tab **"🔗 URL"**
4. Paste link vào ô
5. Click **"Tạo Code"**

#### 💻 Code được tạo:
```javascript
{
  question: "Biểu tượng nào là thư mục?",
  image: "https://i.imgur.com/abc123.png",
  options: ["Icon A", "Icon B", "Icon C", "Icon D"],
  answer: 0
}
```

---

## 📤 CÁCH UPLOAD ẢNH LÊN GOOGLE DRIVE

### Bước 1: Upload ảnh
1. Vào Google Drive
2. Upload ảnh → Right click → **"Get link"**
3. Chọn **"Anyone with the link can view"**
4. Copy link

### Bước 2: Chuyển đổi link
Link gốc (KHÔNG dùng):
```
https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing
```

Link đã chuyển (SỬ DỤNG):
```
https://drive.google.com/uc?id=1ABC123XYZ
```

**Công thức**: Lấy `FILE_ID` từ link gốc → Dán vào template:
```
https://drive.google.com/uc?id=FILE_ID
```

---

## 📤 CÁCH UPLOAD ẢNH LÊN IMGUR (ĐỀ XUẤT)

### Tại sao nên dùng Imgur?
- ✅ Miễn phí
- ✅ Không cần đăng nhập
- ✅ Link trực tiếp đến ảnh
- ✅ Không giới hạn lưu trữ

### Các bước:
1. Vào https://imgur.com
2. Click **"New post"**
3. Kéo thả ảnh
4. Right click ảnh → **"Copy image address"**
5. Paste link vào tool

---

## 💻 CÁCH ÁP DỤNG CODE VÀO FILE HTML

### Bước 1: Tìm file HTML bài học
```
Web/
├── A1.html       ← Bài A.1
├── A2.html       ← Bài A.2
├── A4.html       ← Bài A.4
└── A5.html       ← Bài A.5
```

### Bước 2: Mở file và tìm mảng quizData
```javascript
// Tìm đoạn này trong file HTML:
const quizData = [
  {question: "Câu hỏi 1...", options: [...], answer: 0},
  {question: "Câu hỏi 2...", options: [...], answer: 1},
  // ← PASTE CODE MỚI VÀO ĐÂY
];
```

### Bước 3: Paste code
```javascript
const quizData = [
  {question: "Câu hỏi 1...", options: [...], answer: 0},
  {question: "Câu hỏi 2...", options: [...], answer: 1},
  // Code mới từ tool:
  {
    question: "Trong hình dưới đây, thiết bị nào là thiết bị vào?",
    image: "https://i.imgur.com/abc123.png",
    options: ["Màn hình", "Bàn phím", "Chuột", "Loa"],
    answer: 1,
    explanation: "Bàn phím là thiết bị vào..."
  }
];
```

### Bước 4: Lưu và test
1. Lưu file HTML
2. Mở trong browser
3. Làm thử bài kiểm tra

---

## 🎨 TEMPLATE HTML HỖ TRỢ HÌNH ẢNH

### Nếu file HTML chưa hỗ trợ hiển thị ảnh:

#### Option 1: Dùng template có sẵn
Copy file `quiz_template_with_images.html` và đổi tên:
```bash
cp Web/quiz_template_with_images.html Web/A6_new.html
```

Sau đó sửa:
- Line 7: Title
- Line 35: Tên bài học
- Line XXX: Mảng quizData

#### Option 2: Thêm code vào file cũ

**Thêm CSS** (trong `<style>`):
```css
.question-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  margin: 16px auto;
  display: block;
}
```

**Thêm HTML** (sau question-card):
```html
<!-- Image (if exists) -->
<div id="image-container" class="mb-6 hidden">
  <img id="question-image" class="question-image" alt="Question illustration">
  <p class="text-center text-sm text-gray-500 mt-2">🔍 Click để phóng to</p>
</div>
```

**Thêm JavaScript** (trong hàm showQuestion):
```javascript
// Show image if exists
const imgContainer = document.getElementById('image-container');
const img = document.getElementById('question-image');
if (q.image) {
  img.src = q.image;
  imgContainer.classList.remove('hidden');
} else {
  imgContainer.classList.add('hidden');
}
```

---

## 📊 ĐỊNH DẠNG DỮ LIỆU

### Câu hỏi KHÔNG có hình ảnh:
```javascript
{
  question: "Màn hình thuộc loại thiết bị nào?",
  options: ["Vào", "Ra", "Lưu trữ", "Xử lí"],
  answer: 1
}
```

### Câu hỏi CÓ hình ảnh:
```javascript
{
  question: "Trong hình, thiết bị nào là bàn phím?",
  image: "https://i.imgur.com/abc123.png",
  options: ["A", "B", "C", "D"],
  answer: 2
}
```

### Câu hỏi CÓ giải thích:
```javascript
{
  question: "CPU là gì?",
  options: ["Bộ xử lý trung tâm", "Màn hình", "Bàn phím", "Chuột"],
  answer: 0,
  explanation: "CPU (Central Processing Unit) là bộ xử lý trung tâm, bộ não của máy tính."
}
```

### Câu hỏi ĐẦY ĐỦ (image + explanation):
```javascript
{
  question: "Biểu tượng nào biểu thị thư mục?",
  image: "https://i.imgur.com/folder-icons.png",
  options: ["📁", "📄", "🗑️", "💾"],
  answer: 0,
  explanation: "📁 là biểu tượng thư mục (folder) dùng để chứa nhiều file."
}
```

---

## 🎓 EXAMPLES

### Example 1: Câu hỏi về thiết bị máy tính (có ảnh)
```javascript
{
  question: "Thiết bị nào trong hình là thiết bị vào?",
  image: "https://i.imgur.com/computer-devices.jpg",
  options: [
    "Màn hình (Monitor)", 
    "Bàn phím (Keyboard)", 
    "Loa (Speaker)", 
    "Máy in (Printer)"
  ],
  answer: 1,
  explanation: "Bàn phím là thiết bị vào vì nó dùng để nhập dữ liệu vào máy tính."
}
```

### Example 2: Câu hỏi về icon Windows (có ảnh)
```javascript
{
  question: "Icon nào dùng để mở File Explorer trong Windows?",
  image: "https://i.imgur.com/windows-icons.png",
  options: ["Icon A", "Icon B", "Icon C", "Icon D"],
  answer: 2,
  explanation: "Icon thư mục vàng (📁) là File Explorer."
}
```

### Example 3: Câu hỏi code (có ảnh + explanation)
```javascript
{
  question: "Kết quả của đoạn code sau là gì?",
  image: "data:image/svg+xml,%3Csvg...%3E%3Ctext%3Ex = 5; y = 3; print(x + y)%3C/text%3E%3C/svg%3E",
  options: ["5", "3", "8", "53"],
  answer: 2,
  explanation: "x + y = 5 + 3 = 8. Phép + với số là phép cộng."
}
```

---

## ⚡ TIPS & TRICKS

### 1. Tối ưu kích thước ảnh
- ✅ Nên: 800x600px, dưới 200KB
- ❌ Tránh: Ảnh quá lớn (>2MB)
- 🛠️ Tool nén: TinyPNG, Squoosh

### 2. Chọn định dạng ảnh
- 📸 JPG: Ảnh chụp, ảnh có nhiều màu
- 🎨 PNG: Ảnh có nền trong suốt, icon
- 🎬 GIF: Animation (nếu cần)
- 📊 SVG: Biểu đồ, icon vector (nhẹ nhất!)

### 3. Tạo ảnh nhanh với Canva
1. Vào Canva.com
2. Chọn template "Social Media Post"
3. Thêm text/icon
4. Download → Upload lên Imgur

### 4. Tạo SVG đơn giản
```svg
<!-- File image.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
  <rect fill="#f0f0f0" width="400" height="200"/>
  <text x="200" y="100" text-anchor="middle" font-size="24">
    🖥️ Màn hình
  </text>
</svg>
```

Convert sang Data URI: https://yoksel.github.io/url-encoder/

### 5. Screenshot màn hình
- Windows: `Win + Shift + S`
- Mac: `Cmd + Shift + 4`
- Crop → Save → Upload

---

## ❓ TROUBLESHOOTING

### ❌ Ảnh không hiển thị

**Nguyên nhân 1**: Link ảnh sai
```
Kiểm tra: Mở link trong browser mới
Giải pháp: Sửa lại link hoặc upload lại
```

**Nguyên nhân 2**: File HTML chưa hỗ trợ ảnh
```
Giải pháp: Dùng quiz_template_with_images.html
Hoặc thêm code hiển thị ảnh (xem phần Template)
```

**Nguyên nhân 3**: Google Drive link chưa đúng
```
Sai: /file/d/ID/view
Đúng: /uc?id=ID
```

### ❌ Ảnh quá lớn

```
Giải pháp:
1. Nén ảnh bằng TinyPNG
2. Hoặc dùng URL thay vì upload
3. Resize về 800x600px
```

### ❌ Code không chạy

```
Kiểm tra:
1. Có dấu phẩy giữa các câu hỏi không?
2. Có thiếu dấu ngoặc } không?
3. Escape dấu " trong text: \" thay vì "
```

---

## 📚 TÀI LIỆU THAM KHẢO

### Files quan trọng:
```
Web/Teacher_Tools/
├── them_cau_hoi.html              ← Tool chính
├── HUONG_DAN_THEM_CAU_HOI.md      ← File này
└── EXAMPLES/
    ├── example_with_image.html    ← Demo câu hỏi có ảnh
    └── example_images/            ← Ảnh mẫu
```

### Links hữu ích:
- 🖼️ Imgur: https://imgur.com
- 🎨 Canva: https://canva.com
- 📦 TinyPNG: https://tinypng.com
- 🔧 SVG Encoder: https://yoksel.github.io/url-encoder/

---

## 🎉 KẾT LUẬN

Với công cụ này, giáo viên có thể:
- ✅ Thêm câu hỏi nhanh chóng (< 2 phút/câu)
- ✅ Thêm hình ảnh dễ dàng (upload hoặc URL)
- ✅ Xem trước trước khi áp dụng
- ✅ Không cần biết code chi tiết

**🚀 Bắt đầu ngay:** Mở `Web/Teacher_Tools/them_cau_hoi.html`

---

_Hướng dẫn bởi: Claude AI | Cập nhật: 11/11/2025_

