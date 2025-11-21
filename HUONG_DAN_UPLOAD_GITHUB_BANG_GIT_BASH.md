# 🚀 HƯỚNG DẪN ĐƯA CODE LÊN GITHUB BẰNG GIT BASH

> Hướng dẫn chi tiết từng bước để upload dự án lên GitHub

---

## 📋 BƯỚC 1: CHUẨN BỊ

### 1.1. Kiểm tra Git đã cài đặt chưa

Mở **Git Bash** và chạy lệnh:

```bash
git --version
```

Nếu hiển thị version (ví dụ: `git version 2.42.0`) → ✅ Đã cài đặt  
Nếu báo lỗi → Cần tải và cài Git từ: https://git-scm.com/downloads

### 1.2. Cấu hình Git (chỉ cần làm 1 lần)

```bash
# Thay YOUR_NAME và YOUR_EMAIL bằng thông tin của bạn
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"

# Kiểm tra lại
git config --global user.name
git config --global user.email
```

**Ví dụ:**
```bash
git config --global user.name "Nguyen Van A"
git config --global user.email "nguyenvana@example.com"
```

---

## 📋 BƯỚC 2: TẠO REPOSITORY TRÊN GITHUB

### 2.1. Đăng nhập GitHub

1. Truy cập: https://github.com
2. Đăng nhập vào tài khoản của bạn

### 2.2. Tạo repository mới

1. Click nút **"New"** hoặc **"+"** ở góc trên bên phải → Chọn **"New repository"**
2. Điền thông tin:
   ```
   Repository name: he-thong-ho-tro-giao-vien-thcs
   Description: Hệ thống hỗ trợ giáo viên THCS nâng cao chất lượng giảng dạy Tin học dựa trên Knowledge Graph
   
   ☑️ Public (chọn Public để có thể deploy GitHub Pages miễn phí)
   ☐ Add a README file (KHÔNG chọn - vì đã có README.md)
   ☐ Add .gitignore (KHÔNG chọn - vì đã có .gitignore)
   ☐ Choose a license (tùy chọn)
   ```
3. Click **"Create repository"**

### 2.3. Lưu URL repository

Sau khi tạo xong, GitHub sẽ hiển thị URL repository. **Lưu lại URL này!**

Ví dụ: `https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git`

---

## 📋 BƯỚC 3: KHỞI TẠO GIT TRONG THỦ MỤC DỰ ÁN

### 3.1. Mở Git Bash trong thư mục dự án

**Cách 1:** Mở Git Bash, sau đó di chuyển đến thư mục:
```bash
cd /d/A_De_tai_Tot_nghiep
```

**Cách 2:** Trong Windows Explorer:
- Mở thư mục `D:\A_De_tai_Tot_nghiep`
- Click chuột phải → Chọn **"Git Bash Here"**

### 3.2. Khởi tạo Git repository

```bash
# Khởi tạo repository
git init

# Kiểm tra trạng thái
git status
```

Bạn sẽ thấy danh sách các file chưa được thêm vào Git.

---

## 📋 BƯỚC 4: THÊM CÁC FILE VÀO GIT

### 4.1. Kiểm tra .gitignore

Đảm bảo file `.gitignore` đã có và đúng. File này sẽ loại trừ các file không cần upload (PDF, DOC, credentials, ...)

```bash
# Xem nội dung .gitignore
cat .gitignore
```

### 4.2. Thêm tất cả các file vào Git

```bash
# Thêm tất cả file (theo .gitignore)
git add .

# Kiểm tra lại những file đã được thêm
git status
```

Bạn sẽ thấy danh sách các file đã được thêm (màu xanh).

**Lưu ý:** Các file PDF, DOC, DOCX sẽ KHÔNG được thêm vào (vì đã có trong .gitignore)

---

## 📋 BƯỚC 5: COMMIT LẦN ĐẦU

```bash
# Commit với thông điệp mô tả
git commit -m "Initial commit - Hệ thống hoàn chỉnh Khối 6 và Khối 7"

# Kiểm tra lại
git log
```

Bạn sẽ thấy commit vừa tạo.

---

## 📋 BƯỚC 6: KẾT NỐI VỚI GITHUB

### 6.1. Thêm remote repository

**Thay `YOUR_USERNAME` bằng username GitHub của bạn:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git

