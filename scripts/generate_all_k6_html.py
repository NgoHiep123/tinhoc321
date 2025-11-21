"""
Script tạo tất cả file HTML cho Tin học 6 (Chủ đề A-F)
"""

import csv
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Metadata tất cả các bài
ALL_LESSONS = {
    # Chủ đề A
    'K6A1': {'id': 'A1', 'name': 'Máy tính và ứng dụng', 'icon': '💻', 'topic': 'A'},
    'K6A2': {'id': 'A2', 'name': 'Hệ điều hành và PM ứng dụng', 'icon': '💾', 'topic': 'A'},
    'K6A3': {'id': 'A3', 'name': 'Tệp và thư mục', 'icon': '📁', 'topic': 'A'},
    'K6A4': {'id': 'A4', 'name': 'Mạng máy tính và Internet', 'icon': '🌐', 'topic': 'A'},
    'K6A5': {'id': 'A5', 'name': 'An toàn thông tin', 'icon': '🔐', 'topic': 'A'},
    'K6A6': {'id': 'A6', 'name': 'Thao tác cơ bản', 'icon': '⌨️', 'topic': 'A'},
    # Chủ đề B
    'K6B1': {'id': 'B1', 'name': 'Làm quen Microsoft Word', 'icon': '📝', 'topic': 'B'},
    'K6B2': {'id': 'B2', 'name': 'Định dạng văn bản', 'icon': '🎨', 'topic': 'B'},
    'K6B3': {'id': 'B3', 'name': 'Căn lề và đoạn văn', 'icon': '📄', 'topic': 'B'},
    'K6B4': {'id': 'B4', 'name': 'Chèn hình ảnh và bảng', 'icon': '🖼️', 'topic': 'B'},
    'K6B5': {'id': 'B5', 'name': 'Thiết lập trang và in ấn', 'icon': '🖨️', 'topic': 'B'},
    'K6B6': {'id': 'B6', 'name': 'Thực hành Word nâng cao', 'icon': '⚡', 'topic': 'B'},
    # Chủ đề C
    'K6C1': {'id': 'C1', 'name': 'Làm quen Microsoft Excel', 'icon': '📊', 'topic': 'C'},
    'K6C2': {'id': 'C2', 'name': 'Công thức và hàm', 'icon': '🧮', 'topic': 'C'},
    'K6C3': {'id': 'C3', 'name': 'Biểu đồ trong Excel', 'icon': '📈', 'topic': 'C'},
    'K6C4': {'id': 'C4', 'name': 'Sắp xếp và lọc dữ liệu', 'icon': '🔍', 'topic': 'C'},
    # Chủ đề D
    'K6D1': {'id': 'D1', 'name': 'Làm quen PowerPoint', 'icon': '🎬', 'topic': 'D'},
    'K6D2': {'id': 'D2', 'name': 'Thiết kế slide đẹp', 'icon': '🎨', 'topic': 'D'},
    'K6D3': {'id': 'D3', 'name': 'Animation và Transition', 'icon': '✨', 'topic': 'D'},
    # Chủ đề E
    'K6E1': {'id': 'E1', 'name': 'Thuật toán cơ bản', 'icon': '🧩', 'topic': 'E'},
    'K6E2': {'id': 'E2', 'name': 'Làm quen Scratch', 'icon': '🐱', 'topic': 'E'},
    'K6E3': {'id': 'E3', 'name': 'Sự kiện trong Scratch', 'icon': '⚡', 'topic': 'E'},
    'K6E4': {'id': 'E4', 'name': 'Vòng lặp', 'icon': '🔁', 'topic': 'E'},
    'K6E5': {'id': 'E5', 'name': 'Câu lệnh điều kiện', 'icon': '🔀', 'topic': 'E'},
    'K6E6': {'id': 'E6', 'name': 'Biến và dự án game', 'icon': '🎮', 'topic': 'E'},
    # Chủ đề F
    'K6F1': {'id': 'F1', 'name': 'Lập kế hoạch dự án', 'icon': '📋', 'topic': 'F'},
    'K6F2': {'id': 'F2', 'name': 'Thuyết trình dự án', 'icon': '🎤', 'topic': 'F'}
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <title>⚡ K6-{lesson_id}: {lesson_name}</title>
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
          <span class="text-sm font-bold text-purple-700">🎓 KHỐI 6 - BÀI {lesson_id}</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-gray-900 mb-2">{icon} {lesson_name}</h1>
        <p class="text-gray-600 text-lg">🎯 10 câu hỏi - Thời gian: ~10 phút</p>
      </div>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl">
        <div class="flex items-center gap-3">
          <div class="text-3xl">📝</div>
          <div><div id="progress" class="text-gray-900 font-bold text-lg">Câu 1/10</div><div class="text-sm text-gray-500">Chúc bạn làm bài tốt!</div></div>
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
    const QUIZ_ID="K6_{lesson_id}";
    const ENDPOINT="https://script.google.com/macros/s/AKfycbwj9IiX8PXC-bNsh4DGIw0uysx0v3jWPNeu0lQpieUIQAx9sT9YNUKTZoQFBjg-w86TKg/exec";
    function getStudent(){{try{{return JSON.parse(localStorage.getItem('student')||'null')}}catch(e){{return null}}}}
    const student=getStudent();
    (function(){{const pill=document.getElementById('userPill');if(student&&pill){{pill.classList.remove('hidden');pill.innerHTML=`👤 ${{student.name}} · Lớp ${{student.className}}`}}}})();
    const quizData={quiz_data};
    let currentQ=0,score=0,startTime=Date.now();
    function shuffle(arr){{for(let i=arr.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]]}}return arr}}
    function withShuffledOptions(q){{const order=q.options.map((_,i)=>i);shuffle(order);return{{...q,options:order.map(i=>q.options[i]),answer:order.indexOf(q.answer)}}}}
    const quiz=quizData.map(withShuffledOptions);
    function showQuestion(){{const q=quiz[currentQ];document.getElementById('question-text').textContent=q.question;document.getElementById('progress').innerHTML=`Câu ${{currentQ+1}}/10`;document.getElementById('bar').style.width=((currentQ+1)/10*100)+'%';const container=document.getElementById('options-container');container.innerHTML='';const letters=['A','B','C','D'];q.options.forEach((opt,i)=>{{const btn=document.createElement('button');btn.className='option-btn w-full text-left px-6 py-4 rounded-xl border-2 border-gray-200 hover:border-purple-400 bg-white font-semibold text-gray-800 text-lg';btn.innerHTML=`<span class="inline-block w-8 h-8 rounded-full bg-purple-100 text-purple-700 font-bold mr-3 text-center leading-8">${{letters[i]}}</span>${{opt}}`;btn.onclick=()=>checkAnswer(i,btn);container.appendChild(btn)}});document.getElementById('next-btn').classList.add('hidden');document.getElementById('feedback-text').textContent=''}}
    function checkAnswer(chosen,btn){{const q=quiz[currentQ];const allBtns=document.querySelectorAll('.option-btn');allBtns.forEach(b=>b.disabled=true);if(chosen===q.answer){{btn.classList.add('correct');score++;document.getElementById('score').innerHTML=`🏆 ${{score}}`;document.getElementById('feedback-text').innerHTML='✅ <span style="color:#10b981">Chính xác!</span>';confetti({{particleCount:50,spread:60,origin:{{y:0.6}}}})}}else{{btn.classList.add('incorrect');allBtns[q.answer].classList.add('correct');document.getElementById('feedback-text').innerHTML='❌ <span style="color:#ef4444">Chưa đúng!</span>'}}document.getElementById('next-btn').classList.remove('hidden')}}
    document.getElementById('next-btn').onclick=()=>{{currentQ++;if(currentQ<quiz.length)showQuestion();else showResults()}};
    function showResults(){{document.querySelector('#quiz-container>div:first-child').classList.add('hidden');document.getElementById('options-container').classList.add('hidden');document.getElementById('next-btn').classList.add('hidden');document.getElementById('feedback-container').classList.add('hidden');document.getElementById('results-container').classList.remove('hidden');const pct=(score/quiz.length*100).toFixed(0);document.getElementById('final-score').textContent=`${{score}}/10 (${{pct}}%)`;let comment,emoji;if(pct>=90){{comment="🌟 Xuất sắc!";emoji="🎉"}}else if(pct>=70){{comment="👍 Rất tốt!";emoji="😊"}}else if(pct>=50){{comment="💪 Khá tốt!";emoji="😃"}}else{{comment="📖 Cố gắng hơn nhé!";emoji="😅"}}document.getElementById('score-comment').textContent=comment;document.getElementById('result-emoji').textContent=emoji;if(pct>=70){{const duration=3000,end=Date.now()+duration;(function frame(){{confetti({{particleCount:3,angle:60,spread:55,origin:{{x:0}}}});confetti({{particleCount:3,angle:120,spread:55,origin:{{x:1}}}});if(Date.now()<end)requestAnimationFrame(frame)}}())}}const duration=Math.floor((Date.now()-startTime)/1000);if(student){{sendResult(student.name,student.className,QUIZ_ID,score,quiz.length,duration)}}else{{document.getElementById('send-status').textContent='Chưa đăng nhập'}}}}
    async function sendResult(name,className,quizId,score,total,duration){{try{{const url=`${{ENDPOINT}}?student_name=${{encodeURIComponent(name)}}&class_name=${{encodeURIComponent(className)}}&quiz_id=${{quizId}}&score=${{score}}&total=${{total}}&duration=${{duration}}`;await fetch(url,{{mode:'no-cors'}});document.getElementById('send-status').textContent='✅ Đã lưu!'}}catch(e){{document.getElementById('send-status').textContent='⚠️ Không lưu được'}}}}
    document.getElementById('restart-btn').onclick=()=>location.reload();
    showQuestion();
  </script>
