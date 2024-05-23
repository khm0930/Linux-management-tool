#!/usr/bin/env python3

# tkinter 모듈을 tk로 가져오기
import tkinter as tk
# 외부 프로세스 실행을 위해 subprocess 모듈 가져오기
import subprocess

# 'ls' 명령어를 실행하는 함수 정의
def run_ls_command():
    # 사용자가 입력한 디렉토리 경로 가져오기
    directory = directory_entry.get()
    # subprocess 모듈을 사용하여 'll' 명령 실행
    result = subprocess.run(["ls","-l", directory], stdout=subprocess.PIPE)
    # 텍스트 상자 내용을 지우고 'll' 명령의 결과 표시
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result.stdout.decode())

# 메인 윈도우 생성
root = tk.Tk()
# 윈도우 제목 설정
root.title("Simple Command GUI")

# 디렉토리 입력을 위한 라벨과 엔트리(텍스트 입력 필드) 생성
directory_label = tk.Label(root, text="Enter Directory:")
# 디렉토리 입력 라벨을 윈도우에 추가 (위쪽에 약간의 여백 추가)
directory_label.pack(pady=(10, 0))

# 디렉토리 입력을 위한 엔트리 생성
directory_entry = tk.Entry(root, width=50)
# 디렉토리 입력 엔트리를 윈도우에 추가
directory_entry.pack()

# 'll' 명령을 실행하는 버튼 생성
run_button = tk.Button(root, text="Run 'ls-l' Command", command=run_ls_command)
# 실행 버튼을 윈도우에 추가 (약간의 여백 추가)
run_button.pack(pady=10)

# 결과 출력을 위한 텍스트 상자 생성
output_text = tk.Text(root, height=10, width=50)
# 텍스트 상자를 윈도우에 추가 (여백 추가)
output_text.pack(padx=10, pady=10)

# GUI 이벤트 루프 시작
root.mainloop()
