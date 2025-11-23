@echo off
chcp 65001 >nul
echo ============================================
echo SETUP DATABASE MYSQL
echo ============================================
echo.

REM Kiểm tra MySQL có cài đặt không
where mysql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Không tìm thấy MySQL!
    echo 💡 Hãy cài đặt MySQL hoặc thêm MySQL vào PATH
    pause
    exit /b 1
)

echo ✅ Đã tìm thấy MySQL
echo.

REM Nhập thông tin MySQL
echo Nhập thông tin MySQL:
echo.
set /p MYSQL_USER="Username (mặc định: root): "
if "%MYSQL_USER%"=="" set MYSQL_USER=root

set /p MYSQL_HOST="Host (mặc định: localhost): "
if "%MYSQL_HOST%"=="" set MYSQL_HOST=localhost

echo.
echo ⚠️  Bạn sẽ được yêu cầu nhập password MySQL
echo.

REM Tạo database
echo [1/3] Đang tạo database...
mysql -h %MYSQL_HOST% -u %MYSQL_USER% -p < create_database.sql

if %ERRORLEVEL% EQU 0 (
    echo ✅ Đã tạo database thành công!
) else (
    echo ❌ Lỗi khi tạo database!
    echo 💡 Kiểm tra lại username, password và MySQL đã chạy chưa
    pause
    exit /b 1
)

echo.
echo [2/3] Đang kiểm tra database...
mysql -h %MYSQL_HOST% -u %MYSQL_USER% -p -e "USE tinhoc321_quiz; SHOW TABLES;" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Database đã được tạo đúng!
) else (
    echo ⚠️  Không thể kiểm tra database (có thể do password)
)

echo.
echo [3/3] Đang kiểm tra cấu trúc bảng...
mysql -h %MYSQL_HOST% -u %MYSQL_USER% -p -e "USE tinhoc321_quiz; DESCRIBE quiz_results;" 2>nul

echo.
echo ============================================
echo HOÀN THÀNH!
echo ============================================
echo.
echo 📋 Bước tiếp theo:
echo    1. Cập nhật api/config.php với thông tin database
echo    2. Test API: mở backend_api/test_api.php
echo    3. Test từ frontend: làm một bài và kiểm tra
echo.
pause

