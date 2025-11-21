#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo các file HTML trắc nghiệm Tin học 6 từ file CSV mới
Mỗi bài có 12 câu, mỗi lần làm chỉ lấy 10 câu ngẫu nhiên
"""

import csv
import os
import json
from collections import defaultdict

# Mapping từ topic_id sang mã bài
TOPIC_TO_LESSON = {
    'A1_Thong_tin_va_xu_li': 'A1',
    'A2_Luu_tru_va_trao_doi': 'A2',
    'A3_May_tinh_trong_HDTT': 'A3',
    'A4_Bieu_dien_du_lieu': 'A4',
    'A5_Du_lieu_trong_may_tinh': 'A5',
    'A6_He_dieu_hanh': 'A6',
}

# Mapping tiêu đề cho từng bài
LESSON_TITLES = {
    'A1': '💻 Thông tin và xử lí',
    'A2': '💾 Lưu trữ và trao đổi',
    'A3': '🖥️ Máy tính trong HDTT',
    'A4': '📊 Biểu diễn dữ liệu',
    'A5': '💿 Dữ liệu trong máy tính',
    'A6': '⚙️ Hệ điều hành',
    'B1': '🌐 Mạng máy tính',
    'B2': '💬 Giao tiếp trực tuyến',
    'B3': '📧 Thư điện tử',
    'B4': '🔍 Tìm kiếm thông tin',
    'B5': '📱 Công cụ trực tuyến',
    'B6': '☁️ Lưu trữ đám mây',
    'C1': '🌍 Thông tin trên Web',
    'C2': '🔐 An toàn thông tin',
    'C3': '🛡️ Bảo mật dữ liệu',
    'C4': '📖 Quyền tác giả',
    'D1': '⚠️ Mặt trái Internet',
    'D2': '🎮 An toàn mạng xã hội',
    'D3': '👨‍👩‍👧 Sử dụng lành mạnh',
    'E1': '🔎 Find & Replace',
    'E2': '📝 Soạn thảo nâng cao',
    'E3': '📊 Bảng biểu Word',
    'E4': '📐 Công thức toán',
    'E5': '🖼️ Hình ảnh trong văn bản',
    'E6': '📄 Trình bày tài liệu',
    'F1': '🧮 Khái niệm thuật toán',
    'F2': '🎯 Lập trình Scratch',
}

def read_csv_file(filepath):
    """Đọc file CSV và trả về danh sách câu hỏi"""
    questions = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig để tự động bỏ BOM
        lines = f.readlines()
        
        # Xử lý header: bỏ dấu ngoặc kép bao quanh và split
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
            
            # Tạo dictionary nếu số cột khớp
            if len(parts) == len(headers):
                row = dict(zip(headers, parts))
                questions.append(row)
    return questions

def group_questions_by_lesson(questions):
    """Nhóm câu hỏi theo bài học"""
    lessons = defaultdict(list)
    for q in questions:
        q_id = q['q_id']
        # Lấy mã bài từ q_id (vd: K6A1_01 -> A1)
        lesson_code = q_id.split('_')[0].replace('K6', '')
        lessons[lesson_code].append(q)
    return lessons

def create_html_template(lesson_code, lesson_title, questions):
    """Tạo nội dung HTML cho một bài học"""
    
    # Số câu hỏi thực tế
    total_questions = len(questions)
    num_quiz_questions = min(10, total_questions)
    
    # Hàm escape string cho JavaScript
    def js_escape(text):
        text = text.strip()
        # Escape các ký tự đặc biệt
        text = text.replace('\\', '\\\\')  # Backslash
        text = text.replace('"', '\\"')    # Double quote
        text = text.replace('\n', '\\n')   # Newline
        text = text.replace('\r', '\\r')   # Carriage return
        text = text.replace('\t', '\\t')   # Tab
        return text
    
    # Hàm thêm dấu "." vào cuối đáp án nếu chưa có
    def add_period(text):
        text = text.strip()
        if not text.endswith('.') and not text.endswith('?') and not text.endswith('!'):
            return text + '.'
        return text
    
    # Tạo chuỗi JavaScript array đơn giản (inline format)
    js_lines = []
    for q in questions:
        question_text = js_escape(q['question_text'])
        opt_a = js_escape(add_period(q['option_A']))
        opt_b = js_escape(add_period(q['option_B']))
        opt_c = js_escape(add_period(q['option_C']))
        opt_d = js_escape(add_period(q['option_D']))
        answer = ord(q['correct_option']) - ord('A')
        
        line = f'      {{question: "{question_text}", options: ["{opt_a}", "{opt_b}", "{opt_c}", "{opt_d}"], answer: {answer}}}'
        js_lines.append(line)
    
    js_array = '[\n' + ',\n'.join(js_lines) + '\n    ]'
    
    html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <title>⚡ K6-{lesson_code}: {lesson_title}</title>
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
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 6 - BÀI {lesson_code}</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">{lesson_title}</h1>
        <p class="text-gray-600 text-lg">🎯 {num_quiz_questions} câu hỏi{' (từ bộ ' + str(total_questions) + ' câu)' if total_questions > num_quiz_questions else ''} - Thời gian: ~{num_quiz_questions} phút</p>
      </div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl">
        <div class="flex items-center gap-3">
          <div class="text-3xl">📝</div>
          <div><div id="progress" class="text-gray-900 font-bold text-lg">Câu 1/{num_quiz_questions}</div><div class="text-sm text-gray-500">Chúc bạn làm bài tốt!</div></div>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex-1 w-48 h-3 rounded-full bg-gray-200 overflow-hidden"><div id="bar" class="h-full rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 transition-all" style="width:10%"></div></div>
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
    const QUIZ_ID="K6_{lesson_code}";
    const ENDPOINT="https://script.google.com/macros/s/AKfycbwj9IiX8PXC-bNsh4DGIw0uysx0v3jWPNeu0lQpieUIQAx9sT9YNUKTZoQFBjg-w86TKg/exec";
    function getStudent(){{try{{return JSON.parse(localStorage.getItem('student')||'null')}}catch(e){{return null}}}}
    const student=getStudent();
    (function(){{const pill=document.getElementById('userPill');if(student&&pill){{pill.classList.remove('hidden');pill.innerHTML=`👤 ${{student.name}} · Lớp ${{student.className}}`}}}})();
    
    const allQuestions={js_array};
    let currentQ=0,score=0,startTime=Date.now();
    function shuffle(arr){{for(let i=arr.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}}return arr}}
    function withShuffledOptions(q){{const order=q.options.map((_,i)=>i);shuffle(order);return{{...q,options:order.map(i=>q.options[i]),answer:order.indexOf(q.answer)}}}}
    const selectedQuestions = shuffle([...allQuestions]).slice(0, Math.min(10, allQuestions.length));
    const quiz=selectedQuestions.map(withShuffledOptions);
    
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
        const url=`${{ENDPOINT}}?student_name=${{encodeURIComponent(name)}}&class_name=${{encodeURIComponent(className)}}&quiz_id=${{quizId}}&score=${{score}}&total=${{total}}&duration=${{duration}}`;
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
    # Đường dẫn
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'Bai_tap_Tin_6')
    output_dir = os.path.join(base_dir, 'Web')
    
    # Đọc tất cả các file CSV
    csv_files = {
        'A': 'K6_question_A_full.csv',
        'B': 'K6_question_B_full.csv',
        'C': 'K6_question_C_full.csv',
        'D': 'K6_question_D_full.csv',
        'E': 'K6_question_E_full.csv',
        'F': 'K6_question_F_full.csv',
    }
    
    all_lessons = {}
    
    for theme, filename in csv_files.items():
        filepath = os.path.join(data_dir, filename)
        print(f"Reading {filename}...")
        questions = read_csv_file(filepath)
        lessons = group_questions_by_lesson(questions)
        all_lessons.update(lessons)
    
    print(f"\nTotal lessons: {len(all_lessons)}")
    print(f"Lessons: {sorted(all_lessons.keys())}")
    
    # Tạo file HTML cho từng bài
    for lesson_code in sorted(all_lessons.keys()):
        questions = all_lessons[lesson_code]
        lesson_title = LESSON_TITLES.get(lesson_code, lesson_code)
        
        print(f"\nCreating K6_{lesson_code}.html ({len(questions)} questions)...")
        
        html_content = create_html_template(lesson_code, lesson_title, questions)
        output_file = os.path.join(output_dir, f'K6_{lesson_code}.html')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  Done: {output_file}")
    
    print("\nCompleted! All HTML files created.")

if __name__ == '__main__':
    main()

