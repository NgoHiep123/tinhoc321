#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo 4 bài kiểm tra khối 6 học kì 2
- Kiểm tra 5: 20 câu từ D3, E1, E2
- Kiểm tra 6: 20 câu từ D3, E1, E2, E3, E4, E5
- Kiểm tra 7: 20 câu từ E6, E7, E8
- Kiểm tra 8: 20 câu từ D3, E1, E2, E3, E4, E5, E6, E7, E8
"""

import csv
import os
import random
from collections import defaultdict

# Đường dẫn file CSV
CSV_FILES = {
    'D': 'Bai_tap_Tin_6/K6_question_D_full.csv',
    'E': 'Bai_tap_Tin_6/K6_question_E_full.csv',
}

# Đường dẫn output
OUTPUT_DIR = '.'

# Mapping tên bài kiểm tra
TEST_NAMES = {
    5: {
        'id': 'K6_KIEM_TRA_5',
        'title': 'Kiểm tra 5 - Chủ đề D3, E1, E2',
        'icon': '📝',
        'description': '20 câu hỏi từ D3, E1, E2'
    },
    6: {
        'id': 'K6_KIEM_TRA_6',
        'title': 'Kiểm tra 6 - Chủ đề D3, E1, E2, E3, E4, E5',
        'icon': '📚',
        'description': '20 câu hỏi từ D3, E1, E2, E3, E4, E5'
    },
    7: {
        'id': 'K6_KIEM_TRA_7',
        'title': 'Kiểm tra 7 - Chủ đề E6, E7, E8',
        'icon': '🌐',
        'description': '20 câu hỏi từ E6, E7, E8'
    },
    8: {
        'id': 'K6_KIEM_TRA_8',
        'title': 'Kiểm tra 8 - Chủ đề D3, E1-E8',
        'icon': '🎯',
        'description': '20 câu hỏi từ D3, E1, E2, E3, E4, E5, E6, E7, E8'
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
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= len(headers):
                # Lấy đủ số phần tử
                parts = parts[:len(headers)]
                row_dict = dict(zip(headers, parts))
                
                # Lấy mã bài từ q_id (vd: K6D3_01 -> D3, K6E1_01 -> E1)
                q_id = row_dict.get('q_id', '')
                if q_id:
                    # Xử lý q_id: K6D3_01 -> D3, K6E1_01 -> E1
                    lesson_code = q_id.split('_')[0].replace('K6', '')
                    row_dict['lesson_code'] = lesson_code
                    questions.append(row_dict)
    
    return questions


def select_questions_for_test5(all_questions_d, all_questions_e):
    """
    Kiểm tra 5: 20 câu từ D3, E1, E2
    Phân bổ: ~7 câu D3, ~7 câu E1, ~6 câu E2
    """
    selected = []
    
    # Lọc D3
    questions_d3 = [q for q in all_questions_d if q.get('lesson_code', '') == 'D3']
    # Lọc E1
    questions_e1 = [q for q in all_questions_e if q.get('lesson_code', '') == 'E1']
    # Lọc E2
    questions_e2 = [q for q in all_questions_e if q.get('lesson_code', '') == 'E2']
    
    # Lấy câu từ D3
    count_d3 = min(7, len(questions_d3))
    if count_d3 > 0:
        selected.extend(random.sample(questions_d3, count_d3))
    
    # Lấy câu từ E1
    count_e1 = min(7, len(questions_e1))
    if count_e1 > 0:
        selected.extend(random.sample(questions_e1, count_e1))
    
    # Lấy câu từ E2
    remaining = 20 - len(selected)
    count_e2 = min(remaining, len(questions_e2))
    if count_e2 > 0:
        selected.extend(random.sample(questions_e2, count_e2))
    
    random.shuffle(selected)
    return selected


def select_questions_for_test6(all_questions_d, all_questions_e):
    """
    Kiểm tra 6: 20 câu từ D3, E1, E2, E3, E4, E5
    Phân bổ đều: ~3-4 câu mỗi bài
    """
    selected = []
    
    lessons = ['D3', 'E1', 'E2', 'E3', 'E4', 'E5']
    
    # Nhóm câu hỏi theo bài
    questions_by_lesson = {}
    for lesson in lessons:
        if lesson == 'D3':
            questions_by_lesson[lesson] = [q for q in all_questions_d if q.get('lesson_code', '') == lesson]
        else:
            questions_by_lesson[lesson] = [q for q in all_questions_e if q.get('lesson_code', '') == lesson]
    
    # Phân bổ đều: mỗi bài ~3-4 câu
    questions_per_lesson = 3
    for lesson in lessons:
        available = questions_by_lesson.get(lesson, [])
        count = min(questions_per_lesson, len(available))
        if count > 0:
            selected.extend(random.sample(available, count))
    
    # Nếu chưa đủ 20 câu, thêm ngẫu nhiên
    if len(selected) < 20:
        all_available = []
        for lesson in lessons:
            all_available.extend(questions_by_lesson.get(lesson, []))
        
        # Loại bỏ những câu đã chọn
        selected_ids = {q.get('q_id', '') for q in selected}
        remaining = [q for q in all_available if q.get('q_id', '') not in selected_ids]
        
        needed = 20 - len(selected)
        if len(remaining) >= needed:
            selected.extend(random.sample(remaining, needed))
        else:
            selected.extend(remaining)
    
    random.shuffle(selected)
    return selected[:20]  # Đảm bảo chỉ 20 câu


def select_questions_for_test7(all_questions_e):
    """
    Kiểm tra 7: 20 câu từ E6, E7, E8
    Phân bổ: ~7 câu mỗi bài
    """
    selected = []
    
    lessons = ['E6', 'E7', 'E8']
    
    # Nhóm câu hỏi theo bài
    questions_by_lesson = {}
    for lesson in lessons:
        questions_by_lesson[lesson] = [q for q in all_questions_e if q.get('lesson_code', '') == lesson]
    
    # Phân bổ: ~7 câu mỗi bài
    questions_per_lesson = 7
    for lesson in lessons:
        available = questions_by_lesson.get(lesson, [])
        count = min(questions_per_lesson, len(available))
        if count > 0:
            selected.extend(random.sample(available, count))
    
    # Nếu chưa đủ 20 câu, thêm ngẫu nhiên
    if len(selected) < 20:
        all_available = []
        for lesson in lessons:
            all_available.extend(questions_by_lesson.get(lesson, []))
        
        # Loại bỏ những câu đã chọn
        selected_ids = {q.get('q_id', '') for q in selected}
        remaining = [q for q in all_available if q.get('q_id', '') not in selected_ids]
        
        needed = 20 - len(selected)
        if len(remaining) >= needed:
            selected.extend(random.sample(remaining, needed))
        else:
            selected.extend(remaining)
    
    random.shuffle(selected)
    return selected[:20]  # Đảm bảo chỉ 20 câu


def select_questions_for_test8(all_questions_d, all_questions_e):
    """
    Kiểm tra 8: 20 câu từ D3, E1, E2, E3, E4, E5, E6, E7, E8
    Phân bổ: ~2 câu mỗi bài
    """
    selected = []
    
    lessons = ['D3', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8']
    
    # Nhóm câu hỏi theo bài
    questions_by_lesson = {}
    for lesson in lessons:
        if lesson == 'D3':
            questions_by_lesson[lesson] = [q for q in all_questions_d if q.get('lesson_code', '') == lesson]
        else:
            questions_by_lesson[lesson] = [q for q in all_questions_e if q.get('lesson_code', '') == lesson]
    
    # Phân bổ: ~2 câu mỗi bài
    questions_per_lesson = 2
    for lesson in lessons:
        available = questions_by_lesson.get(lesson, [])
        count = min(questions_per_lesson, len(available))
        if count > 0:
            selected.extend(random.sample(available, count))
    
    # Nếu chưa đủ 20 câu, thêm ngẫu nhiên
    if len(selected) < 20:
        all_available = []
        for lesson in lessons:
            all_available.extend(questions_by_lesson.get(lesson, []))
        
        # Loại bỏ những câu đã chọn
        selected_ids = {q.get('q_id', '') for q in selected}
        remaining = [q for q in all_available if q.get('q_id', '') not in selected_ids]
        
        needed = 20 - len(selected)
        if len(remaining) >= needed:
            selected.extend(random.sample(remaining, needed))
        else:
            selected.extend(remaining)
    
    random.shuffle(selected)
    return selected[:20]  # Đảm bảo chỉ 20 câu


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
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 6 - HỌC KÌ 2</span>
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
    print("TẠO 4 BÀI KIỂM TRA KHỐI 6 HỌC KÌ 2")
    print("=" * 60)
    
    # Đọc câu hỏi từ các file CSV
    print("\n[1] Đang đọc câu hỏi từ CSV...")
    questions_d = read_csv_file(CSV_FILES['D'])
    questions_e = read_csv_file(CSV_FILES['E'])
    
    print(f"  - Chủ đề D: {len(questions_d)} câu hỏi")
    print(f"  - Chủ đề E: {len(questions_e)} câu hỏi")
    
    # Thống kê theo bài
    lessons_d = defaultdict(int)
    lessons_e = defaultdict(int)
    for q in questions_d:
        lesson = q.get('lesson_code', '')
        lessons_d[lesson] += 1
    for q in questions_e:
        lesson = q.get('lesson_code', '')
        lessons_e[lesson] += 1
    
    print("\n  Thống kê theo bài:")
    for lesson in sorted(lessons_d.keys()):
        print(f"    - {lesson}: {lessons_d[lesson]} câu")
    for lesson in sorted(lessons_e.keys()):
        print(f"    - {lesson}: {lessons_e[lesson]} câu")
    
    # Tạo 4 bài kiểm tra
    print("\n[2] Đang tạo các bài kiểm tra...")
    
    # Kiểm tra 5
    print("\n  [TEST 5] Tạo Kiểm tra 5 (D3, E1, E2)...")
    test5_questions = select_questions_for_test5(questions_d, questions_e)
    print(f"    - Đã chọn {len(test5_questions)} câu hỏi")
    
    # Kiểm tra 6
    print("\n  [TEST 6] Tạo Kiểm tra 6 (D3, E1, E2, E3, E4, E5)...")
    test6_questions = select_questions_for_test6(questions_d, questions_e)
    print(f"    - Đã chọn {len(test6_questions)} câu hỏi")
    
    # Kiểm tra 7
    print("\n  [TEST 7] Tạo Kiểm tra 7 (E6, E7, E8)...")
    test7_questions = select_questions_for_test7(questions_e)
    print(f"    - Đã chọn {len(test7_questions)} câu hỏi")
    
    # Kiểm tra 8
    print("\n  [TEST 8] Tạo Kiểm tra 8 (D3, E1-E8)...")
    test8_questions = select_questions_for_test8(questions_d, questions_e)
    print(f"    - Đã chọn {len(test8_questions)} câu hỏi")
    
    # Tạo file HTML
    print("\n[3] Đang tạo file HTML...")
    
    tests = [
        (5, test5_questions),
        (6, test6_questions),
        (7, test7_questions),
        (8, test8_questions),
    ]
    
    created_files = []
    for test_num, test_questions in tests:
        html_content = create_html_for_test(test_num, test_questions)
        filename = f"{TEST_NAMES[test_num]['id']}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_files.append(filepath)
        print(f"  [OK] Đã tạo: {filename} ({len(test_questions)} câu)")
    
    # Tóm tắt
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)
    print(f"\nTổng kết:")
    print(f"   - Đã tạo {len(created_files)} file HTML")
    print(f"\nCác file đã tạo:")
    for f in created_files:
        print(f"   - {f}")
    
    print(f"\nBước tiếp theo:")
    print(f"   1. Mở các file HTML trong browser để kiểm tra")
    print(f"   2. Cập nhật index.html để thêm link đến các bài kiểm tra")


if __name__ == '__main__':
    # Đặt seed để có thể tái tạo kết quả (tùy chọn)
    random.seed(42)
    main()

