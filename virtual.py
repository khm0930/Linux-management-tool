import tkinter as tk
from tkinter import messagebox, filedialog

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("ISO files", "*.iso")])
    if file_path:
        print("선택된 파일 경로:", file_path)

def create_vm():
    # 가상 머신 생성 코드
    vm_window = tk.Toplevel(root)
    vm_window.title("가상 머신 생성")
    
    # 파일 선택 버튼
    select_file_button = tk.Button(vm_window, text="운영체제 ISO 파일 선택", command=open_file_dialog)
    select_file_button.pack(pady=10)
    #messagebox.showinfo("가상 머신 생성", "가상 머신이 생성되었습니다.")

def start_vm():
    # 가상 머신 시작 코드
    select_file_button = tk.Button(button_frame, text="선택할 파일", command=open_file_dialog)
    select_file_button.pack(fill="x", padx=10, pady=5)
    messagebox.showinfo("가상 머신 시작", "가상 머신이 시작되었습니다.")

def stop_vm():
    # 가상 머신 정지 코드
    messagebox.showinfo("가상 머신 정지", "가상 머신이 정지되었습니다.")

# GUI 생성
root = tk.Tk()
root.title("가상 머신 관리")
root.geometry("600x400")  # 더 큰 사이즈로 설정

# 가상 머신 목록 프레임 생성
vm_frame = tk.Frame(root)
vm_frame.pack(side="left", fill="y")

# 가상 머신 목록 레이블
vm_label = tk.Label(vm_frame, text="가상 머신 목록", font=("Arial", 12, "bold"))
vm_label.pack()

# 버튼 프레임 생성
button_frame = tk.Frame(root)
button_frame.pack(side="right", padx=20, pady=20)

# 버튼 생성
create_button = tk.Button(button_frame, text="가상 머신 생성", command=create_vm)
create_button.pack(fill="x", padx=10, pady=5)

start_button = tk.Button(button_frame, text="가상 머신 시작", command=start_vm)
start_button.pack(fill="x", padx=10, pady=5)

stop_button = tk.Button(button_frame, text="가상 머신 정지", command=stop_vm)
stop_button.pack(fill="x", padx=10, pady=5)

# GUI 실행
root.mainloop()
