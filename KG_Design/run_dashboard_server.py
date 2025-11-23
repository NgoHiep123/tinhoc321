"""
Script chạy local web server để xem dashboard giáo viên
Sử dụng: python run_dashboard_server.py
"""

import http.server
import socketserver
import sys
import os

# Fix encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler với CORS support"""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Override để hiển thị log đẹp hơn"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    """Chạy web server"""
    # Chuyển đến thư mục chứa file HTML
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("=" * 70)
            print("🚀 DASHBOARD GIÁO VIÊN - LOCAL WEB SERVER")
            print("=" * 70)
            print(f"\n✅ Server đang chạy tại: http://localhost:{PORT}/")
            print(f"📊 Mở trình duyệt và truy cập: http://localhost:{PORT}/teachers_dashboard.html")
            print(f"\n⚠️  Nhấn Ctrl+C để dừng server\n")
            print("-" * 70)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Đã dừng server")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048:  # Windows: Address already in use
            print(f"\n❌ Lỗi: Port {PORT} đang được sử dụng.")
            print(f"   Vui lòng đóng ứng dụng khác đang dùng port {PORT} hoặc")
            print(f"   sửa PORT trong file này.")
        else:
            print(f"\n❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

