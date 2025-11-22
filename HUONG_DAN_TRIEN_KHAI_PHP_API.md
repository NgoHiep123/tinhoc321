# 🚀 HƯỚNG DẪN TRIỂN KHAI PHP API - TỪNG BƯỚC CHI TIẾT

## 📋 TỔNG QUAN

Hướng dẫn này sẽ giúp bạn triển khai giải pháp Backend API + MySQL để thay thế Google Sheets trong việc lưu kết quả trắc nghiệm.

**Kiến trúc:**
- **Frontend**: GitHub Pages (static HTML/JS)
- **Backend**: PHP + MySQL trên hosting tinhoc321.com
- **Kết nối**: AJAX/Fetch từ frontend đến backend

---

## 🎯 YÊU CẦU TRƯỚC KHI BẮT ĐẦU

### ✅ Cần có:
1. **Hosting PHP**: Có hỗ trợ PHP 7.0+ và MySQL
2. **Database**: Quyền tạo database và user MySQL
3. **FTP/Cpanel**: Quyền upload file lên hosting
4. **Domain**: tinhoc321.com (hoặc domain khác)

### ✅ Kiểm tra:
- [ ] Hosting có hỗ trợ PHP và MySQL
- [ ] Đã có thông tin đăng nhập cPanel/FTP
- [ ] Đã có thông tin MySQL (host, username, password, database name)

---

## 📝 BƯỚC 1: CHUẨN BỊ FILE

### 1.1. Kiểm tra cấu trúc file

Đảm bảo bạn đã có các file trong thư mục `backend_api/`:

```
backend_api/
├── create_database.sql          ← SQL script tạo database
├── api/
│   ├── config.php               ← File cấu hình
│   ├── save_result.php          ← API lưu kết quả
│   ├── get_results.php          ← API lấy kết quả
│   └── .htaccess                ← Bảo mật
└── dashboard/
    └── index.php                ← Dashboard giáo viên
```

### 1.2. Sửa API endpoint trong script

Mở file `scripts/update_endpoint_to_php_api.py` và sửa dòng:

```python
NEW_API_ENDPOINT = "https://tinhoc321.com/api/save_result.php"
```

Thay `tinhoc321.com` bằng domain hosting thực tế của bạn.

---

## 📤 BƯỚC 2: UPLOAD FILE LÊN HOSTING

### 2.1. Kết nối FTP/cPanel

**Cách 1: FTP (FileZilla)**
1. Mở FileZilla
2. Nhập thông tin FTP:
   - Host: ftp.tinhoc321.com (hoặc IP)
   - Username: [username FTP]
   - Password: [password FTP]
   - Port: 21
3. Kết nối

**Cách 2: cPanel File Manager**
1. Đăng nhập cPanel
2. Vào **File Manager**
3. Mở thư mục `public_html/` (hoặc `www/`)

### 2.2. Upload các file

Cấu trúc trên hosting phải như sau:

```
/home/tinhoc321/public_html/    (hoặc /public_html/)
├── api/
│   ├── config.php
│   ├── save_result.php
│   ├── get_results.php
│   └── .htaccess
└── dashboard/
    └── index.php
```

**Các bước upload:**
1. Tạo thư mục `api/` trong `public_html/`
2. Upload các file vào `api/`:
   - `config.php`
   - `save_result.php`
   - `get_results.php`
   - `.htaccess`
3. Tạo thư mục `dashboard/` trong `public_html/`
4. Upload `index.php` vào `dashboard/`

---

## 🗄️ BƯỚC 3: TẠO DATABASE

### 3.1. Tạo database trong cPanel

1. Đăng nhập cPanel
2. Vào **MySQL Databases** (hoặc **phpMyAdmin**)
3. Tạo database mới:
   - Tên database: `tinhoc321_quiz` (hoặc tên khác)
   - Nhấn **Create Database**
4. **Lưu lại tên database** (ví dụ: `user_tinhoc321_quiz`)

### 3.2. Tạo MySQL User

1. Trong **MySQL Databases**, scroll xuống phần **MySQL Users**
2. Tạo user mới:
   - Username: `tinhoc321_user` (hoặc tên khác)
   - Password: Tạo password mạnh (lưu lại!)
   - Nhấn **Create User**
3. Cấp quyền: Chọn user và database → **ALL PRIVILEGES** → **Make Changes**

### 3.3. Import SQL Script

