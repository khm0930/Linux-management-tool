import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
import subprocess
import shutil
import psutil

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 음성 도우미")
        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.recognize_button = tk.Button(self.root, text="음성 인식", command=self.recognize_speech)
        self.recognize_button.grid(column=0, row=1, padx=10, pady=10)

        self.quit_button = tk.Button(self.root, text="종료", command=self.quit_program)
        self.quit_button.grid(column=0, row=2, padx=10, pady=10)

    def recognize_speech(self):
        # 먼저 "말씀하세요!" 메시지를 출력
        self.text_area.insert(tk.END, "말씀하세요!\n")
        self.root.update()  # GUI 업데이트

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            self.text_area.insert(tk.END, "음성을 인식하는 중...\n")
            text = recognizer.recognize_google(audio, language='ko-KR')
            self.text_area.insert(tk.END, f"인식된 내용: {text}\n")
            self.text_to_speech(text)
            self.execute_command(text)  # 인식된 내용을 바탕으로 명령 실행
        except sr.UnknownValueError:
            self.text_area.insert(tk.END, "Google 음성 인식이 음성을 이해하지 못했습니다.\n")
        except sr.RequestError as e:
            self.text_area.insert(tk.END, f"Google 음성 인식 서비스에 요청할 수 없습니다; {e}\n")

    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='ko')
        filename = "output.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)

    def execute_command(self, text):
        if "파이어폭스" in text or "인터넷" in text:
            self.open_firefox()
        elif "터미널" in text:
            self.open_terminal()
        elif "파일 열기" in text:
            self.open_file()
        elif "음악 재생" in text:
            self.play_music()
        elif "파일 탐색기" in text:
            self.open_file_explorer()
        elif "시스템 종료" in text or "컴퓨터종료" in text:
            self.shutdown_system()
        elif "스크린샷" in text:
            self.take_screenshot()
        elif "파일 복사" in text:
            self.copy_file()
        elif "음량 높여" in text:
            self.change_volume("up")
        elif "음량 낮춰" in text:
            self.change_volume("down")
        elif "종료" in text:
            self.quit_program()
        elif "시스템 정보" in text:
            self.system_info()
        elif "ip변경" in text or "IP 변경" in text or "네트워크 변경" in text:
            self.run_ip_script()
        # 추가 명령은 여기에 작성

    def open_firefox(self):
        try:
            subprocess.run(["firefox"])
            self.text_area.insert(tk.END, "Firefox를 실행했습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Firefox 실행에 실패했습니다: {e}\n")

    def open_terminal(self):
        try:
            subprocess.run(["gnome-terminal"])
            self.text_area.insert(tk.END, "터미널을 실행했습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"터미널 실행에 실패했습니다: {e}\n")

    def open_file(self):
        file_path = "/path/to/your/file.txt"  # 여기에 열고 싶은 파일 경로를 입력하세요
        try:
            subprocess.run(["xdg-open", file_path])
            self.text_area.insert(tk.END, f"{file_path} 파일을 열었습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"파일 열기에 실패했습니다: {e}\n")

    def play_music(self):
        music_path = "/path/to/your/music.mp3"  # 여기에 재생할 음악 파일 경로를 입력하세요
        try:
            subprocess.run(["xdg-open", music_path])
            self.text_area.insert(tk.END, f"{music_path} 음악을 재생합니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"음악 재생에 실패했습니다: {e}\n")

    def open_file_explorer(self):
        try:
            subprocess.run(["xdg-open", os.path.expanduser("~")])
            self.text_area.insert(tk.END, "파일 탐색기를 열었습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"파일 탐색기 열기에 실패했습니다: {e}\n")

    def shutdown_system(self):
        try:
            subprocess.run(["shutdown", "now"])
            self.text_area.insert(tk.END, "시스템을 종료합니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"시스템 종료에 실패했습니다: {e}\n")

    def take_screenshot(self):
        screenshot_path = os.path.join(os.path.expanduser("~"), "screenshot.png")
        try:
            subprocess.run(["gnome-screenshot", "-f", screenshot_path])
            self.text_area.insert(tk.END, f"스크린샷을 찍었습니다: {screenshot_path}\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"스크린샷 찍기에 실패했습니다: {e}\n")

    def copy_file(self):
        src_path = "/path/to/source/file.txt"  # 복사할 파일 경로
        dst_path = "/path/to/destination/file.txt"  # 복사될 경로
        try:
            shutil.copy(src_path, dst_path)
            self.text_area.insert(tk.END, f"{src_path} 파일을 {dst_path}로 복사했습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"파일 복사에 실패했습니다: {e}\n")

    def change_volume(self, direction):
        try:
            if direction == "up":
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%+"])
                self.text_area.insert(tk.END, "음량을 높였습니다.\n")
            elif direction == "down":
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "5%-"])
                self.text_area.insert(tk.END, "음량을 낮췄습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"음량 조절에 실패했습니다: {e}\n")

    def quit_program(self):
        self.text_area.insert(tk.END, "프로그램을 종료합니다.\n")
        self.root.quit()

    def system_info(self):
        info = f"""
        CPU 사용률: {psutil.cpu_percent()}%
        메모리 사용률: {psutil.virtual_memory().percent}%
        디스크 사용률: {psutil.disk_usage('/').percent}%
        """
        self.text_area.insert(tk.END, f"시스템 정보:\n{info}\n")
        self.text_to_speech(info)

    def run_ip_script(self):
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'ip.py')
            subprocess.run(["python3", script_path])
            self.text_area.insert(tk.END, "ip.py 파일을 실행했습니다.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"ip.py 파일 실행에 실패했습니다: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
