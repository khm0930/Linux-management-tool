import pyautogui
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox

def capture_screenshot():
    try:
        # 현재 시간을 기준으로 파일 이름을 설정합니다.
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"screenshot_{current_time}.png"

        # 현재 작업 디렉토리에 "screenshots" 폴더가 없으면 생성합니다.
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        # 스크린샷을 캡처하고 파일로 저장합니다.
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join("screenshots", file_name))
        messagebox.showinfo("Success", f"Screenshot saved as {file_name} in screenshots directory.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Tkinter를 사용하여 GUI 생성
root = tk.Tk()
root.title("Screen Capture Tool")

# 버튼을 생성하고 캡처 함수와 연결
capture_button = tk.Button(root, text="Capture Screenshot", command=capture_screenshot)
capture_button.pack(pady=20)

# GUI 실행
root.mainloop()
