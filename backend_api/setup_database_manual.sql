-- ============================================
-- SETUP DATABASE MYSQL - THỦ CÔNG
-- ============================================
-- Hướng dẫn: Copy và paste từng phần vào MySQL console
-- Hoặc chạy: mysql -u root -p < setup_database_manual.sql
-- ============================================

-- Bước 1: Tạo database (nếu chưa có)
CREATE DATABASE IF NOT EXISTS tinhoc321_quiz 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

-- Bước 2: Sử dụng database
USE tinhoc321_quiz;

-- Bước 3: Tạo bảng quiz_results (nếu chưa có)
CREATE TABLE IF NOT EXISTS quiz_results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_name VARCHAR(100) NOT NULL,
  class_name VARCHAR(20) NOT NULL,
  quiz_id VARCHAR(50) NOT NULL,
  score INT NOT NULL,
  total INT NOT NULL,
  percentage DECIMAL(5,2) NOT NULL,
  duration INT NOT NULL COMMENT 'Thời gian làm bài (giây)',
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_student (student_name),
  INDEX idx_class (class_name),
  INDEX idx_quiz (quiz_id),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bước 4: Tạo bảng students (nếu chưa có)
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  class_name VARCHAR(20) NOT NULL,
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_student (name, class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bước 5: Tạo bảng teachers (nếu chưa có)
CREATE TABLE IF NOT EXISTS teachers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  teacher_id VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  expertise VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bước 6: Tạo view thống kê (tùy chọn)
CREATE OR REPLACE VIEW v_quiz_stats AS
SELECT 
  quiz_id,
  COUNT(*) as total_attempts,
  AVG(percentage) as avg_score,
  MAX(percentage) as max_score,
  MIN(percentage) as min_score,
  COUNT(DISTINCT student_name) as unique_students,
  COUNT(DISTINCT class_name) as unique_classes
FROM quiz_results
GROUP BY quiz_id;

-- Bước 7: Kiểm tra kết quả
SELECT 'Database đã được tạo thành công!' as Status;
SHOW TABLES;
DESCRIBE quiz_results;

-- ============================================
-- HOÀN THÀNH!
-- ============================================

