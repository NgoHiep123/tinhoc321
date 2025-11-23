<?php
/**
 * FILE: test_api.php
 * Mô tả: Script test API để kiểm tra kết nối database và API
 * Cách dùng: Mở file này trong trình duyệt hoặc chạy: php test_api.php
 */

require_once 'api/config.php';

header('Content-Type: text/html; charset=utf-8');

?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test API - Hệ thống lưu kết quả</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .test-section {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success {
            color: #10b981;
            font-weight: bold;
        }
        .error {
            color: #ef4444;
            font-weight: bold;
        }
        .info {
            color: #3b82f6;
        }
        pre {
            background: #f3f4f6;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        button {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #2563eb;
        }
    </style>
</head>
<body>
    <h1>🧪 Test API - Hệ thống lưu kết quả</h1>
    
    <?php
    // Test 1: Kết nối Database
    echo '<div class="test-section">';
    echo '<h2>1. Test kết nối Database</h2>';
    try {
        $pdo = getDBConnection();
        echo '<p class="success">✅ Kết nối database thành công!</p>';
        
        // Kiểm tra bảng
        $tables = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);
        echo '<p class="info">📊 Các bảng trong database:</p>';
        echo '<ul>';
        foreach ($tables as $table) {
            echo "<li>$table</li>";
        }
        echo '</ul>';
        
        // Kiểm tra số bản ghi
        $stmt = $pdo->query("SELECT COUNT(*) as count FROM quiz_results");
        $result = $stmt->fetch();
        echo "<p class="info">📈 Số bản ghi trong quiz_results: <strong>{$result['count']}</strong></p>";
        
    } catch (Exception $e) {
        echo '<p class="error">❌ Lỗi kết nối database: ' . htmlspecialchars($e->getMessage()) . '</p>';
        echo '<p class="error">💡 Kiểm tra lại thông tin trong api/config.php</p>';
    }
    echo '</div>';
    
    // Test 2: Test API Save Result
    echo '<div class="test-section">';
    echo '<h2>2. Test API Save Result</h2>';
    echo '<p>Nhấn nút bên dưới để test lưu kết quả:</p>';
    echo '<button onclick="testSaveResult()">Test Lưu Kết Quả</button>';
    echo '<div id="save-result"></div>';
    echo '</div>';
    
    // Test 3: Test API Get Results
    echo '<div class="test-section">';
    echo '<h2>3. Test API Get Results</h2>';
    echo '<p>Nhấn nút bên dưới để test lấy kết quả:</p>';
    echo '<button onclick="testGetResults()">Test Lấy Kết Quả</button>';
    echo '<div id="get-result"></div>';
    echo '</div>';
    
    // Test 4: Test từ Database
    echo '<div class="test-section">';
    echo '<h2>4. Kết quả gần đây (từ Database)</h2>';
    try {
        $pdo = getDBConnection();
        $stmt = $pdo->query("
            SELECT 
                id, student_name, class_name, quiz_id, 
                score, total, percentage, duration,
                DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at
            FROM quiz_results
            ORDER BY created_at DESC
            LIMIT 10
        ");
        $results = $stmt->fetchAll();
        
        if (count($results) > 0) {
            echo '<table border="1" cellpadding="8" style="width:100%; border-collapse: collapse;">';
            echo '<tr style="background:#f3f4f6;">';
            echo '<th>ID</th><th>Học sinh</th><th>Lớp</th><th>Bài</th><th>Điểm</th><th>%</th><th>Thời gian</th><th>Ngày</th>';
            echo '</tr>';
            foreach ($results as $row) {
                echo '<tr>';
                echo "<td>{$row['id']}</td>";
                echo "<td>{$row['student_name']}</td>";
                echo "<td>{$row['class_name']}</td>";
                echo "<td>{$row['quiz_id']}</td>";
                echo "<td>{$row['score']}/{$row['total']}</td>";
                echo "<td>{$row['percentage']}%</td>";
                echo "<td>{$row['duration']}s</td>";
                echo "<td>{$row['created_at']}</td>";
                echo '</tr>';
            }
            echo '</table>';
        } else {
            echo '<p class="info">📭 Chưa có dữ liệu. Hãy test lưu kết quả trước.</p>';
        }
    } catch (Exception $e) {
        echo '<p class="error">❌ Lỗi: ' . htmlspecialchars($e->getMessage()) . '</p>';
    }
    echo '</div>';
    ?>
    
    <script>
        async function testSaveResult() {
            const resultDiv = document.getElementById('save-result');
            resultDiv.innerHTML = '<p class="info">⏳ Đang test...</p>';
            
            const testData = {
                student_name: 'Test Student',
                class_name: '7/1',
                quiz_id: 'TEST_QUIZ',
                score: 15,
                total: 20,
                duration: 300
            };
            
            try {
                const response = await fetch('api/save_result.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(testData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <p class="success">✅ Test thành công!</p>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <p class="error">❌ Test thất bại!</p>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <p class="error">❌ Lỗi: ${error.message}</p>
                    <p class="error">💡 Kiểm tra lại endpoint và CORS</p>
                `;
            }
        }
        
        async function testGetResults() {
            const resultDiv = document.getElementById('get-result');
            resultDiv.innerHTML = '<p class="info">⏳ Đang test...</p>';
            
            try {
                const response = await fetch('api/get_results.php?limit=5');
                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `
                        <p class="success">✅ Test thành công! (${result.count} kết quả)</p>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <p class="error">❌ Test thất bại!</p>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <p class="error">❌ Lỗi: ${error.message}</p>
                    <p class="error">💡 Kiểm tra lại endpoint và CORS</p>
                `;
            }
        }
    </script>
</body>
</html>

