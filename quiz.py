import tkinter as tk
from tkinter import messagebox
import random

# Hàm đọc file câu hỏi từ file txt với định dạng mới
def read_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Chia câu hỏi, lựa chọn và đáp án bằng dấu |
            parts = line.strip().split(" | ")
            if len(parts) == 6:  # Đảm bảo có đủ các phần (1 câu hỏi + 4 lựa chọn + 1 đáp án đúng)
                question = parts[0]
                options = parts[1:5]
                correct_answer = parts[5].strip()  # Đảm bảo đáp án không có khoảng trắng
                questions.append((question, options, correct_answer))
    return questions

# Hàm đảo thứ tự câu hỏi ngẫu nhiên
def shuffle_questions(questions):
    random.shuffle(questions)
    return questions

# Hàm kiểm tra câu trả lời
def check_answer():
    global current_question_index, score
    
    selected_option = radio_var.get().strip()  # Lấy câu trả lời người dùng chọn, bỏ khoảng trắng
    correct_answer = current_correct_answer.strip()  # Lấy đáp án đúng, bỏ khoảng trắng
    
    if selected_option.lower() == correct_answer.lower():  # So sánh không phân biệt chữ hoa/thường
        score += 1
        result_label.config(text="Correct! Your score: " + str(score), fg="green")
    else:
        result_label.config(text=f"Wrong! The correct answer is: {current_correct_answer}", fg="red")
    
    # Cập nhật điểm số hiển thị
    score_label.config(text=f"Score: {score}")
    
    current_question_index += 1
    if current_question_index < len(questions):
        root.after(2000, load_question)  # Tự động tải câu hỏi tiếp theo sau 2 giây
    else:
        show_result()  # Nếu không còn câu hỏi, hiển thị kết quả cuối cùng

# Hàm hiển thị kết quả cuối cùng
def show_result():
    messagebox.showinfo("Result", f"Your final score is {score}/{len(questions)}")
    root.quit()

# Hàm tải câu hỏi tiếp theo và xáo trộn các câu trả lời
def load_question():
    global current_correct_answer
    
    if current_question_index < len(questions):
        question, options, correct_answer = questions[current_question_index]
        current_correct_answer = correct_answer
        
        question_label.config(text=question)
        
        # Xáo trộn câu trả lời
        random.shuffle(options)
        
        for idx, option in enumerate(options):
            radio_buttons[idx].config(text=option.strip(), value=option.strip())  # Bỏ khoảng trắng thừa
        
        radio_var.set(None)  # Reset lại lựa chọn
        result_label.config(text="")  # Reset kết quả trước đó
    else:
        show_result()  # Hiển thị kết quả cuối cùng nếu hết câu hỏi

# Đọc câu hỏi từ file
questions = read_questions_from_file('question.txt')

# Đảo thứ tự câu hỏi ngẫu nhiên
questions = shuffle_questions(questions)

# Biến toàn cục cho chỉ số câu hỏi, đáp án đúng và điểm số
current_question_index = 0
score = 0
current_correct_answer = ""

# Tạo cửa sổ giao diện Tkinter
root = tk.Tk()
root.title("Quiz Application - Requirements Analysis and Design")
root.geometry("800x500")
root.configure(bg='#f0f0f0')  # Background màu sáng

# Tùy chỉnh font chữ cho các nhãn và nút
font_style = ('Cambria', 16)
font_answer = ('Cambria', 14)

button_font_style = ('Cambria', 14, 'bold')

# Hiển thị câu hỏi
question_label = tk.Label(root, text="", wraplength=500, font=font_style, bg='#f0f0f0', fg='#333')
question_label.pack(pady=20)

# Hiển thị điểm số liên tục
score_label = tk.Label(root, text=f"Score: {score}", font=('Cambria', 12, 'bold'), bg='#f0f0f0', fg='#000')
score_label.pack(pady=5)

# Tạo các lựa chọn cho câu trả lời (Radio buttons)
radio_var = tk.StringVar()
radio_buttons = []
for i in range(4):
    rb = tk.Radiobutton(root, text="", variable=radio_var, value="", font=font_answer, bg='#f0f0f0', fg='#333', activebackground='#ddd', activeforeground='#000')
    rb.pack(anchor="w", padx=10, pady=5)  # Thêm pady để tạo khoảng cách dọc giữa các nút
    radio_buttons.append(rb)

submit_button = tk.Button(root, text="Submit", command=check_answer, font=button_font_style, bg='#4CAF50', fg='white', relief="raised", borderwidth=5, highlightthickness=2, highlightbackground="#333")
submit_button.pack(pady=20)


# Hiển thị kết quả mỗi câu hỏi (đúng hay sai)
result_label = tk.Label(root, text="", font=font_style, bg='#f0f0f0', fg='#333')
result_label.pack(pady=10)

# Tải câu hỏi đầu tiên
load_question()

# Bắt đầu vòng lặp ứng dụng
root.mainloop()