# Kiểm tra lại
git remote -v
```

Bạn sẽ thấy:
```
origin  https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git (fetch)
origin  https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git (push)
```

### 6.2. Đổi tên nhánh thành `main` (nếu cần)

```bash
git branch -M main
```

---

## 📋 BƯỚC 7: PUSH CODE LÊN GITHUB

### 7.1. Push code lên GitHub

```bash
git push -u origin main
```

### 7.2. Xác thực

Khi chạy lệnh trên, Git sẽ yêu cầu xác thực:

**Nếu dùng Personal Access Token (khuyến nghị):**
1. Tạo Personal Access Token:
   - Vào GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Đặt tên: `git-push-token`
   - Chọn quyền: `repo` (full control)
   - Click "Generate token"
   - **SAO CHÉP TOKEN NGAY** (chỉ hiển thị 1 lần!)

2. Khi Git hỏi password:
   - Username: Nhập username GitHub của bạn
   - Password: **Dán Personal Access Token** (không phải mật khẩu GitHub)

**Nếu dùng GitHub CLI:**
```bash
# Cài GitHub CLI (nếu chưa có)
# Sau đó:
gh auth login
```

### 7.3. Kiểm tra kết quả

Sau khi push thành công, bạn sẽ thấy:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git
 * [new branch]      main -> main
Branch 'main' set up to track 'remote branch 'main' from 'origin'.
```

**✅ XONG! Code đã lên GitHub!**

---

## 📋 BƯỚC 8: KIỂM TRA TRÊN GITHUB

1. Truy cập: `https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs`
2. Kiểm tra:
   - ✅ Tất cả file đã có trên GitHub
   - ✅ README.md hiển thị đúng
   - ✅ Không có file PDF, DOC (đã bị loại bỏ bởi .gitignore)

---

## 📋 BƯỚC 9: CẬP NHẬT CODE SAU NÀY

Khi bạn sửa code và muốn cập nhật lên GitHub:

```bash
# 1. Kiểm tra thay đổi
git status

# 2. Thêm file đã sửa
git add .

# 3. Commit với thông điệp mô tả
git commit -m "Mô tả thay đổi: Ví dụ - Thêm tính năng X"

# 4. Push lên GitHub
git push
```

**Ví dụ:**
```bash
git add .
git commit -m "Fix: Sửa lỗi đăng nhập trên mobile"
git push
```

---

## 🎯 TÓM TẮT CÁC LỆNH CHÍNH

```bash
# === LẦN ĐẦU TIÊN ===
cd /d/A_De_tai_Tot_nghiep
git init
git add .
git commit -m "Initial commit - Hệ thống hoàn chỉnh"
git remote add origin https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git
git branch -M main
git push -u origin main

# === CẬP NHẬT SAU NÀY ===
git add .
git commit -m "Mô tả thay đổi"
git push
```

---

## ❓ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: "fatal: not a git repository"

**Nguyên nhân:** Chưa chạy `git init`  
**Giải pháp:**
```bash
git init
```

### Lỗi 2: "fatal: remote origin already exists"

**Nguyên nhân:** Đã thêm remote trước đó  
**Giải pháp:**
```bash
# Xóa remote cũ
git remote remove origin

# Thêm lại
git remote add origin https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs.git
```

### Lỗi 3: "Authentication failed"

**Nguyên nhân:** Sai username/password hoặc token  
**Giải pháp:**
- Kiểm tra lại username
- Tạo Personal Access Token mới và dùng token đó làm password

### Lỗi 4: "failed to push some refs"

**Nguyên nhân:** Repository trên GitHub đã có code (ví dụ: đã tạo README)  
**Giải pháp:**
```bash
# Lấy code từ GitHub về trước
git pull origin main --allow-unrelated-histories

# Sau đó push lại
git push -u origin main
```

### Lỗi 5: File PDF vẫn bị upload

**Nguyên nhân:** File đã được thêm vào Git trước khi có .gitignore  
**Giải pháp:**
```bash
# Xóa file khỏi Git (nhưng giữ lại trên máy)
git rm --cached *.pdf
git rm --cached *.docx
git rm --cached *.doc

# Commit thay đổi
git commit -m "Remove PDF and DOC files from Git"

# Push lên GitHub
git push
```

---

## 🎉 HOÀN THÀNH!

Sau khi hoàn thành các bước trên, bạn đã:
- ✅ Tạo repository trên GitHub
- ✅ Upload tất cả code lên GitHub
- ✅ Biết cách cập nhật code sau này

**Link repository của bạn:**
`https://github.com/YOUR_USERNAME/he-thong-ho-tro-giao-vien-thcs`

---

## 📚 TÀI LIỆU THAM KHẢO

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com
- Tạo Personal Access Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

---

**Chúc bạn thành công! 🚀**

