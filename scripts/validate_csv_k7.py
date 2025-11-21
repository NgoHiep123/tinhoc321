#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra chất lượng file CSV trước khi tạo HTML
Giúp phát hiện lỗi sớm, tránh phải sửa sau
"""

import csv
import os
import sys

def validate_csv_file(filepath):
    """Kiểm tra file CSV"""
    errors = []
    warnings = []
    
    print(f"\n=== Checking {os.path.basename(filepath)} ===")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Đọc file
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        return False
    
    if len(lines) < 2:
        print(f"❌ File too short (need at least header + 1 question)")
        return False
    
    # Kiểm tra header
    header_line = lines[0].strip().strip('"')
    expected_header = "q_id,topic_id,question_text,option_A,option_B,option_C,option_D,correct_option,difficulty,source"
    
    if header_line != expected_header:
        errors.append(f"Invalid header. Expected:\n  {expected_header}\nGot:\n  {header_line}")
    
    # Parse các dòng dữ liệu
    questions = []
    for i, line in enumerate(lines[1:], start=2):
        line = line.strip()
        if not line:
            warnings.append(f"Line {i}: Empty line (will be ignored)")
            continue
        
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        
        parts = [p.strip() for p in line.split(',')]
        
        if len(parts) != 10:
            errors.append(f"Line {i}: Expected 10 columns, got {len(parts)}")
            continue
        
        q = {
            'line': i,
            'q_id': parts[0],
            'topic_id': parts[1],
            'question_text': parts[2],
            'option_A': parts[3],
            'option_B': parts[4],
            'option_C': parts[5],
            'option_D': parts[6],
            'correct_option': parts[7],
            'difficulty': parts[8],
            'source': parts[9]
        }
        questions.append(q)
    
    print(f"[OK] Found {len(questions)} questions")
    
    # Kiểm tra từng câu hỏi
    q_ids = set()
    
    for q in questions:
        line = q['line']
        
        # Kiểm tra q_id
        if not q['q_id']:
            errors.append(f"Line {line}: q_id is empty")
        elif q['q_id'] in q_ids:
            errors.append(f"Line {line}: Duplicate q_id '{q['q_id']}'")
        else:
            q_ids.add(q['q_id'])
        
        # Kiểm tra format q_id (K7A1_01)
        if q['q_id'] and not q['q_id'].startswith('K7'):
            warnings.append(f"Line {line}: q_id '{q['q_id']}' should start with 'K7'")
        
        # Kiểm tra câu hỏi
        if not q['question_text']:
            errors.append(f"Line {line}: question_text is empty")
        elif len(q['question_text']) > 150:
            warnings.append(f"Line {line}: question_text is too long ({len(q['question_text'])} chars)")
        
        # Kiểm tra đáp án
        for opt in ['option_A', 'option_B', 'option_C', 'option_D']:
            if not q[opt]:
                errors.append(f"Line {line}: {opt} is empty")
            elif len(q[opt]) > 100:
                warnings.append(f"Line {line}: {opt} is too long ({len(q[opt])} chars)")
        
        # Kiểm tra correct_option
        if q['correct_option'] not in ['A', 'B', 'C', 'D']:
            errors.append(f"Line {line}: correct_option must be A, B, C, or D, got '{q['correct_option']}'")
        
        # Kiểm tra difficulty
        valid_difficulties = ['Nhận biết', 'Thông hiểu', 'Vận dụng']
        if q['difficulty'] not in valid_difficulties:
            warnings.append(f"Line {line}: difficulty should be one of {valid_difficulties}, got '{q['difficulty']}'")
    
    # Kiểm tra phân bổ theo bài
    lessons = {}
    for q in questions:
        if q['q_id']:
            # Extract lesson code (K7A1 from K7A1_01)
            lesson_code = '_'.join(q['q_id'].split('_')[:-1])
            if lesson_code not in lessons:
                lessons[lesson_code] = []
            lessons[lesson_code].append(q)
    
    print(f"\n=== Statistics ===")
    print(f"  Total questions: {len(questions)}")
    print(f"  Lessons: {len(lessons)}")
    
    for lesson_code in sorted(lessons.keys()):
        count = len(lessons[lesson_code])
        status = "[OK]" if count == 12 else "[!]"
        print(f"  {status} {lesson_code}: {count} questions", end="")
        if count != 12:
            print(f" (recommend 12)")
        else:
            print()
    
    # Hiển thị kết quả
    print(f"\n=== Validation Results ===")
    
    if errors:
        print(f"\n[ERROR] Found {len(errors)} errors:")
        for err in errors[:10]:  # Hiển thị 10 lỗi đầu
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors)-10} more errors")
    
    if warnings:
        print(f"\n[WARNING] Found {len(warnings)} warnings:")
        for warn in warnings[:10]:  # Hiển thị 10 warning đầu
            print(f"  - {warn}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings)-10} more warnings")
    
    if not errors and not warnings:
        print("[OK] Perfect! No errors or warnings found.")
    elif not errors:
        print(f"\n[OK] No errors found. {len(warnings)} warnings (can proceed).")
    else:
        print(f"\n[ERROR] Found {len(errors)} errors. Please fix before generating HTML.")
        return False
    
    return True

def main():
    """Hàm chính"""
    if len(sys.argv) < 2:
        print("Usage: python validate_csv_k7.py <csv_file>")
        print("Example: python validate_csv_k7.py Bai_tap_Tin_7/K7_question_A_full.csv")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    success = validate_csv_file(filepath)
    
    if success:
        print("\n[OK] Validation passed! You can proceed to generate HTML.")
        sys.exit(0)
    else:
        print("\n[ERROR] Validation failed. Please fix errors first.")
        sys.exit(1)

if __name__ == '__main__':
    main()

