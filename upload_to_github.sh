#!/bin/bash
# Script hỗ trợ upload code lên GitHub
# Sử dụng: bash upload_to_github.sh

echo "🚀 BẮT ĐẦU UPLOAD CODE LÊN GITHUB"
echo "=================================="
echo ""

# Kiểm tra Git đã cài chưa
if ! command -v git &> /dev/null; then
    echo "❌ LỖI: Git chưa được cài đặt!"
    echo "Vui lòng tải và cài Git từ: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git đã được cài đặt: $(git --version)"
echo ""

# Kiểm tra đã có repository chưa
if [ -d ".git" ]; then
    echo "⚠️  Đã có Git repository trong thư mục này"
    read -p "Bạn có muốn tiếp tục? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "📦 Khởi tạo Git repository..."
    git init
fi

echo ""
echo "📝 Kiểm tra .gitignore..."
if [ ! -f ".gitignore" ]; then
    echo "⚠️  Cảnh báo: Không tìm thấy file .gitignore"
    read -p "Bạn có muốn tiếp tục? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ File .gitignore đã có"
fi

echo ""
echo "➕ Thêm các file vào Git..."
git add .

echo ""
echo "📊 Trạng thái các file:"
git status --short

echo ""
read -p "Nhập thông điệp commit (hoặc Enter để dùng mặc định): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit - Hệ thống hoàn chỉnh"
fi

echo ""
echo "💾 Commit các thay đổi..."
git commit -m "$commit_msg"

echo ""
echo "🔗 Kiểm tra remote repository..."
if git remote | grep -q "^origin$"; then
    echo "✅ Đã có remote 'origin'"
    git remote -v
    echo ""
    read -p "Bạn có muốn thay đổi remote URL? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Nhập URL repository GitHub: " repo_url
        git remote set-url origin "$repo_url"
    fi
else
    echo "❌ Chưa có remote repository"
    read -p "Nhập URL repository GitHub (ví dụ: https://github.com/USERNAME/REPO.git): " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Đã thêm remote: $repo_url"
    else
        echo "❌ LỖI: Bạn cần cung cấp URL repository"
        exit 1
    fi
fi

echo ""
echo "🌿 Đổi tên nhánh thành 'main'..."
git branch -M main

echo ""
echo "📤 Push code lên GitHub..."
echo "⚠️  LƯU Ý: Bạn sẽ cần nhập username và password (hoặc Personal Access Token)"
echo ""
read -p "Bạn đã sẵn sàng push? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 THÀNH CÔNG! Code đã được upload lên GitHub!"
        echo ""
        echo "📋 Các bước tiếp theo:"
        echo "1. Kiểm tra repository trên GitHub"
        echo "2. Xem hướng dẫn deploy GitHub Pages trong file HUONG_DAN_GITHUB.md"
        echo ""
    else
        echo ""
        echo "❌ LỖI: Push không thành công"
        echo "Vui lòng kiểm tra lại:"
        echo "- Username và password/token đúng chưa"
        echo "- URL repository đúng chưa"
        echo "- Kết nối Internet"
    fi
else
    echo "Đã hủy. Bạn có thể chạy lại script sau."
fi

echo ""
echo "✨ Hoàn thành!"

