import tkinter as tk
from tkinter import messagebox
import psutil

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Manager")
        self.geometry("450x300")
        
        # 'List Processes' 버튼
        self.list_button = tk.Button(self, text="List Processes", command=self.list_processes)
        self.list_button.pack(pady=10)
        
    def list_processes(self):
        self.destroy()
        ProcessListScreen()

class ProcessListScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process List")
        self.geometry("800x600")
        
        # 스크롤바 추가
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 프로세스 목록 표시를 위한 텍스트 위젯
        self.process_text = tk.Text(self, height=15, width=50, yscrollcommand=scrollbar.set)
        self.process_text.pack(padx=10, pady=10)
        
        # 스크롤바와 텍스트 위젯 연결
        scrollbar.config(command=self.process_text.yview)
        
        # 'Stop Process' 버튼
        self.stop_button = tk.Button(self, text="Stop Selected Process", command=self.stop_selected_process)
        self.stop_button.pack(pady=10)
        
        # 'Refresh' 버튼
        self.refresh_button = tk.Button(self, text="Refresh", command=self.update_process_list)
        self.refresh_button.pack(pady=10)
        
        # '뒤로가기' 버튼
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)
        
        # 프로세스 목록 가져오기
        self.update_process_list()
        
    def update_process_list(self):
        self.process_text.delete(1.0, tk.END)
        processes = []
        for proc in psutil.process_iter():
            try:
                process_name = proc.name()
                process_id = proc.pid
                processes.append(f"Name: {process_name}, PID: {process_id}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        if processes:
            self.process_text.insert(tk.END, "\n".join(processes))
        else:
            self.process_text.insert(tk.END, "No processes found.")
        
    def stop_selected_process(self):
        selected_text = self.process_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            pid = int(selected_text.split("PID: ")[1])
            try:
                process = psutil.Process(pid)
                process.terminate()
                messagebox.showinfo("Success", f"Process with PID {pid} terminated successfully.")
                # 프로세스를 중지한 후에 자동으로 갱신되도록 주석 처리
                # self.update_process_list()
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "Process does not exist.")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "Permission denied to terminate the process.")
        else:
            messagebox.showerror("Error", "Please select a process to stop.")
        
    def go_back(self):
        self.destroy()
        MainApplication().mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
