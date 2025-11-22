# 🔧 Backend API - Lưu kết quả trắc nghiệm

## 📁 Cấu trúc thư mục

```
backend_api/
├── create_database.sql    ← SQL script tạo database
├── api/
│   ├── config.php         ← Cấu hình database & CORS
│   ├── save_result.php    ← API endpoint lưu kết quả
│   ├── get_results.php    ← API endpoint lấy kết quả
│   └── .htaccess          ← Bảo mật
└── dashboard/
    └── index.php          ← Dashboard giáo viên
```

## 🚀 Hướng dẫn nhanh

### 1. Upload lên hosting

Upload các file vào:
```
/public_html/
├── api/          ← Upload thư mục api/
└── dashboard/    ← Upload thư mục dashboard/
```

### 2. Tạo database

1. Vào phpMyAdmin
2. Import file `create_database.sql`
3. Tạo MySQL user và cấp quyền

### 3. Cấu hình

Sửa file `api/config.php`:
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`
- `ALLOWED_ORIGINS` (thêm domain GitHub Pages)
- `API_SECRET` (tạo key ngẫu nhiên)

### 4. Test

- API: `https://yourdomain.com/api/save_result.php`
- Dashboard: `https://yourdomain.com/dashboard/`

## 📖 Hướng dẫn chi tiết

Xem file: **`../HUONG_DAN_TRIEN_KHAI_PHP_API.md`**

## 🔗 Liên kết

- File so sánh giải pháp: `../SO_SANH_GIAI_PHAP_LUU_KET_QUA.md`
- Script cập nhật HTML: `../scripts/update_endpoint_to_php_api.py`