</body>
</html>
"""

def read_all_questions():
    """Đọc tất cả câu hỏi từ các file CSV"""
    csv_files = [
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_A.csv',
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_B.csv',
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_C.csv',
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_D.csv',
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_E.csv',
        '../Bai_tap_Tin_6/question_bank_K6_ChuDe_F.csv'
    ]
    
    all_questions = {}
    
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            print(f"[SKIP] Khong tim thay: {csv_file}")
            continue
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lesson_key = row['q_id'][:4]  # K6A1, K6B1, etc.
                
                if lesson_key not in all_questions:
                    all_questions[lesson_key] = []
                
                all_questions[lesson_key].append({
                    'question': row['question_text'],
                    'options': [
                        row['option_A'],
                        row['option_B'],
                        row['option_C'],
                        row['option_D']
                    ],
                    'answer': ord(row['correct_option']) - ord('A')
                })
    
    return all_questions

def generate_all_html():
    """Tạo tất cả file HTML"""
    print("=" * 60)
    print("TAO FILE HTML CHO TIN HOC 6")
    print("=" * 60)
    
    # Đọc câu hỏi
    print("\n[1] Dang doc cau hoi...")
    all_questions = read_all_questions()
    print(f"[OK] Da doc {len(all_questions)} bai")
    
    # Tạo HTML
    print("\n[2] Dang tao file HTML...")
    created = []
    
    for lesson_key, questions in sorted(all_questions.items()):
        if lesson_key not in ALL_LESSONS:
            continue
        
        metadata = ALL_LESSONS[lesson_key]
        
        # Convert to JSON
        quiz_json = '[\n'
        for i, q in enumerate(questions):
            quiz_json += '      {question: "' + q['question'].replace('"', '\\"') + '", '
            quiz_json += 'options: ' + str(q['options']).replace("'", '"') + ', '
            quiz_json += 'answer: ' + str(q['answer']) + '}'
            if i < len(questions) - 1:
                quiz_json += ','
            quiz_json += '\n'
        quiz_json += '    ]'
        
        # Generate HTML
        html = HTML_TEMPLATE.format(
            lesson_id=metadata['id'],
            lesson_name=metadata['name'],
            icon=metadata['icon'],
            quiz_data=quiz_json
        )
        
        # Save
        output = f'../Web/K6_{metadata["id"]}.html'
        with open(output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        created.append((metadata['topic'], metadata['id'], metadata['name'], len(questions)))
        print(f"[OK] K6_{metadata['id']}.html - {len(questions)} cau")
    
    # Summary
    print("\n" + "=" * 60)
    print("HOAN THANH!")
    print("=" * 60)
    
    by_topic = {}
    for topic, lid, name, count in created:
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append((lid, name, count))
    
    total_questions = sum(c for _, _, _, c in created)
    
    print(f"\nTong ket:")
    print(f"  - Tong so bai: {len(created)}")
    print(f"  - Tong so cau hoi: {total_questions}")
    
    print(f"\nChi tiet theo chu de:")
    for topic in sorted(by_topic.keys()):
        lessons = by_topic[topic]
        topic_total = sum(c for _, _, c in lessons)
        print(f"\n  Chu de {topic}: {len(lessons)} bai, {topic_total} cau")
        for lid, name, count in lessons:
            print(f"    - Bai {lid}: {name} ({count} cau)")
    
    print(f"\n[NEXT] Buoc tiep theo:")
    print(f"  1. Mo Web/index.html de test")
    print(f"  2. Dang nhap Khoi 6 va lam thu")
    print(f"  3. Cap nhat index.html voi cac link moi")

def main():
    generate_all_html()

if __name__ == '__main__':
    main()

