#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo lại HTML cho chủ đề E của khối 8 (E1 và E2)
E1: E1-1 đến E1-6
E2: E2-1 đến E2-3
"""

import csv
import os
import sys
import io
import json
import re
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Template HTML (giống K8)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <title>⚡ {quiz_id}: {emoji} {title}</title>
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
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 8 - BÀI {badge}</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">{emoji} {title}</h1>
        <p class="text-gray-600 text-lg">🎯 {num_questions} câu hỏi - Thời gian: ~{num_questions} phút</p>
      </div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl">
        <div class="flex items-center gap-3">
          <div class="text-3xl">📝</div>
          <div><div id="progress" class="text-gray-900 font-bold text-lg">Câu 1/{num_questions}</div><div class="text-sm text-gray-500">Chúc bạn làm bài tốt!</div></div>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex-1 w-48 h-3 rounded-full bg-gray-200 overflow-hidden"><div id="bar" class="h-full rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 transition-all" style="width:{progress_width}%"></div></div>
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
    
    const allQuestions={questions_json};
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
</html>
"""

def read_csv_file(filepath):
    """Đọc file CSV và nhóm theo bài con"""
    questions_by_lesson = defaultdict(list)
    
    if not os.path.exists(filepath):
        print(f"[WARNING] Không tìm thấy file: {filepath}")
        return questions_by_lesson
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q_id = row.get('q_id', '')
            if not q_id:
                continue
            
            # Phân tích mã bài: K8E1_01 -> E1-1, K8E1_B2_01 -> E1-2, K8E1_B3 -> E1-3
            # K8E2_01 -> E2-1, K8E2_B3_01 -> E2-2, K8E2_B6_01 -> E2-3
            lesson_code = None
            
            if q_id.startswith('K8E1'):
                # E1: K8E1_01 -> E1-1, K8E1_B2 -> E1-2, K8E1_B3 -> E1-3, K8E1_B4 -> E1-4, K8E1_B5 -> E1-5, K8E1_B6 -> E1-6
                if '_B2' in q_id:
                    lesson_code = 'E1-2'
                elif '_B3' in q_id:
                    lesson_code = 'E1-3'
                elif '_B4' in q_id:
                    lesson_code = 'E1-4'
                elif '_B5' in q_id:
                    lesson_code = 'E1-5'
                elif '_B6' in q_id:
                    lesson_code = 'E1-6'
                else:
                    lesson_code = 'E1-1'
            elif q_id.startswith('K8E2'):
                # E2: K8E2_01 -> E2-1, K8E2_B3_01 -> E2-2, K8E2_B6_01 -> E2-3
                if '_B6' in q_id:
                    lesson_code = 'E2-3'
                elif '_B3' in q_id:
                    lesson_code = 'E2-2'
                else:
                    lesson_code = 'E2-1'
            
            if lesson_code:
                row['lesson_code'] = lesson_code
                questions_by_lesson[lesson_code].append(row)
    
    return questions_by_lesson

def get_topic_info(lesson_code):
    """Lấy thông tin về bài học"""
    topic_names = {
        'E1-1': ('Xử lý bảng tính', '📊'),
        'E1-2': ('Sắp xếp dữ liệu', '🔀'),
        'E1-3': ('Biểu đồ', '📈'),
        'E1-4': ('Lọc dữ liệu nâng cao', '🔍'),
        'E1-5': ('Hàm và công thức', '🧮'),
        'E1-6': ('Thực hành tổng hợp', '✅'),
        'E2-1': ('Soạn thảo nâng cao - Hình ảnh', '🖼️'),
        'E2-2': ('Soạn thảo nâng cao - Danh sách', '📋'),
        'E2-3': ('Thực hành phân cấp', '📑'),
    }
    
    name, emoji = topic_names.get(lesson_code, (f'Bài {lesson_code}', '📖'))
    return name, emoji

def convert_question_to_json(q):
    """Chuyển câu hỏi sang format JSON"""
    def js_escape(text):
        if not text:
            return ""
        text = str(text).strip()
        text = text.replace('\\', '\\\\')
        text = text.replace('"', '\\"')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\r')
        return text
    
    question_text = js_escape(q.get('question_text', ''))
    opt_a = js_escape(q.get('option_A', ''))
    opt_b = js_escape(q.get('option_B', ''))
    opt_c = js_escape(q.get('option_C', ''))
    opt_d = js_escape(q.get('option_D', ''))
    
    correct_option = q.get('correct_option', 'A').strip()
    answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'A.': 0, 'B.': 1, 'C.': 2, 'D.': 3}
    answer = answer_map.get(correct_option, 0)
    
    return {
        'question': question_text,
        'options': [opt_a, opt_b, opt_c, opt_d],
        'answer': answer
    }

def generate_html_for_lesson(lesson_code, questions, output_dir='.'):
    """Tạo file HTML cho một bài học"""
    title, emoji = get_topic_info(lesson_code)
    quiz_id = f"K8_{lesson_code.replace('-', '_')}"
    badge = lesson_code
    
    json_questions = [convert_question_to_json(q) for q in questions]
    questions_json = json.dumps(json_questions, ensure_ascii=False)
    
    num_questions = len(json_questions)
    progress_width = round(100 / num_questions) if num_questions > 0 else 8
    
    html_content = HTML_TEMPLATE.format(
        quiz_id=quiz_id,
        title=title,
        emoji=emoji,
        badge=badge,
        num_questions=num_questions,
        progress_width=progress_width,
        questions_json=questions_json
    )
    
    output_file = os.path.join(output_dir, f"{quiz_id}.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    print("=" * 60)
    print("TẠO LẠI HTML CHO CHỦ ĐỀ E - KHỐI 8")
    print("=" * 60)
    
    output_dir = '.'
    
    # Xử lý E1
    print("\n[ĐANG XỬ LÝ] K8_question_E1_full.csv...")
    e1_path = 'Bai_tap_Tin_8/K8_question_E1_full.csv'
    e1_lessons = read_csv_file(e1_path)
    print(f"  - Tìm thấy {len(e1_lessons)} bài học")
    
    for lesson_code, questions in sorted(e1_lessons.items()):
        if questions:
            output_file = generate_html_for_lesson(lesson_code, questions, output_dir)
            print(f"  [OK] Đã tạo: {os.path.basename(output_file)} ({len(questions)} câu)")
    
    # Xử lý E2
    print("\n[ĐANG XỬ LÝ] K8_question_E2_full.csv...")
    e2_path = 'Bai_tap_Tin_8/K8_question_E2_full.csv'
    e2_lessons = read_csv_file(e2_path)
    print(f"  - Tìm thấy {len(e2_lessons)} bài học")
    
    for lesson_code, questions in sorted(e2_lessons.items()):
        if questions:
            output_file = generate_html_for_lesson(lesson_code, questions, output_dir)
            print(f"  [OK] Đã tạo: {os.path.basename(output_file)} ({len(questions)} câu)")
    
    print("\n" + "=" * 60)
    print("HOÀN THÀNH!")
    print("=" * 60)

if __name__ == '__main__':
    main()

