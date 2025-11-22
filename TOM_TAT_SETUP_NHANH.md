# ⚡ TÓM TẮT SETUP NHANH - GOOGLE APPS SCRIPT

## 🎯 3 BƯỚC CHÍNH

### ✅ **BƯỚC 1: Tạo Google Sheets** (2 phút)

1. Vào https://sheets.google.com
2. Tạo mới, đặt tên: **"Kết quả trắc nghiệm THCS"**
3. Đổi sheet đầu thành: **"Results"**
4. Thêm header (dòng 1):
   ```
   Timestamp | Student Name | Class | Quiz ID | Score | Total | Percentage | Duration (s)
   ```

---

### ✅ **BƯỚC 2: Tạo Apps Script** (5 phút)

1. Trong Sheets: **Extensions** → **Apps Script**
2. Xóa code cũ, dán code từ file `HUONG_DAN_SETUP_GOOGLE_APPS_SCRIPT.md`
3. **Save** (Ctrl + S)
4. **Deploy** → **New deployment**
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone** ⚠️ QUAN TRỌNG!
5. **Authorize** → Cấp quyền
6. **Copy URL** (dạng: `https://script.google.com/macros/s/AKfycby.../exec`)

---

### ✅ **BƯỚC 3: Cập nhật file HTML** (2 phút)

#### **Cách 1: Dùng script tự động (Khuyến nghị)**

```bash
# 1. Mở file scripts/update_endpoint.py
# 2. Sửa dòng NEW_ENDPOINT = "..." (dán URL vừa copy)
# 3. Chạy script
python scripts/update_endpoint.py
```

#### **Cách 2: Thủ công**

1. Mở tất cả file `K6_*.html` và `K7_*.html`
2. Tìm dòng:
   ```javascript
   const ENDPOINT="https://script.google.com/macros/s/...";
   ```
3. Thay bằng URL mới

---

## ✅ KIỂM TRA

1. Mở `K6_B3.html` trong trình duyệt
2. Đăng nhập → Làm bài
3. Xem thông báo: **"✅ Đã lưu!"**
4. Kiểm tra Google Sheets → Sheet Results

---

## 🆘 GẶP LỖI?

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| ⚠️ Không lưu được | URL sai hoặc chưa deploy | Kiểm tra lại URL, deploy lại |
| ⚠️ Authorization error | Chưa cấp quyền | Deploy → Authorize lại |
| ⚠️ Sheet not found | Tên sheet sai | Đổi tên sheet thành "Results" |

---

## 📞 HỖ TRỢ

Xem chi tiết trong file: **`HUONG_DAN_SETUP_GOOGLE_APPS_SCRIPT.md`**

---

**⏱️ Tổng thời gian: ~10 phút**

