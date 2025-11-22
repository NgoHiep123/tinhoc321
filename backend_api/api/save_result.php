<?php
/**
 * FILE: api/save_result.php
 * Mô tả: API endpoint để lưu kết quả trắc nghiệm
 * Method: POST (hoặc GET cho tương thích ngược)
 */

require_once 'config.php';

// Setup
setCORSHeaders();
checkRateLimit();

try {
    // Chỉ chấp nhận POST hoặc GET (GET cho tương thích ngược với Google Sheets)
    $method = $_SERVER['REQUEST_METHOD'];
    
    if (!in_array($method, ['GET', 'POST'])) {
        throw new Exception('Method not allowed. Use GET or POST.');
    }
    
    // Lấy dữ liệu
    if ($method === 'POST') {
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);
        
        // Nếu không parse được JSON, thử lấy từ POST form
        if (!$data) {
            $data = $_POST;
        }
    } else {
        // GET method (tương thích với Google Sheets format)
        $data = $_GET;
    }
    
    // Validate các trường bắt buộc
    $required = ['student_name', 'class_name', 'quiz_id', 'score', 'total', 'duration'];
    foreach ($required as $field) {
        if (!isset($data[$field]) || $data[$field] === '') {
            throw new Exception("Thiếu trường bắt buộc: $field");
        }
    }
    
    // Sanitize và validate dữ liệu
    $student_name = sanitizeString($data['student_name'], 100);
    $class_name = sanitizeString($data['class_name'], 20);
    $quiz_id = sanitizeString($data['quiz_id'], 50);
    
    if (empty($student_name) || empty($class_name) || empty($quiz_id)) {
        throw new Exception('Tên học sinh, lớp hoặc mã bài không được để trống');
    }
    
    if (!validateQuizId($quiz_id)) {
        throw new Exception('Mã bài không hợp lệ. Chỉ chấp nhận chữ, số, gạch dưới và gạch ngang.');
    }
    
    $score = (int)$data['score'];
    $total = (int)$data['total'];
    $duration = (int)$data['duration'];
    
    // Validate giá trị
    if ($total <= 0) {
        throw new Exception('Tổng số câu hỏi phải lớn hơn 0');
    }
    
    if ($score < 0 || $score > $total) {
        throw new Exception("Điểm không hợp lệ: $score/$total");
    }
    
    if ($duration < 0 || $duration > 7200) {  // Max 2 giờ (7200 giây)
        throw new Exception("Thời gian không hợp lệ: $duration giây");
    }
    
    // Tính phần trăm
    $percentage = round(($score / $total) * 100, 2);
    
    // Lấy thông tin bổ sung
    $ip_address = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $user_agent = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 500);  // Giới hạn độ dài
    
    // Lưu vào database
    $pdo = getDBConnection();
    
    $sql = "INSERT INTO quiz_results 
            (student_name, class_name, quiz_id, score, total, percentage, duration, ip_address, user_agent)
            VALUES 
            (:student_name, :class_name, :quiz_id, :score, :total, :percentage, :duration, :ip_address, :user_agent)";
    
    $stmt = $pdo->prepare($sql);
    $result = $stmt->execute([
        ':student_name' => $student_name,
        ':class_name' => $class_name,
        ':quiz_id' => $quiz_id,
        ':score' => $score,
        ':total' => $total,
        ':percentage' => $percentage,
        ':duration' => $duration,
        ':ip_address' => $ip_address,
        ':user_agent' => $user_agent,
    ]);
    
    if (!$result) {
        throw new Exception('Không thể lưu kết quả vào database');
    }
    
    $result_id = $pdo->lastInsertId();
    
    // Trả về kết quả thành công
    echo json_encode([
        'success' => true,
        'message' => 'Đã lưu kết quả thành công',
        'data' => [
            'id' => $result_id,
            'student' => $student_name,
            'class' => $class_name,
            'quiz' => $quiz_id,
            'score' => "$score/$total",
            'percentage' => round($percentage, 1) . '%',
            'duration' => $duration . 's'
        ]
    ], JSON_UNESCAPED_UNICODE);
    
} catch (PDOException $e) {
    error_log('Database error in save_result.php: ' . $e->getMessage());
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Lỗi database. Vui lòng thử lại sau.'
    ], JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
?>

