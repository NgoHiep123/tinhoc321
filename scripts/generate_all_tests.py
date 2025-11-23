#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tổng quát tạo tất cả các bài kiểm tra cho K7, K8, K9
"""

import csv
import os
import sys
import io
import random
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Định nghĩa cấu trúc bài kiểm tra cho mỗi khối
TEST_CONFIGS = {
    'K7': {
        'HK1': {
            1: {'lessons': ['A1', 'A2', 'A3'], 'description': '20 câu từ A1, A2, A3'},
            2: {'lessons': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'C1', 'C2', 'C3'], 'description': '20 câu từ A1-A6, C1-C3'},
            3: {'lessons': ['D1', 'D2'], 'description': '20 câu từ D1, D2'},
            4: {'lessons': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'C1', 'C2', 'C3', 'D1', 'D2', 'E1', 'E2'], 'description': '20 câu từ A1-A6, C1-C3, D1-D2, E1-E2'},
        },
        'HK2': {
            5: {'lessons': ['E7', 'E8'], 'description': '20 câu từ E7, E8'},
            6: {'lessons': ['E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12'], 'description': '20 câu từ E6-E12'},
            7: {'lessons': ['E13', 'E14', 'E15'], 'description': '20 câu từ E13-E15'},
            8: {'lessons': ['E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15'], 'description': '20 câu từ E6-E15'},
        },
    },
    'K8': {
        'HK1': {
            1: {'lessons': ['A1', 'A2', 'C1'], 'description': '20 câu từ A1, A2, C1'},
            2: {'lessons': ['A1', 'A2', 'C1', 'C2', 'C3', 'D1'], 'description': '20 câu từ A1, A2, C1-C3, D1'},
            3: {'lessons': ['F1-1', 'F1-2'], 'description': '20 câu từ F1-1, F1-2'},
            4: {'lessons': ['A1', 'A2', 'C1', 'C2', 'C3', 'D1', 'F1-1', 'F1-2', 'F1-3', 'F1-4', 'F1-5'], 'description': '20 câu từ A1, A2, C1-C3, D1, F1-1 đến F1-5'},
        },
        'HK2': {
            1: {'lessons': ['A1', 'A2', 'C1'], 'description': '20 câu từ A1, A2, C1'},
            5: {'lessons': ['E1-1', 'E1-2', 'E1-3'], 'description': '20 câu từ E1-1, E1-2, E1-3'},
            6: {'lessons': ['E1-1', 'E1-2', 'E1-3', 'E1-4', 'E1-5', 'E1-6'], 'description': '20 câu từ E1-1 đến E1-6'},
            7: {'lessons': ['E2-1', 'E2-2', 'E2-3'], 'description': '20 câu từ E2-1, E2-2, E2-3'},
            8: {'lessons': ['E1-1', 'E1-2', 'E1-3', 'E1-4', 'E1-5', 'E1-6', 'E2-1', 'E2-2', 'E2-3'], 'description': '20 câu từ E1-1 đến E1-6, E2-1 đến E2-3'},
        },
    },
    'K9': {
        'HK1': {
            1: {'lessons': ['B1', 'B2'], 'description': '20 câu từ Bài 1, 2'},
            2: {'lessons': ['B1', 'B2', 'B3', 'B4'], 'description': '20 câu từ Bài 1-4'},
            3: {'lessons': ['B5', 'B6A'], 'description': '20 câu từ Bài 5, 6A'},
            4: {'lessons': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6A', 'B7A'], 'description': '20 câu từ Bài 1-4, 5, 6A, 7A'},
        },
        'HK2': {
            5: {'lessons': ['B8A', 'B9A'], 'description': '20 câu từ Bài 8A, 9A'},
            6: {'lessons': ['B8A', 'B9A', 'B10A'], 'description': '20 câu từ Bài 8A, 9A, 10A'},
            7: {'lessons': ['B11', 'B12'], 'description': '20 câu từ Bài 11, 12'},
            8: {'lessons': ['B8A', 'B9A', 'B10A', 'B11', 'B12'], 'description': '20 câu từ Bài 8A-10A, 11-12'},
        },
    },
}

def read_csv_file(filepath, grade):
    """Đọc file CSV và trả về danh sách câu hỏi"""
    questions = []
    if not os.path.exists(filepath):
        return questions
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        
        if not lines:
            return questions
        
        # Xử lý header
        header_line = lines[0].strip()
        if header_line.startswith('"') and header_line.endswith('"'):
            header_line = header_line[1:-1]
        headers = [h.strip() for h in header_line.split(',')]
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= len(headers):
                parts = parts[:len(headers)]
                row_dict = dict(zip(headers, parts))
                
                q_id = row_dict.get('q_id', '')
                if q_id:
                    # Xử lý mã bài tùy theo khối
                    if grade == 'K7':
                        lesson_code = q_id.split('_')[0].replace('K7', '')
                        row_dict['lesson_code'] = lesson_code
                    elif grade == 'K8':
                        # Xử lý đặc biệt cho K8: K8A1_01 -> A1, K8E1_01 -> E1-1, K8F1_01 -> F1-1
                        code = q_id.split('_')[0].replace('K8', '')
                        if code.startswith('E1'):
                            if '_B2' in q_id:
                                code = 'E1-2'
                            elif '_B3' in q_id:
                                code = 'E1-3'
                            elif '_B4' in q_id:
                                code = 'E1-4'
                            elif '_B5' in q_id:
                                code = 'E1-5'
                            elif '_B6' in q_id:
                                code = 'E1-6'
                            else:
                                code = 'E1-1'
                        elif code.startswith('E2'):
                            if '_B6' in q_id:
                                code = 'E2-3'
                            elif '_B3' in q_id:
                                code = 'E2-2'
                            else:
                                code = 'E2-1'
                        elif code.startswith('F1'):
                            # F1 có các bài F1-1, F1-2, F1-3, F1-4, F1-5
                            # Dựa vào source để phân biệt
                            source = row_dict.get('source', '')
                            if 'Bài 1' in source or not '_B' in q_id:
                                code = 'F1-1'
                            elif '_B2' in q_id or 'Bài 2' in source:
                                code = 'F1-2'
                            elif '_B3' in q_id or 'Bài 3' in source:
                                code = 'F1-3'
                            elif '_B4' in q_id or 'Bài 4' in source:
                                code = 'F1-4'
                            elif '_B5' in q_id or 'Bài 5' in source:
                                code = 'F1-5'
                            else:
                                code = 'F1-1'
                        row_dict['lesson_code'] = code
                    elif grade == 'K9':
                        # K9B1_01 -> B1, K9B6A_01 -> B6A
                        code = q_id.split('_')[0].replace('K9', '')
                        row_dict['lesson_code'] = code
                    
                    questions.append(row_dict)
    
    return questions

def select_questions_for_test(all_questions, target_lessons, num_questions=20):
    """Chọn câu hỏi cho bài kiểm tra"""
    selected = []
    
    # Lọc câu hỏi theo các bài học yêu cầu
    filtered_questions = defaultdict(list)
    for q in all_questions:
        lesson = q.get('lesson_code', '')
        if lesson in target_lessons:
            filtered_questions[lesson].append(q)
    
    # Nếu không đủ bài học, bỏ qua
    available_lessons = [l for l in target_lessons if l in filtered_questions and len(filtered_questions[l]) > 0]
    
    if not available_lessons:
        return selected
    
    # Phân bổ đều số câu hỏi
    questions_per_lesson = num_questions // len(available_lessons)
    remainder = num_questions % len(available_lessons)
    
    for i, lesson in enumerate(available_lessons):
        count = questions_per_lesson + (1 if i < remainder else 0)
        questions = filtered_questions[lesson]
        if len(questions) >= count:
            selected.extend(random.sample(questions, count))
        else:
            selected.extend(questions)
    
    random.shuffle(selected)
    return selected[:num_questions]

def convert_question_to_js_format(q):
    """Chuyển câu hỏi sang format JS"""
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

def create_html_for_test(grade, semester, test_num, questions, config):
    """Tạo file HTML cho bài kiểm tra"""
    quiz_id = f"{grade}_KIEM_TRA_{test_num}"
    title = f"Kiểm tra {test_num} - Học kì {semester[-1]} ({', '.join(config['lessons'])})"
    description = config['description']
    
    num_questions = len(questions)
    icon_map = {1: '📝', 2: '📚', 3: '🌐', 4: '🎯', 5: '📝', 6: '📚', 7: '🌐', 8: '🎯'}
    icon = icon_map.get(test_num, '📝')
    
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
    
    # Template HTML (giống K6)
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
          <span class="text-sm font-bold text-purple-700">🎓 {grade} - HỌC KÌ {semester[-1]}</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">{icon} {title}</h1>
        <p class="text-gray-600 text-lg">🎯 {num_questions} câu hỏi - Thời gian: ~{num_questions} phút</p>
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
    
    output_file = os.path.join('.', f"{quiz_id}.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def generate_tests_for_grade(grade):
    """Tạo tất cả bài kiểm tra cho một khối"""
    print(f"\n{'='*60}")
    print(f"TẠO BÀI KIỂM TRA CHO {grade}")
    print(f"{'='*60}")
    
    # Đọc tất cả câu hỏi
    all_questions = []
    
    if grade == 'K7':
        csv_files = [
            'Bai_tap_Tin_7/K7_question_A_full.csv',
            'Bai_tap_Tin_7/K7_question_B_full.csv',
            'Bai_tap_Tin_7/K7_question_D_full.csv',
            'Bai_tap_Tin_7/K7_question_E_full.csv',
        ]
    elif grade == 'K8':
        csv_files = [
            'Bai_tap_Tin_8/K8_question_A_full.csv',
            'Bai_tap_Tin_8/K8_question_C_full.csv',
            'Bai_tap_Tin_8/K8_question_D_full.csv',
            'Bai_tap_Tin_8/K8_question_E1_full.csv',
            'Bai_tap_Tin_8/K8_question_E2_full.csv',
            'Bai_tap_Tin_8/K8_question_F_full.csv',
        ]
    elif grade == 'K9':
        csv_files = []
        for i in [1, 2, 3, 4, 5, '6A', '7A', '8A', '9A', '10A', 11, 12, 13, 14]:
            csv_file = f'Bai_tap_Tin_9/K9_question_Bai_{i}_full.csv'
            if os.path.exists(csv_file):
                csv_files.append(csv_file)
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            questions = read_csv_file(csv_file, grade)
            all_questions.extend(questions)
            print(f"  [OK] Đã đọc {len(questions)} câu hỏi từ {os.path.basename(csv_file)}")
    
    # Tạo bài kiểm tra
    configs = TEST_CONFIGS[grade]
    
    for semester in ['HK1', 'HK2']:
        print(f"\n  [{semester}]")
        semester_configs = configs.get(semester, {})
        
        for test_num, test_config in sorted(semester_configs.items()):
            target_lessons = test_config['lessons']
            selected_questions = select_questions_for_test(all_questions, target_lessons, 20)
            
            if selected_questions:
                output_file = create_html_for_test(grade, semester, test_num, selected_questions, test_config)
                print(f"    [OK] {grade}_KIEM_TRA_{test_num}.html ({len(selected_questions)} câu) - {', '.join(target_lessons[:3])}...")
            else:
                print(f"    [WARNING] {grade}_KIEM_TRA_{test_num}.html - Không tìm thấy câu hỏi cho {', '.join(target_lessons)}")

if __name__ == '__main__':
    for grade in ['K7', 'K8', 'K9']:
        generate_tests_for_grade(grade)
    
    print(f"\n{'='*60}")
    print("HOÀN THÀNH!")
    print(f"{'='*60}")

