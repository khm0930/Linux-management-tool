import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound

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
            if "종료" in text:
                self.quit_program()
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

    def quit_program(self):
        self.text_area.insert(tk.END, "프로그램을 종료합니다.\n")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
