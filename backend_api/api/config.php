<?php
/**
 * FILE: api/config.php
 * Mô tả: File cấu hình cho Backend API
 * HƯỚNG DẪN: Sửa các thông tin database và bảo mật trước khi deploy
 */

// ============================================================
// CẤU HÌNH DATABASE
// ============================================================
// Lưu ý: Thay đổi các giá trị này theo thông tin hosting của bạn
define('DB_HOST', 'localhost');  // Hoặc IP của MySQL server (vd: '127.0.0.1' hoặc 'mysql.example.com')
define('DB_NAME', 'tinhoc321_quiz');
define('DB_USER', 'tinhoc321_user');  // Thay bằng username MySQL thực tế
define('DB_PASS', 'YOUR_PASSWORD_HERE');    // Thay bằng password MySQL thực tế
define('DB_CHARSET', 'utf8mb4');

// ============================================================
// CẤU HÌNH CORS (Cross-Origin Resource Sharing)
// ============================================================
// Cho phép các domain này gọi API
define('ALLOWED_ORIGINS', [
    'https://tinhoc321.com',
    'https://www.tinhoc321.com',
    'https://ngohiep123.github.io',  // GitHub Pages
    'https://ngohiep123.github.io/tinhoc321',  // Nếu có subfolder
    'http://localhost:8000',  // Cho phép test local
    'http://127.0.0.1:8000',  // Cho phép test local
    'http://localhost',  // Cho phép test local
    'http://127.0.0.1',  // Cho phép test local
    '*',  // Tạm thời cho phép tất cả (để test, nên thu hẹp lại sau)
]);

// ============================================================
// CẤU HÌNH BẢO MẬT
// ============================================================
// Secret key để xác thực (tạo một key ngẫu nhiên phức tạp)
// Ví dụ: openssl rand -base64 32
define('API_SECRET', 'CHANGE_THIS_TO_A_RANDOM_SECRET_KEY_123456789');  // ⚠️ ĐỔI NGAY!

// Rate limiting: Số request tối đa mỗi IP trong 1 giờ
define('RATE_LIMIT', 100);  // Điều chỉnh theo nhu cầu

// ============================================================
// HÀM KẾT NỐI DATABASE
// ============================================================
function getDBConnection() {
    static $pdo = null;
    
    if ($pdo === null) {
        try {
            $dsn = sprintf(
                'mysql:host=%s;dbname=%s;charset=%s',
                DB_HOST,
                DB_NAME,
                DB_CHARSET
            );
            
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::ATTR_PERSISTENT => false,
            ];
            
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
            
        } catch (PDOException $e) {
            error_log('Database connection failed: ' . $e->getMessage());
            http_response_code(500);
            die(json_encode([
                'success' => false,
                'message' => 'Lỗi kết nối database. Vui lòng liên hệ quản trị viên.'
            ], JSON_UNESCAPED_UNICODE));
        }
    }
    
    return $pdo;
}

// ============================================================
// THIẾT LẬP CORS HEADERS
// ============================================================
function setCORSHeaders() {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    
    // Nếu có '*' trong ALLOWED_ORIGINS, cho phép tất cả (để test)
    if (in_array('*', ALLOWED_ORIGINS)) {
        header("Access-Control-Allow-Origin: $origin");
    } elseif (in_array($origin, ALLOWED_ORIGINS)) {
        header("Access-Control-Allow-Origin: $origin");
    } elseif (!empty($origin)) {
        // Nếu origin không trong danh sách, vẫn cho phép (tạm thời để test)
        header("Access-Control-Allow-Origin: $origin");
    } else {
        // Nếu không có origin (same-origin request), không cần set header
    }
    
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization');
    header('Access-Control-Max-Age: 86400');
    header('Content-Type: application/json; charset=utf-8');
    
    // Handle preflight request
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit;
    }
}

// ============================================================
// RATE LIMITING (Đơn giản)
// ============================================================
function checkRateLimit() {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    
    // Sử dụng thư mục tạm để lưu rate limit
    $cache_dir = sys_get_temp_dir() . '/quiz_api_rate_limit';
    if (!is_dir($cache_dir)) {
        mkdir($cache_dir, 0755, true);
    }
    
    $cache_file = $cache_dir . '/' . md5($ip) . '.json';
    
    $count = 0;
    $now = time();
    
    if (file_exists($cache_file)) {
        $data = json_decode(file_get_contents($cache_file), true);
        if ($data && isset($data['time']) && ($now - $data['time']) < 3600) {  // 1 giờ
            $count = $data['count'] ?? 0;
            
            if ($count >= RATE_LIMIT) {
                http_response_code(429);
                die(json_encode([
                    'success' => false,
                    'message' => 'Quá nhiều request. Vui lòng thử lại sau 1 giờ.',
                    'retry_after' => 3600 - ($now - $data['time'])
                ], JSON_UNESCAPED_UNICODE));
            }
        } else {
            $count = 0;
        }
    }
    
    $count++;
    file_put_contents($cache_file, json_encode([
        'count' => $count,
        'time' => $now
    ]));
}

// ============================================================
// HÀM VALIDATE VÀ SANITIZE INPUT
// ============================================================
function sanitizeString($str, $maxLength = 255) {
    return substr(trim(strip_tags($str)), 0, $maxLength);
}

function validateQuizId($quizId) {
    // Cho phép: chữ, số, gạch dưới, gạch ngang
    return preg_match('/^[a-zA-Z0-9_-]+$/', $quizId);
}

?>

