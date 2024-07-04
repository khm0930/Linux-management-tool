import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_ip_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'ip.py')
        subprocess.run(["python3", script_path])
    except Exception as e:
        messagebox.showerror("오류", f"ip.py 파일 실행에 실패했습니다: {e}")

def run_backup_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'backup.py')
        subprocess.run(["python3", script_path])
    except Exception as e:
        messagebox.showerror("오류", f"backup.py 파일 실행에 실패했습니다: {e}")

def run_capture_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'capture.py')
        subprocess.run(["python3", script_path])
    except Exception as e:
        messagebox.showerror("오류", f"capture.py 파일 실행에 실패했습니다: {e}")
        
def run_monitor_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'monitor.py')
        subprocess.run(["python3", script_path])
    except Exception as e:
        messagebox.showerror("오류", f"montior.py 파일 실행에 실패했습니다: {e}")

def run_voice_script():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'ai_voice2.py')
        subprocess.run(["python3", script_path])
    except Exception as e:
        messagebox.showerror("오류", f"ai_voice2.py 파일 실행에 실패했습니다: {e}")

# 메인 윈도우 생성
root = tk.Tk()
root.title("리눅스 도구 모음")
root.geometry("400x320")

# 레이블 생성
title_label = tk.Label(root, text="리눅스 도구 모음", font=("Helvetica", 16))
title_label.pack(pady=10)

# 버튼 프레임 생성
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 첫 번째 열 버튼
btn_ip_change = tk.Button(button_frame, text="IP 변경", width=15, command=run_ip_script)
btn_backup = tk.Button(button_frame, text="백업", width=15, command=run_backup_script)
btn_screenshot = tk.Button(button_frame, text="스크린샷 캡처", width=15, command=run_capture_script)
btn_disk_clean = tk.Button(button_frame, text="디스크 정리", width=15)

btn_ip_change.grid(row=0, column=0, padx=10, pady=5)
btn_backup.grid(row=1, column=0, padx=10, pady=5)
btn_screenshot.grid(row=2, column=0, padx=10, pady=5)
btn_disk_clean.grid(row=3, column=0, padx=10, pady=5)

# 두 번째 열 버튼
btn_monitoring = tk.Button(button_frame, text="모니터링", width=15, command=run_monitor_script)
btn_cloud_storage = tk.Button(button_frame, text="클라우드 스토리지", width=15)
btn_record_screen = tk.Button(button_frame, text="화면 녹화", width=15)
btn_virtual_server = tk.Button(button_frame, text="가상 서버", width=15)

btn_monitoring.grid(row=0, column=1, padx=10, pady=5)
btn_cloud_storage.grid(row=1, column=1, padx=10, pady=5)
btn_record_screen.grid(row=2, column=1, padx=10, pady=5)
btn_virtual_server.grid(row=3, column=1, padx=10, pady=5)

# 음성인식 버튼
btn_voice_recognition = tk.Button(root, text="음성인식", width=20 , command=run_voice_script)
btn_voice_recognition.pack(pady=20)

# 메인 루프 실행
root.mainloop()
