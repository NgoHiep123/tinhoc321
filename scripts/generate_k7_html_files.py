#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động tạo file HTML cho các bài Khối 7 từ CSV
"""

import csv
import os
from collections import defaultdict

# Template HTML cơ bản
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <title>⚡ {quiz_id_title}: {emoji} {title}</title>
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
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 7 - BÀI {badge}</span>
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
</html>
"""

def get_topic_emoji(topic_id):
    """Lấy emoji phù hợp cho từng chủ đề"""
    emoji_map = {
        'E1': '📊', 'E2': '📑', 'E3': '🔢', 'E4': '🎨', 'E5': '🧮',
        'E6': '🔍', 'E7': '📈', 'E8': '📝', 'E9': '❓', 'E10': '🔢',
        'E11': '📍', 'E12': '🔧', 'E13': '🎨', 'E14': '🔒', 'E15': '✅',
        'F1': '🎯', 'F2': '💻', 'F3': '🔨', 'F4': '🚀', 'F5': '📚',
        'F6': '🌟', 'F7': '🎭', 'F8': '🎪'
    }
    for key in emoji_map:
        if topic_id.startswith(key):
            return emoji_map[key]
    return '📖'

def parse_csv_questions(csv_file):
    """Đọc câu hỏi từ file CSV và nhóm theo bài"""
    questions_by_topic = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Bỏ dòng header
        for line in lines[1:]:
            line = line.strip()
            if not line or line == '':
                continue
            
            # Bỏ dấu ngoặc kép đầu cuối
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            
            # Split bằng dấu phẩy
            parts = line.split(',')
            if len(parts) < 10:
                continue
                
            q_id = parts[0]
            question_text = parts[2]
            option_A = parts[3]
            option_B = parts[4]
            option_C = parts[5]
            option_D = parts[6]
            correct_option = parts[7].strip()
            
            # Lấy topic từ q_id (vd: K7E1_01 => E1)
            topic = q_id.split('_')[0][2:]  # K7E1 => E1
            
            # Xác định đáp án đúng (A=0, B=1, C=2, D=3)
            correct_map = {'A.': 0, 'B.': 1, 'C.': 2, 'D.': 3, 
                          'A': 0, 'B': 1, 'C': 2, 'D': 3}
            answer_index = correct_map.get(correct_option, 0)
            
            question = {
                'question': question_text,
                'options': [option_A, option_B, option_C, option_D],
                'answer': answer_index
            }
            
            questions_by_topic[topic].append(question)
    
    return questions_by_topic

def generate_html_files(csv_file, output_dir):
    """Tạo file HTML cho tất cả các bài"""
    questions_by_topic = parse_csv_questions(csv_file)
    
    # Map tên bài
    topic_names = {
        'E1': 'Làm quen bảng tính',
        'E2': 'Trang tính và thành phần',
        'E3': 'Hộp tên khối ô và sao chép',
        'E4': 'Định dạng bảng tính',
        'E5': 'Công thức và hàm',
        'E6': 'Sắp xếp và lọc',
        'E7': 'Biểu đồ',
        'E8': 'Thực hành báo cáo',
        'E9': 'Hàm IF',
        'E10': 'Đếm và tính theo điều kiện',
        'E11': 'Địa chỉ tương đối tuyệt đối',
        'E12': 'Sắp xếp lọc nâng cao',
        'E13': 'Định dạng có điều kiện',
        'E14': 'Bảo vệ chia sẻ',
        'E15': 'Thực hành tổng hợp',
        'F1': 'Giới thiệu Scratch',
        'F2': 'Lập trình cơ bản',
        'F3': 'Điều khiển và lặp',
        'F4': 'Biến và toán tử',
        'F5': 'Dự án Scratch',
        'F6': 'Thuật toán',
        'F7': 'Cấu trúc rẽ nhánh',
        'F8': 'Tổng hợp'
    }
    
    os.makedirs(output_dir, exist_ok=True)
    
    for topic, questions in sorted(questions_by_topic.items()):
        if not questions:
            continue
            
        num_questions = len(questions)
        progress_width = round(100 / num_questions) if num_questions > 0 else 8
        
        # Tạo JSON cho questions
        import json
        questions_json = json.dumps(questions, ensure_ascii=False)
        
        quiz_id = f"K7_{topic}"
        title = topic_names.get(topic, f"Bài {topic}")
        emoji = get_topic_emoji(topic)
        badge = topic
        quiz_id_title = quiz_id.replace('_', '-')
        
        html_content = HTML_TEMPLATE.format(
            quiz_id=quiz_id,
            quiz_id_title=quiz_id_title,
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
        
        print(f"[OK] Da tao {output_file}")

if __name__ == "__main__":
    output_dir = "Web"
    
    # Tạo file HTML cho chủ đề E
    print("[START] Bat dau tao file HTML cho chu de E...")
    csv_e = "Bai_tap_Tin_7/K7_question_E_full.csv"
    generate_html_files(csv_e, output_dir)
    print("[OK] Hoan thanh chu de E!")
    
    # Tạo file HTML cho chủ đề F
    print("\n[START] Bat dau tao file HTML cho chu de F...")
    csv_f = "Bai_tap_Tin_7/K7_question_F_full.csv"
    generate_html_files(csv_f, output_dir)
    print("[OK] Hoan thanh chu de F!")
    
    print("\n[DONE] Hoan thanh tat ca!")