**Cách 1: Dùng phpMyAdmin (Khuyến nghị)**

1. Vào **phpMyAdmin** trong cPanel
2. Chọn database vừa tạo (bên trái)
3. Vào tab **Import**
4. Chọn file `create_database.sql`
5. Nhấn **Go** (hoặc **Import**)
6. Kiểm tra: Bạn sẽ thấy các bảng:
   - `quiz_results`
   - `students`
   - Các view: `v_quiz_stats`, `v_student_stats`, `v_class_stats`

**Cách 2: Dùng SQL tab trong phpMyAdmin**

1. Vào phpMyAdmin
2. Chọn database
3. Vào tab **SQL**
4. Copy toàn bộ nội dung file `create_database.sql`
5. Dán vào ô SQL
6. Nhấn **Go**

---

## ⚙️ BƯỚC 4: CẤU HÌNH API

### 4.1. Sửa file config.php

Mở file `api/config.php` trên hosting (dùng File Manager → Edit hoặc download → sửa → upload lại)

**Tìm và sửa các dòng sau:**

```php
// 1. Cấu hình Database
define('DB_HOST', 'localhost');  // Thường là 'localhost', nhưng có thể khác
define('DB_NAME', 'tinhoc321_quiz');  // Tên database thực tế (vd: 'user_tinhoc321_quiz')
define('DB_USER', 'tinhoc321_user');  // Username MySQL thực tế
define('DB_PASS', 'YOUR_PASSWORD_HERE');  // Password MySQL thực tế
```

**Lưu ý:**
- `DB_HOST`: Thường là `localhost`, nhưng một số hosting dùng `127.0.0.1` hoặc tên khác
- `DB_NAME`: Đầy đủ tên database (kèm prefix user nếu có)
- `DB_USER`: Đầy đủ username (kèm prefix nếu có)
- `DB_PASS`: Password bạn đã tạo ở bước 3.2

### 4.2. Cấu hình CORS

Tìm phần `ALLOWED_ORIGINS` và thêm domain GitHub Pages của bạn:

```php
define('ALLOWED_ORIGINS', [
    'https://tinhoc321.com',
    'https://www.tinhoc321.com',
    'https://ngohiep123.github.io',  // ← Thêm domain GitHub Pages
    'https://ngohiep123.github.io/tinhoc321',  // ← Nếu có subfolder
    'http://localhost:8000',  // Cho test local
]);
```

**Lưu ý:** Thay `ngohiep123` bằng username GitHub của bạn.

### 4.3. Đổi API_SECRET

Tìm dòng:
```php
define('API_SECRET', 'CHANGE_THIS_TO_A_RANDOM_SECRET_KEY_123456789');
```

Tạo secret key ngẫu nhiên:
- Linux/Mac: `openssl rand -base64 32`
- Online: https://randomkeygen.com/
- Hoặc tự tạo một chuỗi dài và phức tạp

Thay thế bằng secret key mới.

---

## 🧪 BƯỚC 5: KIỂM TRA API

### 5.1. Test API endpoint

Mở trình duyệt và truy cập:
```
https://tinhoc321.com/api/save_result.php
```

**Kết quả mong đợi:**
- Nếu database chưa kết nối được: JSON error
- Nếu đúng: JSON response (có thể là "Method not allowed" - đây là bình thường)

### 5.2. Test bằng cURL (Terminal)

```bash
curl -X POST https://tinhoc321.com/api/save_result.php \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Test Student",
    "class_name": "Test Class",
    "quiz_id": "TEST_01",
    "score": 8,
    "total": 10,
    "duration": 300
  }'
```

**Kết quả mong đợi:**
```json
{
  "success": true,
  "message": "Đã lưu kết quả thành công",
  "data": {
    "id": 1,
    "student": "Test Student",
    "class": "Test Class",
    "quiz": "TEST_01",
    "score": "8/10",
    "percentage": "80.0%"
  }
}
```

### 5.3. Kiểm tra database

Vào phpMyAdmin → Chọn database → Bảng `quiz_results` → Xem kết quả vừa test.

---

## 📱 BƯỚC 6: CẬP NHẬT FILE HTML

### 6.1. Chạy script tự động

Mở terminal/command prompt và chạy:

```bash
cd D:\A_De_tai_Tot_nghiep
python scripts/update_endpoint_to_php_api.py
```

**Kết quả:**
- Script sẽ tìm tất cả file HTML
- Thay thế endpoint Google Sheets bằng PHP API
- Cập nhật function `sendResult()` để dùng POST thay vì GET

