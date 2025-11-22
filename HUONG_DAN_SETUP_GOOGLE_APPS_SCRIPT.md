# 📊 HƯỚNG DẪN THIẾT LẬP GOOGLE APPS SCRIPT ĐỂ LƯU KẾT QUẢ HỌC SINH

## 🎯 MỤC ĐÍCH
Thiết lập hệ thống tự động lưu kết quả trắc nghiệm của học sinh từ các file HTML vào Google Sheets.

---

## 📋 BƯỚC 1: TẠO GOOGLE SHEETS

### 1.1. Tạo Spreadsheet mới

1. Truy cập: https://sheets.google.com
2. Tạo Spreadsheet mới với tên: **`Kết quả trắc nghiệm THCS`**
3. Đổi tên Sheet đầu tiên thành: **`Results`**

### 1.2. Tạo cấu trúc bảng

Thêm **header** (dòng đầu tiên) với các cột:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **Timestamp** | **Student Name** | **Class** | **Quiz ID** | **Score** | **Total** | **Percentage** | **Duration (s)** |

**Ví dụ dữ liệu:**
```
2024-11-21 10:30:00 | Nguyễn Văn A | 6/1 | K6_B3 | 8 | 10 | 80% | 450
2024-11-21 10:35:00 | Trần Thị B   | 6/2 | K6_A1 | 9 | 9  | 100% | 380
```

---

## 📝 BƯỚC 2: TẠO GOOGLE APPS SCRIPT

### 2.1. Mở Script Editor

1. Trong Google Sheets, click **Extensions** → **Apps Script**
2. Xóa code mặc định
3. Dán đoạn code sau:

```javascript
// =============================================================================
// GOOGLE APPS SCRIPT - LƯU KẾT QUẢ TRẮC NGHIỆM HỌC SINH
// =============================================================================

function doGet(e) {
  try {
    // Lấy tham số từ URL
    const studentName = e.parameter.student_name || '';
    const className = e.parameter.class_name || '';
    const quizId = e.parameter.quiz_id || '';
    const score = parseInt(e.parameter.score) || 0;
    const total = parseInt(e.parameter.total) || 0;
    const duration = parseInt(e.parameter.duration) || 0;
    
    // Kiểm tra dữ liệu
    if (!studentName || !className || !quizId) {
      return ContentService.createTextOutput(
        JSON.stringify({
          success: false,
          message: 'Thiếu thông tin bắt buộc'
        })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Mở Google Sheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Results');
    
    // Tạo timestamp
    const timestamp = new Date();
    
    // Tính phần trăm
    const percentage = total > 0 ? ((score / total) * 100).toFixed(1) + '%' : '0%';
    
    // Thêm dòng mới
    sheet.appendRow([
      timestamp,
      studentName,
      className,
      quizId,
      score,
      total,
      percentage,
      duration
    ]);
    
    // Format timestamp column
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
    
    // Trả về kết quả
    return ContentService.createTextOutput(
      JSON.stringify({
        success: true,
        message: 'Đã lưu kết quả thành công',
        data: {
          student: studentName,
          class: className,
          quiz: quizId,
          score: score + '/' + total,
          percentage: percentage
        }
      })
    ).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Xử lý lỗi
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        message: 'Lỗi: ' + error.toString()
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// Hàm test (có thể chạy để kiểm tra)
function testScript() {
  const testParams = {
    parameter: {
      student_name: 'Nguyễn Văn A',
      class_name: '6/1',
      quiz_id: 'K6_B3',
      score: '8',
      total: '10',
      duration: '450'
    }
  };
  
  const result = doGet(testParams);
  Logger.log(result.getContent());
}
```

### 2.2. Lưu Script

1. Click **💾 Save** (Ctrl + S)
2. Đặt tên project: **`Quiz Results Logger`**

---

## 🚀 BƯỚC 3: DEPLOY WEB APP

### 3.1. Deploy Script

1. Click **Deploy** → **New deployment**
2. Click biểu tượng ⚙️ → Chọn **Web app**
3. Cấu hình:
   - **Description**: `Quiz Results API v1`
   - **Execute as**: **Me** (your-email@gmail.com)
   - **Who has access**: **Anyone** (quan trọng!)
4. Click **Deploy**

### 3.2. Cấp quyền

1. Click **Authorize access**
2. Chọn tài khoản Google của bạn
3. Click **Advanced** → **Go to Quiz Results Logger (unsafe)**
4. Click **Allow**

### 3.3. Lấy URL

Sau khi deploy thành công, bạn sẽ nhận được **Web app URL**:

```
https://script.google.com/macros/s/AKfycby...YOUR_ID.../exec
```

**⚠️ LƯU Ý: Copy URL này, bạn sẽ cần dùng ở bước tiếp theo!**

---

## 🔧 BƯỚC 4: CẬP NHẬT URL TRONG FILE HTML

### 4.1. Cập nhật ENDPOINT

Bạn cần thay thế URL cũ bằng URL mới trong **TẤT CẢ 31 file HTML** (K6_*.html):

