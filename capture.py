import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import pyautogui
import os
from datetime import datetime

class ScreenCaptureTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture Tool")
        
        # 캡처 버튼 생성 및 배치
        self.capture_button = tk.Button(root, text="Select Area and Capture", command=self.start_selection)
        self.capture_button.pack(pady=20)
        
        # 시작 좌표 초기화
        self.start_x = None
        self.start_y = None

    def start_selection(self):
        # GUI 창 숨기기
        self.root.withdraw()
        
        # 새로운 전체 화면 창 생성 및 설정
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.configure(bg='white')
        
        # 캔버스 생성 및 화면에 배치
        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 캡처할 화면을 스크린샷으로 가져옴
        self.screen_width = self.selection_window.winfo_screenwidth()
        self.screen_height = self.selection_window.winfo_screenheight()
        self.screenshot = pyautogui.screenshot()
        self.screenshot = self.screenshot.resize((self.screen_width, self.screen_height))
        self.photo = ImageTk.PhotoImage(self.screenshot)
        
        self.root.withdraw()
        
        # 캔버스에 스크린샷 이미지 배치
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # 마우스 버튼 누를 때 시작 좌표 저장 및 사각형 생성
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', tag="rect")

    def on_mouse_drag(self, event):
        # 마우스 드래그할 때 사각형 크기 조정
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red', tag="rect")

    def on_button_release(self, event):
        # 마우스 버튼 놓을 때 끝 좌표 저장 및 창 닫기
        self.end_x = event.x
        self.end_y = event.y
        self.selection_window.destroy()
        
        # 선택 영역 캡처
        screenshot = self.capture_selected_area(self.start_x, self.start_y, self.end_x, self.end_y)
        if screenshot:
            self.preview_screenshot(screenshot)
        self.root.deiconify()

    def capture_selected_area(self, x1, y1, x2, y2):
        try:
            # 선택 영역 캡처
            region = (x1, y1, x2 - x1, y2 - y1)
            screenshot = pyautogui.screenshot(region=region)
            return screenshot
        except Exception as e:
            # 오류 발생 시 메시지 박스 표시
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def preview_screenshot(self, image):
        # 미리보기 창 생성
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Screenshot Preview")
        
        # 캡처 이미지 표시
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(self.preview_window, image=self.img)
        self.img_label.pack()

        # 저장 및 그림 그리기 버튼 생성 및 배치
        self.save_button = tk.Button(self.preview_window, text="Save Screenshot", command=lambda: self.save_image(image))
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.draw_button = tk.Button(self.preview_window, text="Draw on Screenshot", command=lambda: self.draw_on_image(image))
        self.draw_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def save_image(self, image):
        # 현재 시간을 기준으로 파일 이름 생성 및 저장
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"screenshot_{current_time}.png"
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        image.save(os.path.join("screenshots", file_name))
        messagebox.showinfo("Success", f"Screenshot saved as {file_name} in screenshots directory.")
        self.preview_window.destroy()

    def draw_on_image(self, image):
        # 그림 그리기 창 생성
        self.draw_window = tk.Toplevel(self.preview_window)
        self.draw_window.title("Draw on Screenshot")

        def paint(event):
            # 마우스 드래그할 때 그림 그리기
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            self.canvas_draw.create_oval(x1, y1, x2, y2, fill='red', width=5)
            self.draw.line([x1, y1, x2, y2], fill='red', width=5)

        # 이미지 복사 및 캔버스에 표시
        self.img_draw = image.copy()
        self.draw = ImageDraw.Draw(self.img_draw)
        self.img_draw_tk = ImageTk.PhotoImage(self.img_draw)

        self.canvas_draw = tk.Canvas(self.draw_window, width=image.width, height=image.height)
        self.canvas_draw.pack()
        self.canvas_draw.create_image(0, 0, image=self.img_draw_tk, anchor=tk.NW)
        self.canvas_draw.bind("<B1-Motion>", paint)

        # 저장 버튼 생성 및 배치
        save_drawn_button = tk.Button(self.draw_window, text="Save Drawn Image", command=self.save_drawn_image)
        save_drawn_button.pack()

    def save_drawn_image(self):
        # 현재 시간을 기준으로 파일 이름 생성 및 저장
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"screenshot_drawn_{current_time}.png"
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.img_draw.save(os.path.join("screenshots", file_name))
        messagebox.showinfo("Success", f"Screenshot saved as {file_name} in screenshots directory.")
        self.draw_window.destroy()
        self.preview_window.destroy()

if __name__ == "__main__":
    # Tkinter 루트 창 생성 및 실행
    root = tk.Tk()
    app = ScreenCaptureTool(root)
    root.mainloop()
