#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo 4 bài kiểm tra khối 6 học kì 1
- Kiểm tra 1: 20 câu từ A1, A2, A3, A4 (mỗi bài: 3 nhận biết, 1 thông hiểu, 1 vận dụng)
- Kiểm tra 2: 20 câu từ chủ đề A và chủ đề B
- Kiểm tra 3: 20 câu từ C1, C2, C3
- Kiểm tra 4: 40 câu từ chủ đề A, B, C
"""

import csv
import os
import random
from collections import defaultdict

# Đường dẫn file CSV
CSV_FILES = {
    'A': 'Bai_tap_Tin_6/K6_question_A_full.csv',
    'B': 'Bai_tap_Tin_6/K6_question_B_full.csv',
    'C': 'Bai_tap_Tin_6/K6_question_C_full.csv',
}

# Đường dẫn output
OUTPUT_DIR = '.'

# Mapping tên bài kiểm tra
TEST_NAMES = {
    1: {
        'id': 'K6_KIEM_TRA_1',
        'title': 'Kiểm tra 1 - Chủ đề A',
        'icon': '📝',
        'description': '20 câu hỏi từ A1, A2, A3, A4'
    },
    2: {
        'id': 'K6_KIEM_TRA_2',
        'title': 'Kiểm tra 2 - Chủ đề A & B',
        'icon': '📚',
        'description': '20 câu hỏi từ chủ đề A và chủ đề B'
    },
    3: {
        'id': 'K6_KIEM_TRA_3',
        'title': 'Kiểm tra 3 - Chủ đề C',
        'icon': '🌐',
        'description': '20 câu hỏi từ C1, C2, C3'
    },
    4: {
        'id': 'K6_KIEM_TRA_4',
        'title': 'Kiểm tra 4 - Chủ đề A, B, C',
        'icon': '🎯',
        'description': '40 câu hỏi từ chủ đề A, B, C'
    }
}


def read_csv_file(filepath):
    """Đọc file CSV và trả về danh sách câu hỏi"""
    questions = []
    if not os.path.exists(filepath):
        print(f"[WARNING] Khong tim thay file: {filepath}")
        return questions
    
    # File CSV có format đặc biệt: mỗi dòng được bao quanh bởi dấu ngoặc kép
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        
        if not lines:
            return questions
        
        # Xử lý header
        header_line = lines[0].strip()
        if header_line.startswith('"') and header_line.endswith('"'):
            header_line = header_line[1:-1]
        headers = [h.strip() for h in header_line.split(',')]
        
        # Đọc các dòng dữ liệu
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            # Bỏ dấu ngoặc kép bao quanh toàn bộ dòng
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            
            # Split bằng dấu phẩy
            # Lưu ý: có thể có dấu phẩy trong nội dung, nhưng với format này thì split đơn giản vẫn được
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= len(headers):
                # Lấy đủ số phần tử
                parts = parts[:len(headers)]
                row_dict = dict(zip(headers, parts))
                
                # Lấy mã bài từ q_id (vd: K6A1_01 -> A1)
                q_id = row_dict.get('q_id', '')
                if q_id:
                    lesson_code = q_id.split('_')[0].replace('K6', '')
                    row_dict['lesson_code'] = lesson_code
                    questions.append(row_dict)
    
    return questions


def group_questions_by_lesson_and_difficulty(questions):
    """Nhóm câu hỏi theo bài và độ khó"""
    grouped = defaultdict(lambda: defaultdict(list))
    
    for q in questions:
        lesson = q.get('lesson_code', '')
        difficulty = q.get('difficulty', '').strip()
        grouped[lesson][difficulty].append(q)
    
    return grouped


def select_questions_for_test1(all_questions):
    """
    Kiểm tra 1: 20 câu từ A1, A2, A3, A4
    Mỗi bài lấy: 3 nhận biết, 1 thông hiểu, 1 vận dụng
    """
    selected = []
    lessons = ['A1', 'A2', 'A3', 'A4']
    requirements = {
        'Nhận biết': 3,
        'Thông hiểu': 1,
        'Vận dụng': 1
    }
    
    grouped = group_questions_by_lesson_and_difficulty(all_questions)
    
    for lesson in lessons:
        if lesson not in grouped:
            print(f"[WARNING] Không tìm thấy câu hỏi cho bài {lesson}")
            continue
        
        for difficulty, count in requirements.items():
            available = grouped[lesson].get(difficulty, [])
            if len(available) < count:
                print(f"[WARNING] Bài {lesson} - {difficulty}: chỉ có {len(available)} câu, cần {count}")
                count = len(available)
            
            selected.extend(random.sample(available, min(count, len(available))))
    
    random.shuffle(selected)
    return selected


def select_questions_for_test2(all_questions_a, all_questions_b):
    """
    Kiểm tra 2: 20 câu từ chủ đề A và chủ đề B
    Phân bổ đều: 10 câu từ A, 10 câu từ B
    """
    selected = []
    
    # Lấy ngẫu nhiên 10 câu từ A
    if len(all_questions_a) >= 10:
        selected.extend(random.sample(all_questions_a, 10))
    else:
        selected.extend(all_questions_a)
    
    # Lấy ngẫu nhiên 10 câu từ B
    if len(all_questions_b) >= 10:
        selected.extend(random.sample(all_questions_b, 10))
    else:
        selected.extend(all_questions_b)
    
    random.shuffle(selected)
    return selected


def select_questions_for_test3(all_questions_c):
    """
    Kiểm tra 3: 20 câu từ C1, C2, C3
    """
    # Lọc chỉ các bài C1, C2, C3
    filtered = [q for q in all_questions_c if q.get('lesson_code', '') in ['C1', 'C2', 'C3']]
    
    if len(filtered) >= 20:
        selected = random.sample(filtered, 20)
    else:
        selected = filtered
        print(f"[WARNING] Chỉ có {len(filtered)} câu hỏi từ C1, C2, C3, cần 20")
    
    random.shuffle(selected)
    return selected


def select_questions_for_test4(all_questions_a, all_questions_b, all_questions_c):
    """
    Kiểm tra 4: 40 câu từ chủ đề A, B, C
    Phân bổ: A: ~13, B: ~13, C: ~14
    """
    selected = []
    
    # Lấy câu từ A
    count_a = min(13, len(all_questions_a))
    if count_a > 0:
        selected.extend(random.sample(all_questions_a, count_a))
    
    # Lấy câu từ B
    count_b = min(13, len(all_questions_b))
    if count_b > 0:
        selected.extend(random.sample(all_questions_b, count_b))
    
    # Lấy câu từ C
    remaining = 40 - len(selected)
    count_c = min(remaining, len(all_questions_c))
    if count_c > 0:
        selected.extend(random.sample(all_questions_c, count_c))
    
    random.shuffle(selected)
    return selected


def convert_question_to_js_format(q):
    """Chuyển câu hỏi sang format JavaScript"""
    def js_escape(text):
        if not text:
            return ""
        text = str(text).strip()
        text = text.replace('\\', '\\\\')
        text = text.replace('"', '\\"')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        text = text.replace('\t', '\\t')
        return text
    
    def add_period(text):
        text = str(text).strip()
        if text and not text.endswith('.') and not text.endswith('?') and not text.endswith('!'):
            return text + '.'
        return text
    
    question_text = js_escape(q.get('question_text', ''))
    opt_a = js_escape(add_period(q.get('option_A', '')))
    opt_b = js_escape(add_period(q.get('option_B', '')))
    opt_c = js_escape(add_period(q.get('option_C', '')))
    opt_d = js_escape(add_period(q.get('option_D', '')))
    
    # Xác định đáp án đúng
    correct_option = q.get('correct_option', 'A').strip()
    answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'A.': 0, 'B.': 1, 'C.': 2, 'D.': 3}
    answer = answer_map.get(correct_option, 0)
    
    return {
        'question': question_text,
        'options': [opt_a, opt_b, opt_c, opt_d],
        'answer': answer
    }


def create_html_for_test(test_num, questions):
    """Tạo nội dung HTML cho bài kiểm tra"""
    test_info = TEST_NAMES[test_num]
    quiz_id = test_info['id']
    title = test_info['title']
    icon = test_info['icon']
    description = test_info['description']
    
    num_questions = len(questions)
    
    # Chuyển câu hỏi sang format JS
    js_questions = []
    for q in questions:
        js_q = convert_question_to_js_format(q)
        js_questions.append(js_q)
    
    # Tạo chuỗi JavaScript array
    js_lines = []
    for q in js_questions:
        line = f'      {{question: "{q["question"]}", options: ["{q["options"][0]}", "{q["options"][1]}", "{q["options"][2]}", "{q["options"][3]}"], answer: {q["answer"]}}}'
        js_lines.append(line)
    
    js_array = '[\n' + ',\n'.join(js_lines) + '\n    ]'
    
    # Template HTML
    html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <title>⚡ {quiz_id}: {title}</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <style>
    body{{font-family:'Inter',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);background-attachment:fixed}}
    .quiz-container{{background:rgba(255,255,255,0.95);backdrop-filter:blur(10px)}}
    .option-btn{{transition:all 0.3s cubic-bezier(0.4,0,0.2,1)}}
    .option-btn:hover{{transform:translateX(4px);box-shadow:0 10px 25px rgba(99,102,241,0.3)}}
    .correct{{background:linear-gradient(135deg,#10b981 0%,#059669 100%)!important;color:#fff!important;animation:correctPulse 0.6s ease;box-shadow:0 0 30px rgba(16,185,129,0.6)!important}}
    .incorrect{{background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%)!important;color:#fff!important;animation:shake 0.5s ease}}
    @keyframes correctPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
    @keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-10px)}}75%{{transform:translateX(10px)}}}}
  </style>
</head>
<body class="min-h-screen">
  <header class="sticky top-0 z-20 backdrop-blur-lg bg-white/80 border-b border-white/20 shadow-lg">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="index.html" class="inline-flex items-center gap-2 text-purple-700 hover:text-purple-900">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        <span class="font-bold">🏠 Trang chủ</span>
      </a>
      <span id="userPill" class="hidden md:inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold bg-gradient-to-r from-purple-500 to-indigo-500 text-white shadow-lg"></span>
    </div>
  </header>
  <main class="px-4 py-6 flex justify-center">
    <div class="quiz-container w-full max-w-3xl rounded-3xl shadow-2xl p-6 md:p-10">
      <div class="text-center mb-6">
        <div class="inline-block mb-3 px-4 py-2 bg-gradient-to-r from-purple-100 to-indigo-100 rounded-full">
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 6 - HỌC KÌ 1</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">{icon} {title}</h1>
        <p class="text-gray-600 text-lg">🎯 {num_questions} câu hỏi - Thời gian: ~{num_questions * 1} phút</p>
        <p class="text-gray-500 text-sm mt-1">{description}</p>
      </div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl">
        <div class="flex items-center gap-3">
          <div class="text-3xl">📝</div>
          <div><div id="progress" class="text-gray-900 font-bold text-lg">Câu 1/{num_questions}</div><div class="text-sm text-gray-500">Chúc bạn làm bài tốt!</div></div>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex-1 w-48 h-3 rounded-full bg-gray-200 overflow-hidden"><div id="bar" class="h-full rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 transition-all" style="width:2%"></div></div>
          <div id="score" class="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl font-black text-lg shadow-lg">🏆 0</div>
        </div>
      </div>
      <div id="question-card" class="bg-gradient-to-br from-purple-500 to-indigo-600 p-6 rounded-2xl mb-6 min-h-[120px] flex items-center justify-center shadow-xl">
        <p id="question-text" class="text-center text-xl md:text-2xl font-bold text-white leading-relaxed"></p>
      </div>
      <div id="options-container" class="grid grid-cols-1 gap-4 mb-6"></div>
      <div id="feedback-container" class="text-center min-h-[60px] flex items-center justify-center"><p id="feedback-text" class="text-2xl font-bold"></p></div>
      <div class="mt-4 flex justify-end">
        <button id="next-btn" class="hidden w-full md:w-auto bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-black text-lg py-4 px-8 rounded-xl hover:from-purple-700 hover:to-indigo-700 transition-all shadow-lg">➡️ Câu tiếp theo</button>
      </div>
      <div id="results-container" class="hidden text-center">
        <div class="mb-4 text-6xl" id="result-emoji">🎉</div>
        <h2 class="text-4xl font-black text-gray-900 mb-3">Hoàn thành!</h2>
        <div class="my-8">
          <p class="text-7xl font-black bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent" id="final-score"></p>
          <p class="text-2xl text-gray-700 mt-4 font-bold" id="score-comment"></p>
          <p class="text-sm text-gray-500 mt-3" id="send-status">Đang gửi kết quả…</p>
        </div>
        <div class="flex gap-4 justify-center flex-wrap">
          <a href="index.html" class="px-6 py-3 rounded-xl bg-gray-200 text-gray-800 font-bold hover:bg-gray-300">🏠 Trang chủ</a>
          <button id="restart-btn" class="px-8 py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-black hover:from-green-600 hover:to-emerald-600 shadow-lg">🔄 Làm lại</button>
        </div>
      </div>
    </div>
  </main>
  <script>
    const QUIZ_ID="{quiz_id}";
    const ENDPOINT="https://script.google.com/macros/s/AKfycbwj9IiX8PXC-bNsh4DGIw0uysx0v3jWPNeu0lQpieUIQAx9sT9YNUKTZoQFBjg-w86TKg/exec";
    function getStudent(){{try{{return JSON.parse(localStorage.getItem('student')||'null')}}catch(e){{return null}}}}
    const student=getStudent();
    (function(){{const pill=document.getElementById('userPill');if(student&&pill){{pill.classList.remove('hidden');pill.innerHTML=`👤 ${{student.name}} · Lớp ${{student.className}}`}}}})();
    
    const allQuestions={js_array};
    let currentQ=0,score=0,startTime=Date.now();
    function shuffle(arr){{for(let i=arr.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}}return arr}}
    function withShuffledOptions(q){{const order=q.options.map((_,i)=>i);shuffle(order);return{{...q,options:order.map(i=>q.options[i]),answer:order.indexOf(q.answer)}}}}
    const quiz=allQuestions.map(withShuffledOptions);
    
    function showQuestion(){{const q=quiz[currentQ];document.getElementById('question-text').textContent=q.question;document.getElementById('progress').innerHTML=`Câu ${{currentQ+1}}/${{quiz.length}}`;document.getElementById('bar').style.width=((currentQ+1)/quiz.length*100)+'%';const container=document.getElementById('options-container');container.innerHTML='';const letters=['A','B','C','D'];q.options.forEach((opt,i)=>{{const btn=document.createElement('button');btn.className='option-btn w-full text-left px-6 py-4 rounded-xl border-2 border-gray-200 hover:border-purple-400 bg-white font-semibold text-gray-800 text-lg';btn.innerHTML=`<span class="inline-block w-8 h-8 rounded-full bg-purple-100 text-purple-700 font-bold mr-3 text-center leading-8">${{letters[i]}}</span>${{opt}}`;btn.onclick=()=>checkAnswer(i,btn);container.appendChild(btn)}});document.getElementById('next-btn').classList.add('hidden');document.getElementById('feedback-text').textContent=''}}
    
    function checkAnswer(chosen,btn){{
      const q=quiz[currentQ];
      const allBtns=document.querySelectorAll('.option-btn');
      allBtns.forEach(b=>b.disabled=true);
      if(chosen===q.answer){{
        btn.classList.add('correct');
        score++;
        document.getElementById('score').innerHTML=`🏆 ${{score}}`;
        document.getElementById('feedback-text').innerHTML='✅ <span style="color:#10b981">Chính xác!</span>';
        confetti({{particleCount:50,spread:60,origin:{{y:0.6}}}})
      }}else{{
        btn.classList.add('incorrect');
        allBtns[q.answer].classList.add('correct');
        document.getElementById('feedback-text').innerHTML='❌ <span style="color:#ef4444">Chưa đúng!</span>'
      }}
      if(currentQ<quiz.length-1){{
        document.getElementById('next-btn').classList.remove('hidden')
      }}else{{
        setTimeout(showResults,2000)
      }}
    }}
    
    document.getElementById('next-btn').onclick=()=>{{currentQ++;if(currentQ<quiz.length)showQuestion();else showResults()}};
    
    function showResults(){{
      document.querySelector('.quiz-container>div:first-child').classList.add('hidden');
      document.getElementById('question-card').classList.add('hidden');
      document.getElementById('options-container').classList.add('hidden');
      document.getElementById('next-btn').classList.add('hidden');
      document.getElementById('feedback-container').classList.add('hidden');
      document.getElementById('results-container').classList.remove('hidden');
      const pct=(score/quiz.length*100).toFixed(0);
      document.getElementById('final-score').textContent=`${{score}}/${{quiz.length}} (${{pct}}%)`;
      let comment,emoji;
      if(pct>=90){{comment="🌟 Xuất sắc!";emoji="🎉"}}
      else if(pct>=70){{comment="👍 Rất tốt!";emoji="😊"}}
      else if(pct>=50){{comment="💪 Khá tốt!";emoji="😃"}}
      else{{comment="📖 Cố gắng hơn nhé!";emoji="😅"}}
      document.getElementById('score-comment').textContent=comment;
      document.getElementById('result-emoji').textContent=emoji;
      if(pct>=70){{
        const duration=3000,end=Date.now()+duration;
        (function frame(){{
          confetti({{particleCount:3,angle:60,spread:55,origin:{{x:0}}}});
          confetti({{particleCount:3,angle:120,spread:55,origin:{{x:1}}}});
          if(Date.now()<end)requestAnimationFrame(frame)
        }})()
      }}
      const duration=Math.floor((Date.now()-startTime)/1000);
      if(student){{
        sendResult(student.name,student.className,QUIZ_ID,score,quiz.length,duration)
      }}else{{
        document.getElementById('send-status').textContent='Chưa đăng nhập'
      }}
    }}
    
    async function sendResult(name,className,quizId,score,total,duration){{
      try{{
        const url=`${{ENDPOINT}}?student_name=${{encodeURIComponent(name)}}&class_name=${{encodeURIComponent(className)}}&quiz_id=${{encodeURIComponent(quizId)}}&score=${{score}}&total=${{total}}&duration=${{duration}}`;
        await fetch(url,{{mode:'no-cors'}});
        document.getElementById('send-status').textContent='✅ Đã lưu!'
      }}catch(e){{
        document.getElementById('send-status').textContent='⚠️ Không lưu được'
      }}
    }}
    
    document.getElementById('restart-btn').onclick=()=>location.reload();
    showQuestion()
  </script>
</body>
</html>'''
    
    return html_content


def main():
    """Hàm chính"""
    # Xử lý encoding cho console Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("TAO 4 BAI KIEM TRA KHOI 6 HOC KI 1")
    print("=" * 60)
    
    # Đọc câu hỏi từ các file CSV
    print("\n[1] Dang doc cau hoi tu CSV...")
    questions_a = read_csv_file(CSV_FILES['A'])
    questions_b = read_csv_file(CSV_FILES['B'])
    questions_c = read_csv_file(CSV_FILES['C'])
    
    print(f"  - Chu de A: {len(questions_a)} cau hoi")
    print(f"  - Chu de B: {len(questions_b)} cau hoi")
    print(f"  - Chu de C: {len(questions_c)} cau hoi")
    
    # Tạo 4 bài kiểm tra
    print("\n[2] Dang tao cac bai kiem tra...")
    
    # Kiểm tra 1
    print("\n  [TEST 1] Tao Kiem tra 1...")
    test1_questions = select_questions_for_test1(questions_a)
    print(f"    - Da chon {len(test1_questions)} cau hoi")
    
    # Kiểm tra 2
    print("\n  [TEST 2] Tao Kiem tra 2...")
    test2_questions = select_questions_for_test2(questions_a, questions_b)
    print(f"    - Da chon {len(test2_questions)} cau hoi")
    
    # Kiểm tra 3
    print("\n  [TEST 3] Tao Kiem tra 3...")
    test3_questions = select_questions_for_test3(questions_c)
    print(f"    - Da chon {len(test3_questions)} cau hoi")
    
    # Kiểm tra 4
    print("\n  [TEST 4] Tao Kiem tra 4...")
    test4_questions = select_questions_for_test4(questions_a, questions_b, questions_c)
    print(f"    - Da chon {len(test4_questions)} cau hoi")
    
    # Tạo file HTML
    print("\n[3] Dang tao file HTML...")
    
    tests = [
        (1, test1_questions),
        (2, test2_questions),
        (3, test3_questions),
        (4, test4_questions),
    ]
    
    created_files = []
    for test_num, test_questions in tests:
        html_content = create_html_for_test(test_num, test_questions)
        filename = f"{TEST_NAMES[test_num]['id']}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_files.append(filepath)
        print(f"  [OK] Da tao: {filename} ({len(test_questions)} cau)")
    
    # Tóm tắt
    print("\n" + "=" * 60)
    print("HOAN THANH!")
    print("=" * 60)
    print(f"\nTong ket:")
    print(f"   - Da tao {len(created_files)} file HTML")
    print(f"\nCac file da tao:")
    for f in created_files:
        print(f"   - {f}")
    
    print(f"\nBuoc tiep theo:")
    print(f"   1. Mo cac file HTML trong browser de kiem tra")
    print(f"   2. Cap nhat index.html de them link den cac bai kiem tra")


if __name__ == '__main__':
    # Đặt seed để có thể tái tạo kết quả (tùy chọn)
    random.seed(42)
    main()