**URL cũ (không hoạt động):**
```javascript
const ENDPOINT="https://script.google.com/macros/s/AKfycbwj9IiX8PXC-bNsh4DGIw0uysx0v3jWPNeu0lQpieUIQAx9sT9YNUKTZoQFBjg-w86TKg/exec";
```

**URL mới (thay YOUR_NEW_ID bằng ID thực tế):**
```javascript
const ENDPOINT="https://script.google.com/macros/s/YOUR_NEW_ID/exec";
```

### 4.2. Script tự động cập nhật

Tôi sẽ tạo script Python để cập nhật tự động tất cả file HTML:

**File: `scripts/update_endpoint.py`**

```python
import os
import re

# Thay YOUR_NEW_ENDPOINT_URL bằng URL thực tế từ bước 3.3
NEW_ENDPOINT = "https://script.google.com/macros/s/YOUR_NEW_ID/exec"

# Pattern để tìm ENDPOINT cũ
OLD_PATTERN = r'const ENDPOINT="https://script\.google\.com/macros/s/[^"]+";'
NEW_LINE = f'const ENDPOINT="{NEW_ENDPOINT}";'

# Lấy danh sách file HTML
html_files = [f for f in os.listdir('.') if f.startswith('K6_') and f.endswith('.html')]

print(f"Tìm thấy {len(html_files)} file HTML")
print(f"Đang cập nhật ENDPOINT...\n")

updated_count = 0

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Thay thế ENDPOINT
    new_content = re.sub(OLD_PATTERN, NEW_LINE, content)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Đã cập nhật: {filename}")
        updated_count += 1
    else:
        print(f"⚠️ Không tìm thấy ENDPOINT trong: {filename}")

print(f"\n🎉 Hoàn thành! Đã cập nhật {updated_count}/{len(html_files)} file")
```

**Cách chạy:**
```bash
# 1. Sửa NEW_ENDPOINT trong file update_endpoint.py
# 2. Chạy script
python scripts/update_endpoint.py
```

---

## ✅ BƯỚC 5: KIỂM TRA

### 5.1. Test trên trình duyệt

1. Mở file `K6_B3.html` trong trình duyệt
2. Đăng nhập (nếu chưa)
3. Làm bài trắc nghiệm
4. Kiểm tra xem có thông báo **"✅ Đã lưu!"**

### 5.2. Kiểm tra Google Sheets

1. Mở Google Sheets
2. Xem sheet **Results**
3. Kiểm tra xem có dòng dữ liệu mới

---

## 🔍 XỬ LÝ LỖI

### Lỗi 1: "⚠️ Không lưu được"

**Nguyên nhân**: URL endpoint sai hoặc script chưa được deploy đúng

**Giải pháp**:
1. Kiểm tra lại URL trong file HTML
2. Đảm bảo đã chọn **"Who has access: Anyone"** khi deploy
3. Thử deploy lại script

### Lỗi 2: Script không chạy

**Nguyên nhân**: Chưa cấp quyền

**Giải pháp**:
1. Vào Apps Script → Deploy → Test deployments
2. Click **Authorize** và cấp quyền lại

### Lỗi 3: Dữ liệu không xuất hiện trong Sheet

**Nguyên nhân**: Tên sheet sai

**Giải pháp**:
1. Đảm bảo sheet có tên chính xác là **"Results"** (phân biệt chữ hoa/thường)
2. Hoặc sửa tên sheet trong code Apps Script:
```javascript
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('TÊN_SHEET_CỦA_BẠN');
```

---

## 📊 BƯỚC 6: XEM BÁO CÁO (TÙY CHỌN)

### 6.1. Tạo Dashboard trong Google Sheets

Tạo sheet mới tên **"Dashboard"** với các công thức:

**Tổng số lần làm bài:**
```
=COUNTA(Results!A:A)-1
```

**Điểm trung bình:**
```
=AVERAGE(Results!G:G)
```

**Top 5 học sinh:**
```
=QUERY(Results!B:G, "SELECT B, AVG(G) GROUP BY B ORDER BY AVG(G) DESC LIMIT 5 LABEL AVG(G) 'Điểm TB'")
```

### 6.2. Tạo biểu đồ

1. Chọn dữ liệu trong sheet Results
2. Insert → Chart
3. Chọn loại biểu đồ phù hợp (Line chart, Bar chart...)

---

## 🎓 LƯU Ý QUAN TRỌNG

1. ⚠️ **Bảo mật**: URL endpoint là công khai, bất kỳ ai biết URL đều có thể gửi dữ liệu
2. 🔒 **Giải pháp**: Thêm xác thực API key trong script nếu cần
3. 💾 **Backup**: Nên backup Google Sheets định kỳ
4. 📈 **Giới hạn**: Google Apps Script có giới hạn 20,000 lượt gọi/ngày

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra **Execution log** trong Apps Script Editor
2. Xem **View** → **Logs** để debug
3. Test bằng hàm `testScript()` trong Apps Script

---

**🎉 Chúc bạn thiết lập thành công!**

