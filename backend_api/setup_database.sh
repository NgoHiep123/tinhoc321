#!/bin/bash
# Script setup database MySQL cho Linux/Mac

echo "============================================"
echo "SETUP DATABASE MYSQL"
echo "============================================"
echo

# Kiểm tra MySQL có cài đặt không
if ! command -v mysql &> /dev/null; then
    echo "❌ Không tìm thấy MySQL!"
    echo "💡 Hãy cài đặt MySQL: sudo apt-get install mysql-client (Ubuntu) hoặc brew install mysql (Mac)"
    exit 1
fi

echo "✅ Đã tìm thấy MySQL"
echo

# Nhập thông tin MySQL
read -p "Username (mặc định: root): " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-root}

read -p "Host (mặc định: localhost): " MYSQL_HOST
MYSQL_HOST=${MYSQL_HOST:-localhost}

echo
echo "⚠️  Bạn sẽ được yêu cầu nhập password MySQL"
echo

# Tạo database
echo "[1/3] Đang tạo database..."
mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p < create_database.sql

if [ $? -eq 0 ]; then
    echo "✅ Đã tạo database thành công!"
else
    echo "❌ Lỗi khi tạo database!"
    echo "💡 Kiểm tra lại username, password và MySQL đã chạy chưa"
    exit 1
fi

echo
echo "[2/3] Đang kiểm tra database..."
mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p -e "USE tinhoc321_quiz; SHOW TABLES;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database đã được tạo đúng!"
else
    echo "⚠️  Không thể kiểm tra database (có thể do password)"
fi

echo
echo "[3/3] Đang kiểm tra cấu trúc bảng..."
mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p -e "USE tinhoc321_quiz; DESCRIBE quiz_results;" 2>/dev/null

echo
echo "============================================"
echo "HOÀN THÀNH!"
echo "============================================"
echo
echo "📋 Bước tiếp theo:"
echo "   1. Cập nhật api/config.php với thông tin database"
echo "   2. Test API: mở backend_api/test_api.php"
echo "   3. Test từ frontend: làm một bài và kiểm tra"
echo

