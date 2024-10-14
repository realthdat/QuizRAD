import tkinter as tk
from tkinter import messagebox, filedialog
import random

# Hàm đọc file câu hỏi từ file txt với định dạng mới
def read_questions_from_file(file_path):
    questions = []
    try:
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
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} không tồn tại.")
        return None

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
        root.after(2000, next_question)  # Tự động chuyển câu sau 2 giây nếu đúng
    else:
        result_label.config(text=f"Wrong! The correct answer is: {current_correct_answer}", fg="red")
        next_button.config(state="normal")  # Kích hoạt nút "Next" khi trả lời sai
        submit_button.config(state="disabled")  # Vô hiệu hóa nút "Submit" khi trả lời sai
    
    # Cập nhật điểm số hiển thị
    score_label.config(text=f"Score: {score}")

# Hàm hiển thị kết quả cuối cùng và cho phép chọn bài kiểm tra khác
def show_result():
    messagebox.showinfo("Result", f"Your final score is {score}/{len(questions)}")
    
    # Hiển thị nút "Chọn bài kiểm tra khác" để người dùng chọn lại bài kiểm tra
    choose_file_button.config(state="normal")  # Kích hoạt nút chọn file để chọn bài kiểm tra khác
    result_label.config(text="Quiz finished. Please choose another test.")
    next_button.config(state="disabled")  # Vô hiệu hóa nút "Next"
    submit_button.config(state="disabled")  # Vô hiệu hóa nút "Submit"

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

        # Vô hiệu hóa nút "Next" và kích hoạt lại nút "Submit"
        next_button.config(state="disabled")
        submit_button.config(state="disabled")
    else:
        show_result()  # Hiển thị kết quả cuối cùng nếu hết câu hỏi

# Hàm xử lý khi bấm nút "Next"
def next_question():
    global current_question_index
    current_question_index += 1
    load_question()

# Hàm để kiểm tra xem đã chọn đáp án chưa và kích hoạt nút Submit
def on_option_selected(*args):
    if radio_var.get():  # Nếu có một lựa chọn nào được chọn
        submit_button.config(state="normal")  # Kích hoạt nút Submit
    else:
        submit_button.config(state="disabled")  # Vô hiệu hóa nút Submit

# Hàm chọn file câu hỏi mới và reset trạng thái
def choose_file():
    file_path = filedialog.askopenfilename(title="Select a Quiz File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    
    if file_path:
        global questions, current_question_index, score
        questions = read_questions_from_file(file_path)
        
        if questions:  # Chỉ bắt đầu nếu file được đọc thành công
            questions = shuffle_questions(questions)
            current_question_index = 0
            score = 0
            score_label.config(text=f"Score: {score}")
            load_question()

            # Vô hiệu hóa nút "Chọn bài kiểm tra khác" trong khi người dùng đang làm bài kiểm tra
            choose_file_button.config(state="disabled")

# Biến toàn cục cho chỉ số câu hỏi, đáp án đúng và điểm số
current_question_index = 0
score = 0
current_correct_answer = ""

# Tạo cửa sổ giao diện Tkinter
root = tk.Tk()
root.title("Quiz Application - Requirements Analysis and Design")
root.geometry("900x600")
root.configure(bg='#f0f0f0')  # Background màu sáng

# Tùy chỉnh font chữ cho các nhãn và nút
font_style = ('Cambria', 16)
font_answer = ('Cambria', 14)

button_font_style = ('Cambria', 14, 'bold')

# Nút chọn file
choose_file_button = tk.Button(root, text="Choose Quiz File", command=choose_file, font=button_font_style, bg='#4CAF50', fg='white', relief="raised", borderwidth=5, highlightthickness=2, highlightbackground="#333")
choose_file_button.pack(pady=20)

# Hiển thị câu hỏi
question_label = tk.Label(root, text="", wraplength=500, font=font_style, bg='#f0f0f0', fg='#333')
question_label.pack(pady=20)

# Hiển thị điểm số liên tục
score_label = tk.Label(root, text=f"Score: {score}", font=('Cambria', 12, 'bold'), bg='#f0f0f0', fg='#000')
score_label.pack(pady=5)

# Tạo các lựa chọn cho câu trả lời (Radio buttons)
radio_var = tk.StringVar()
radio_var.trace("w", on_option_selected)  # Theo dõi thay đổi của radio_var để gọi hàm on_option_selected
radio_buttons = []
for i in range(4):
    rb = tk.Radiobutton(root, text="", variable=radio_var, value="", font=font_answer, bg='#f0f0f0', fg='#333', activebackground='#ddd', activeforeground='#000')
    rb.pack(anchor="w", padx=10, pady=5)  # Thêm pady để tạo khoảng cách dọc giữa các nút
    radio_buttons.append(rb)

# Frame để chứa hai nút Submit và Next
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=20)

submit_button = tk.Button(button_frame, text="Submit", command=check_answer, font=button_font_style, bg='#4CAF50', fg='white', relief="raised", borderwidth=5, highlightthickness=2, highlightbackground="#333", state="disabled")
submit_button.grid(row=0, column=0, padx=20)

# Nút Next để chuyển sang câu hỏi tiếp theo
next_button = tk.Button(button_frame, text="Next", command=next_question, font=button_font_style, bg='#f0f0f0', fg='black', relief="raised", borderwidth=5, highlightthickness=2, highlightbackground="#333", state="disabled")
next_button.grid(row=0, column=1, padx=20)

# Hiển thị kết quả mỗi câu hỏi (đúng hay sai)
result_label = tk.Label(root, text="", font=font_style, bg='#f0f0f0', fg='#333')
result_label.pack(pady=10)

# Bắt đầu vòng lặp ứng dụng
root.mainloop()
