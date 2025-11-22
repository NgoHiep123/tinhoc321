<?php
/**
 * FILE: dashboard/index.php
 * Mô tả: Dashboard giáo viên để xem thống kê kết quả trắc nghiệm
 */

require_once '../api/config.php';

// Bảo mật: Có thể thêm authentication ở đây
// session_start();
// if (!isset($_SESSION['teacher_logged_in'])) {
//     header('Location: login.php');
//     exit;
// }

$pdo = getDBConnection();

// Thống kê tổng quan
$stats = $pdo->query("
    SELECT 
        COUNT(DISTINCT student_name) as total_students,
        COUNT(*) as total_attempts,
        AVG(percentage) as avg_score,
        COUNT(DISTINCT quiz_id) as total_quizzes,
        COUNT(DISTINCT class_name) as total_classes
    FROM quiz_results
")->fetch();

// Kết quả gần đây (20 bản ghi mới nhất)
$recent = $pdo->query("
    SELECT 
        student_name,
        class_name,
        quiz_id,
        score,
        total,
        percentage,
        duration,
        DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at
    FROM quiz_results
    ORDER BY created_at DESC
    LIMIT 20
")->fetchAll();

// Thống kê theo bài
$quiz_stats = $pdo->query("
    SELECT 
        quiz_id,
        COUNT(*) as attempts,
        COUNT(DISTINCT student_name) as students,
        AVG(percentage) as avg_score,
        MAX(percentage) as max_score,
        MIN(percentage) as min_score
    FROM quiz_results
    GROUP BY quiz_id
    ORDER BY attempts DESC
    LIMIT 10
")->fetchAll();

// Thống kê theo lớp
$class_stats = $pdo->query("
    SELECT 
        class_name,
        COUNT(*) as attempts,
        COUNT(DISTINCT student_name) as students,
        AVG(percentage) as avg_score
    FROM quiz_results
    GROUP BY class_name
    ORDER BY class_name
")->fetchAll();

?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Dashboard - Kết quả trắc nghiệm</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
    </style>
</head>
<body class="min-h-screen py-8">
    <div class="container mx-auto px-4 max-w-7xl">
        <!-- Header -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h1 class="text-4xl font-black text-gray-900 mb-2">📊 Dashboard Kết Quả Trắc Nghiệm</h1>
            <p class="text-gray-600">Quản lý và theo dõi kết quả học tập của học sinh</p>
        </div>
        
        <!-- Thống kê tổng quan -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="text-gray-500 text-sm mb-1">Tổng học sinh</div>
                <div class="text-3xl font-black text-purple-600"><?= number_format($stats['total_students']) ?></div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="text-gray-500 text-sm mb-1">Lượt làm bài</div>
                <div class="text-3xl font-black text-blue-600"><?= number_format($stats['total_attempts']) ?></div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="text-gray-500 text-sm mb-1">Điểm trung bình</div>
                <div class="text-3xl font-black text-green-600"><?= round($stats['avg_score'], 1) ?>%</div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="text-gray-500 text-sm mb-1">Số bài quiz</div>
                <div class="text-3xl font-black text-orange-600"><?= $stats['total_quizzes'] ?></div>
            </div>
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="text-gray-500 text-sm mb-1">Số lớp</div>
                <div class="text-3xl font-black text-red-600"><?= $stats['total_classes'] ?></div>
            </div>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <!-- Kết quả gần đây -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="p-4 bg-gradient-to-r from-purple-500 to-indigo-600">
                    <h2 class="text-xl font-bold text-white">Kết quả gần đây</h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-4 py-2 text-left text-xs font-bold">Thời gian</th>
                                <th class="px-4 py-2 text-left text-xs font-bold">Học sinh</th>
                                <th class="px-4 py-2 text-left text-xs font-bold">Lớp</th>
                                <th class="px-4 py-2 text-left text-xs font-bold">Bài</th>
                                <th class="px-4 py-2 text-right text-xs font-bold">Điểm</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <?php foreach ($recent as $row): ?>
                            <tr class="hover:bg-gray-50">
                                <td class="px-4 py-2 text-sm"><?= htmlspecialchars($row['created_at']) ?></td>
                                <td class="px-4 py-2 text-sm font-semibold"><?= htmlspecialchars($row['student_name']) ?></td>
                                <td class="px-4 py-2 text-sm"><?= htmlspecialchars($row['class_name']) ?></td>
                                <td class="px-4 py-2 text-sm"><span class="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-bold"><?= htmlspecialchars($row['quiz_id']) ?></span></td>
                                <td class="px-4 py-2 text-right">
                                    <span class="<?= $row['percentage'] >= 70 ? 'text-green-600' : ($row['percentage'] >= 50 ? 'text-yellow-600' : 'text-red-600') ?> font-black">
                                        <?= $row['score'] ?>/<?= $row['total'] ?> (<?= round($row['percentage'], 1) ?>%)
                                    </span>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Thống kê theo lớp -->
            <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <div class="p-4 bg-gradient-to-r from-blue-500 to-cyan-600">
                    <h2 class="text-xl font-bold text-white">Thống kê theo lớp</h2>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-4 py-2 text-left text-xs font-bold">Lớp</th>
                                <th class="px-4 py-2 text-right text-xs font-bold">Học sinh</th>
                                <th class="px-4 py-2 text-right text-xs font-bold">Lượt làm</th>
                                <th class="px-4 py-2 text-right text-xs font-bold">ĐTB</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <?php foreach ($class_stats as $row): ?>
                            <tr class="hover:bg-gray-50">
                                <td class="px-4 py-2 text-sm font-semibold"><?= htmlspecialchars($row['class_name']) ?></td>
                                <td class="px-4 py-2 text-sm text-right"><?= $row['students'] ?></td>
                                <td class="px-4 py-2 text-sm text-right"><?= $row['attempts'] ?></td>
                                <td class="px-4 py-2 text-right">
                                    <span class="font-black <?= $row['avg_score'] >= 70 ? 'text-green-600' : ($row['avg_score'] >= 50 ? 'text-yellow-600' : 'text-red-600') ?>">
                                        <?= round($row['avg_score'], 1) ?>%
                                    </span>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Thống kê theo bài -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="p-4 bg-gradient-to-r from-green-500 to-emerald-600">
                <h2 class="text-xl font-bold text-white">Thống kê theo bài quiz</h2>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="px-4 py-2 text-left text-xs font-bold">Bài quiz</th>
                            <th class="px-4 py-2 text-right text-xs font-bold">Lượt làm</th>
                            <th class="px-4 py-2 text-right text-xs font-bold">Học sinh</th>
                            <th class="px-4 py-2 text-right text-xs font-bold">ĐTB</th>
                            <th class="px-4 py-2 text-right text-xs font-bold">Cao nhất</th>
                            <th class="px-4 py-2 text-right text-xs font-bold">Thấp nhất</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <?php foreach ($quiz_stats as $row): ?>
                        <tr class="hover:bg-gray-50">
                            <td class="px-4 py-2 text-sm font-semibold"><span class="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-bold"><?= htmlspecialchars($row['quiz_id']) ?></span></td>
                            <td class="px-4 py-2 text-sm text-right"><?= $row['attempts'] ?></td>
                            <td class="px-4 py-2 text-sm text-right"><?= $row['students'] ?></td>
                            <td class="px-4 py-2 text-right font-black"><?= round($row['avg_score'], 1) ?>%</td>
                            <td class="px-4 py-2 text-right text-green-600 font-bold"><?= round($row['max_score'], 1) ?>%</td>
                            <td class="px-4 py-2 text-right text-red-600 font-bold"><?= round($row['min_score'], 1) ?>%</td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="mt-6 text-center text-gray-500 text-sm">
            <p>Dashboard được cập nhật tự động từ database</p>
            <p class="mt-2">Cập nhật lần cuối: <?= date('d/m/Y H:i:s') ?></p>
        </div>
    </div>
</body>
</html>

