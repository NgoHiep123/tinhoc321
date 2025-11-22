-- ============================================================
-- FILE: create_database.sql
-- Mô tả: Script tạo database và các bảng cho hệ thống lưu kết quả trắc nghiệm
-- ============================================================

CREATE DATABASE IF NOT EXISTS tinhoc321_quiz 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE tinhoc321_quiz;

-- ============================================================
-- Bảng kết quả trắc nghiệm
-- ============================================================
CREATE TABLE quiz_results (
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
  INDEX idx_created (created_at),
  INDEX idx_student_class (student_name, class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Bảng học sinh (tùy chọn - để quản lý danh sách học sinh)
-- ============================================================
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  class_name VARCHAR(20) NOT NULL,
  email VARCHAR(100),
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY unique_student (name, class_name),
  INDEX idx_class (class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- View thống kê theo bài quiz
-- ============================================================
CREATE VIEW v_quiz_stats AS
SELECT 
  quiz_id,
  COUNT(*) as total_attempts,
  COUNT(DISTINCT student_name) as unique_students,
  AVG(percentage) as avg_score,
  MAX(percentage) as max_score,
  MIN(percentage) as min_score,
  AVG(duration) as avg_duration
FROM quiz_results
GROUP BY quiz_id;

-- ============================================================
-- View thống kê theo học sinh
-- ============================================================
CREATE VIEW v_student_stats AS
SELECT 
  student_name,
  class_name,
  COUNT(*) as total_attempts,
  COUNT(DISTINCT quiz_id) as quizzes_completed,
  AVG(percentage) as avg_score,
  MAX(percentage) as max_score,
  MIN(percentage) as min_score,
  SUM(duration) as total_time_seconds
FROM quiz_results
GROUP BY student_name, class_name;

-- ============================================================
-- View thống kê theo lớp
-- ============================================================
CREATE VIEW v_class_stats AS
SELECT 
  class_name,
  COUNT(*) as total_attempts,
  COUNT(DISTINCT student_name) as total_students,
  COUNT(DISTINCT quiz_id) as total_quizzes,
  AVG(percentage) as class_avg_score
FROM quiz_results
GROUP BY class_name;