### 6.2. Kiểm tra file đã cập nhật

Mở một file HTML (ví dụ: `K6_A1.html`) và tìm:

**Trước khi cập nhật:**
```javascript
const ENDPOINT="https://script.google.com/macros/s/.../exec";
```

**Sau khi cập nhật:**
```javascript
const API_ENDPOINT="https://tinhoc321.com/api/save_result.php";
```

Và function `sendResult()` sẽ dùng POST:
```javascript
async function sendResult(name, className, quizId, score, total, duration) {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        student_name: name,
        class_name: className,
        quiz_id: quizId,
        score: score,
        total: total,
        duration: duration
      })
    });
    // ...
  }
}
```

### 6.3. Upload file HTML lên GitHub

1. Commit các thay đổi:
```bash
git add *.html
git commit -m "Update endpoint to PHP API"
git push origin master
```

2. Hoặc upload thủ công qua GitHub web interface

---

## 📊 BƯỚC 7: KIỂM TRA DASHBOARD

### 7.1. Truy cập Dashboard

Mở trình duyệt và truy cập:
```
https://tinhoc321.com/dashboard/
```

Bạn sẽ thấy:
- Thống kê tổng quan (tổng học sinh, lượt làm bài, điểm TB, ...)
- Bảng kết quả gần đây
- Thống kê theo lớp
- Thống kê theo bài quiz

### 7.2. Test lưu kết quả từ HTML

1. Mở một file HTML trên GitHub Pages
2. Đăng nhập → Làm bài
3. Hoàn thành bài → Xem thông báo "✅ Đã lưu!"
4. Vào Dashboard → Kiểm tra kết quả mới xuất hiện

---

## ✅ BƯỚC 8: KIỂM TRA TỔNG THỂ

### Checklist hoàn thành:

- [ ] API endpoint hoạt động (`https://tinhoc321.com/api/save_result.php`)
- [ ] Database đã có dữ liệu test
- [ ] Tất cả file HTML đã được cập nhật
- [ ] File HTML đã upload lên GitHub
- [ ] GitHub Pages hiển thị đúng
- [ ] Test lưu kết quả thành công từ frontend
- [ ] Dashboard hiển thị kết quả

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### ❌ Lỗi: "Lỗi kết nối database"

**Nguyên nhân:**
- Thông tin database trong `config.php` sai
- Database chưa được tạo
- User MySQL chưa có quyền

**Giải pháp:**
1. Kiểm tra lại thông tin trong `config.php`
2. Kiểm tra database và user trong phpMyAdmin
3. Cấp lại quyền cho user MySQL

### ❌ Lỗi: "CORS error" trong browser console

**Nguyên nhân:**
- Domain GitHub Pages chưa được thêm vào `ALLOWED_ORIGINS`

**Giải pháp:**
1. Sửa `api/config.php`
2. Thêm domain GitHub Pages vào mảng `ALLOWED_ORIGINS`

### ❌ Lỗi: "Method not allowed"

**Nguyên nhân:**
- Function `sendResult()` vẫn dùng GET thay vì POST

**Giải pháp:**
1. Chạy lại script `update_endpoint_to_php_api.py`
2. Hoặc sửa thủ công function `sendResult()` trong HTML

### ❌ Lỗi: "Quá nhiều request"

**Nguyên nhân:**
- Rate limiting đang hoạt động

**Giải pháp:**
1. Đợi 1 giờ hoặc
2. Tăng `RATE_LIMIT` trong `config.php` hoặc
3. Xóa cache trong `sys_get_temp_dir()` trên server

---

## 📚 TÀI LIỆU THAM KHẢO

- File so sánh giải pháp: `SO_SANH_GIAI_PHAP_LUU_KET_QUA.md`
- Database schema: `backend_api/create_database.sql`
- Script cập nhật: `scripts/update_endpoint_to_php_api.py`

---

## 🎉 HOÀN THÀNH!

Sau khi hoàn tất tất cả các bước, hệ thống sẽ:

✅ Lưu kết quả nhanh hơn Google Sheets 10x  
✅ Không giới hạn số lượng request  
✅ Bảo mật cao hơn  
✅ Dễ dàng tích hợp Knowledge Graph sau này  
✅ Dashboard đẹp để theo dõi kết quả  

**Chúc bạn triển khai thành công! 🚀**

