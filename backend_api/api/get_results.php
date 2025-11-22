<?php
/**
 * FILE: api/get_results.php
 * Mô tả: API endpoint để lấy kết quả trắc nghiệm
 * Method: GET
 * Parameters:
 *   - quiz_id: Lọc theo mã bài (optional)
 *   - class_name: Lọc theo lớp (optional)
 *   - student_name: Lọc theo học sinh (optional)
 *   - limit: Giới hạn số kết quả (default: 100)
 */

require_once 'config.php';

setCORSHeaders();

try {
    $pdo = getDBConnection();
    
    // Lấy tham số từ query string
    $quiz_id = isset($_GET['quiz_id']) ? sanitizeString($_GET['quiz_id'], 50) : null;
    $class_name = isset($_GET['class_name']) ? sanitizeString($_GET['class_name'], 20) : null;
    $student_name = isset($_GET['student_name']) ? sanitizeString($_GET['student_name'], 100) : null;
    $limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 100;
    
    // Giới hạn limit để tránh query quá lớn
    if ($limit > 1000) {
        $limit = 1000;
    }
    if ($limit < 1) {
        $limit = 1;
    }
    
    // Build query với điều kiện WHERE
    $where = [];
    $params = [];
    
    if ($quiz_id) {
        $where[] = 'quiz_id = :quiz_id';
        $params[':quiz_id'] = $quiz_id;
    }
    
    if ($class_name) {
        $where[] = 'class_name = :class_name';
        $params[':class_name'] = $class_name;
    }
    
    if ($student_name) {
        $where[] = 'student_name = :student_name';
        $params[':student_name'] = $student_name;
    }
    
    $where_clause = $where ? 'WHERE ' . implode(' AND ', $where) : '';
    
    // Query chính
    $sql = "SELECT 
                id,
                student_name,
                class_name,
                quiz_id,
                score,
                total,
                percentage,
                duration,
                ip_address,
                DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at
            FROM quiz_results
            $where_clause
            ORDER BY created_at DESC
            LIMIT :limit";
    
    $stmt = $pdo->prepare($sql);
    
    // Bind parameters
    foreach ($params as $key => $value) {
        $stmt->bindValue($key, $value);
    }
    $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
    
    $stmt->execute();
    $results = $stmt->fetchAll();
    
    // Trả về kết quả
    echo json_encode([
        'success' => true,
        'count' => count($results),
        'filters' => [
            'quiz_id' => $quiz_id,
            'class_name' => $class_name,
            'student_name' => $student_name,
        ],
        'data' => $results
    ], JSON_UNESCAPED_UNICODE);
    
} catch (PDOException $e) {
    error_log('Database error in get_results.php: ' . $e->getMessage());
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

