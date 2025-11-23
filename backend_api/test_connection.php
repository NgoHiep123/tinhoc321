<?php
/**
 * FILE: test_connection.php
 * Mô tả: Script test kết nối database
 * Cách dùng: Mở file này trong trình duyệt hoặc chạy: php test_connection.php
 */

// Load config
require_once 'api/config.php';

header('Content-Type: text/html; charset=utf-8');

?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Kết nối Database</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .test-box {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success { color: #10b981; font-weight: bold; }
        .error { color: #ef4444; font-weight: bold; }
        .info { color: #3b82f6; }
        pre {
            background: #f3f4f6;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background: #f3f4f6;
        }
    </style>
</head>
<body>
    <h1>🔌 Test Kết nối Database</h1>
    
    <?php
    // Test 1: Thông tin cấu hình
    echo '<div class="test-box">';
    echo '<h2>1. Thông tin cấu hình</h2>';
    echo '<table>';
    echo '<tr><th>Cấu hình</th><th>Giá trị</th></tr>';
    echo '<tr><td>DB_HOST</td><td>' . htmlspecialchars(DB_HOST) . '</td></tr>';
    echo '<tr><td>DB_NAME</td><td>' . htmlspecialchars(DB_NAME) . '</td></tr>';
    echo '<tr><td>DB_USER</td><td>' . htmlspecialchars(DB_USER) . '</td></tr>';
    echo '<tr><td>DB_PASS</td><td>' . (DB_PASS ? '***' : '(trống)') . '</td></tr>';
    echo '</table>';
    echo '</div>';
    
    // Test 2: Kết nối Database
    echo '<div class="test-box">';
    echo '<h2>2. Test kết nối Database</h2>';
    try {
        $pdo = getDBConnection();
        echo '<p class="success">✅ Kết nối database thành công!</p>';
        
        // Test 3: Kiểm tra bảng
        echo '<div class="test-box">';
        echo '<h2>3. Kiểm tra bảng trong database</h2>';
        $tables = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
        
        if (count($tables) > 0) {
            echo '<p class="success">✅ Tìm thấy ' . count($tables) . ' bảng:</p>';
            echo '<ul>';
            foreach ($tables as $table) {
                echo "<li><strong>$table</strong></li>";
            }
            echo '</ul>';
        } else {
            echo '<p class="error">❌ Không tìm thấy bảng nào!</p>';
            echo '<p class="error">💡 Hãy chạy script create_database.sql</p>';
        }
        echo '</div>';
        
        // Test 4: Kiểm tra bảng quiz_results
        echo '<div class="test-box">';
        echo '<h2>4. Kiểm tra bảng quiz_results</h2>';
        
        if (in_array('quiz_results', $tables)) {
            echo '<p class="success">✅ Bảng quiz_results đã tồn tại!</p>';
            
            // Kiểm tra cấu trúc
            $columns = $pdo->query("DESCRIBE quiz_results")->fetchAll(PDO::FETCH_ASSOC);
            echo '<p class="info">📋 Cấu trúc bảng:</p>';
            echo '<table>';
            echo '<tr><th>Field</th><th>Type</th><th>Null</th><th>Key</th><th>Default</th></tr>';
            foreach ($columns as $col) {
                echo '<tr>';
                echo '<td>' . htmlspecialchars($col['Field']) . '</td>';
                echo '<td>' . htmlspecialchars($col['Type']) . '</td>';
                echo '<td>' . htmlspecialchars($col['Null']) . '</td>';
                echo '<td>' . htmlspecialchars($col['Key']) . '</td>';
                echo '<td>' . htmlspecialchars($col['Default'] ?? 'NULL') . '</td>';
                echo '</tr>';
            }
            echo '</table>';
            
            // Đếm số bản ghi
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM quiz_results");
            $result = $stmt->fetch();
            echo "<p class="info">📊 Số bản ghi hiện có: <strong>{$result['count']}</strong></p>";
            
            // Hiển thị 5 bản ghi gần nhất
            if ($result['count'] > 0) {
                $stmt = $pdo->query("
                    SELECT id, student_name, class_name, quiz_id, score, total, percentage,
                           DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at
                    FROM quiz_results
                    ORDER BY created_at DESC
                    LIMIT 5
                ");
                $recent = $stmt->fetchAll();
                
                echo '<p class="info">📝 5 bản ghi gần nhất:</p>';
                echo '<table>';
                echo '<tr><th>ID</th><th>Học sinh</th><th>Lớp</th><th>Bài</th><th>Điểm</th><th>Ngày</th></tr>';
                foreach ($recent as $row) {
                    echo '<tr>';
                    echo '<td>' . $row['id'] . '</td>';
                    echo '<td>' . htmlspecialchars($row['student_name']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['class_name']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['quiz_id']) . '</td>';
                    echo '<td>' . $row['score'] . '/' . $row['total'] . ' (' . $row['percentage'] . '%)</td>';
                    echo '<td>' . $row['created_at'] . '</td>';
                    echo '</tr>';
                }
                echo '</table>';
            }
            
        } else {
            echo '<p class="error">❌ Bảng quiz_results chưa tồn tại!</p>';
            echo '<p class="error">💡 Hãy chạy script create_database.sql</p>';
        }
        echo '</div>';
        
        // Test 5: Test INSERT
        echo '<div class="test-box">';
        echo '<h2>5. Test INSERT (thử lưu một bản ghi test)</h2>';
        try {
            $testSql = "INSERT INTO quiz_results 
                       (student_name, class_name, quiz_id, score, total, percentage, duration)
                       VALUES 
                       ('Test Student', '7/1', 'TEST_QUIZ', 15, 20, 75.00, 300)";
            $pdo->exec($testSql);
            
            $testId = $pdo->lastInsertId();
            
            // Xóa bản ghi test
            $pdo->exec("DELETE FROM quiz_results WHERE id = $testId");
            
            echo '<p class="success">✅ Test INSERT thành công! (bản ghi test đã được xóa)</p>';
        } catch (Exception $e) {
            echo '<p class="error">❌ Test INSERT thất bại: ' . htmlspecialchars($e->getMessage()) . '</p>';
        }
        echo '</div>';
        
    } catch (PDOException $e) {
        echo '<p class="error">❌ Lỗi kết nối database!</p>';
        echo '<p class="error">Chi tiết: ' . htmlspecialchars($e->getMessage()) . '</p>';
        echo '<p class="error">💡 Kiểm tra:</p>';
        echo '<ul>';
        echo '<li>MySQL service đã chạy chưa?</li>';
        echo '<li>Thông tin trong api/config.php có đúng không?</li>';
        echo '<li>User có quyền truy cập database không?</li>';
        echo '<li>Database đã được tạo chưa?</li>';
        echo '</ul>';
    } catch (Exception $e) {
        echo '<p class="error">❌ Lỗi: ' . htmlspecialchars($e->getMessage()) . '</p>';
    }
    echo '</div>';
    
    // Test 6: Hướng dẫn tiếp theo
    echo '<div class="test-box">';
    echo '<h2>📋 Hướng dẫn tiếp theo</h2>';
    echo '<ol>';
    echo '<li>Nếu kết nối thành công, bạn có thể test API tại: <a href="test_api.php">test_api.php</a></li>';
    echo '<li>Nếu có lỗi, kiểm tra lại thông tin trong <code>api/config.php</code></li>';
    echo '<li>Đảm bảo database đã được tạo: chạy <code>create_database.sql</code></li>';
    echo '<li>Sau khi setup xong, test từ frontend: làm một bài và kiểm tra kết quả</li>';
    echo '</ol>';
    echo '</div>';
    ?>
    
</body>
</html>

