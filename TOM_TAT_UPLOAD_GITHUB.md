# ⚡ TÓM TẮT NHANH - UPLOAD LÊN GITHUB

> Hướng dẫn nhanh 5 phút để đưa code lên GitHub

---

## 🎯 CÁC BƯỚC CHÍNH

### 1️⃣ Tạo repository trên GitHub
- Vào: https://github.com/new
- Tên: `he-thong-ho-tro-giao-vien-thcs`
- Chọn: **Public**
- Click: **Create repository**

### 2️⃣ Mở Git Bash trong thư mục dự án
```bash
cd /d/A_De_tai_Tot_nghiep
```

### 3️⃣ Chạy các lệnh sau (thay YOUR_USERNAME):

```bash
# Khởi tạo Git
git init

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit - Hệ thống hoàn chỉnh"

# Kết nối với GitHub
git remote add origin https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git

# Đổi tên nhánh
git branch -M main

# Push lên GitHub
git push -u origin main
```

### 4️⃣ Xác thực
- Username: Nhập username GitHub
- Password: **Dán Personal Access Token** (không phải mật khẩu GitHub)

**Tạo Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Chọn quyền: `repo`
4. Generate và **SAO CHÉP TOKEN**

---

## ✅ XONG!

Kiểm tra: `https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs`

---

## 📚 XEM HƯỚNG DẪN CHI TIẾT

Xem file: `HUONG_DAN_UPLOAD_GITHUB_BANG_GIT_BASH.md`

---

## 🔄 CẬP NHẬT CODE SAU NÀY

```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

---

**Chúc bạn thành công! 🚀**

