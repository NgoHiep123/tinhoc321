# ⚡ SETUP NHANH DATABASE

> Hướng dẫn setup database trong 5 phút

---

## 🚀 CÁCH NHANH NHẤT

### Windows:
```bash
cd backend_api
setup_database.bat
```

### Linux/Mac:
```bash
cd backend_api
chmod +x setup_database.sh
./setup_database.sh
```

---

## 📋 HOẶC SETUP THỦ CÔNG

### Bước 1: Tạo database (1 phút)
```bash
mysql -u root -p < backend_api/create_database.sql
```

### Bước 2: Cấu hình (1 phút)
Sửa `backend_api/api/config.php`:
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'root');  // Hoặc user riêng
define('DB_PASS', 'your_password');  // ⚠️ Thay password
```

### Bước 3: Test (1 phút)
Mở trong browser: `backend_api/test_connection.php`

---

## ✅ KIỂM TRA

Nếu thấy:
- ✅ "Kết nối database thành công!"
- ✅ Các bảng đã được tạo
- ✅ Test INSERT thành công

**→ Database đã setup xong!**

---

## 📞 GẶP VẤN ĐỀ?

Xem: `HUONG_DAN_SETUP_DATABASE_CHI_TIET.md`

