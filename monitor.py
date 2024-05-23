import tkinter as tk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class SystemMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("System Monitor")

        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []

        self.fig, self.ax = plt.subplots(3, 1, figsize=(8, 6))

        self.ax[0].set_title('CPU Usage (%)')
        self.ax[1].set_title('Memory Usage (%)')
        self.ax[2].set_title('Disk Usage (%)')

        # 그래프 간 간격 조정
        plt.subplots_adjust(hspace=0.5)

        self.cpu_line, = self.ax[0].plot([], [])
        self.memory_line, = self.ax[1].plot([], [])
        self.disk_line, = self.ax[2].plot([], [])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # CPU 및 메모리 사용량을 표시할 레이블 생성
        self.cpu_label = tk.Label(master, text='CPU Usage: ')
        self.cpu_label.pack()
        self.memory_label = tk.Label(master, text='Memory Usage: ')
        self.memory_label.pack()

        self.monitor_thread = threading.Thread(target=self.track_usage)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def track_usage(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            self.cpu_usage.append(cpu_percent)
            self.memory_usage.append(memory_percent)
            self.disk_usage.append(disk_percent)

            self.update_graphs()

            # CPU 및 메모리 사용량 레이블 업데이트
            self.cpu_label.config(text='CPU Usage: {:.2f}%'.format(cpu_percent))
            self.memory_label.config(text='Memory Usage: {:.2f}%'.format(memory_percent))

            time.sleep(1)

    def update_graphs(self):
        x = range(len(self.cpu_usage))

        self.cpu_line.set_data(x, self.cpu_usage)
        self.memory_line.set_data(x, self.memory_usage)
        self.disk_line.set_data(x, self.disk_usage)

        # 각 그래프에 눈금 및 눈금 라벨 표시
        self.ax[0].set_xticks(x)
        self.ax[0].set_yticks(range(0, 101, 20))
        self.ax[0].set_yticklabels(range(0, 101, 20))
        self.ax[1].set_xticks(x)
        self.ax[1].set_yticks(range(0, 101, 20))
        self.ax[1].set_yticklabels(range(0, 101, 20))
        self.ax[2].set_xticks(x)
        self.ax[2].set_yticks(range(0, 101, 20))
        self.ax[2].set_yticklabels(range(0, 101, 20))

        self.canvas.draw()

root = tk.Tk()
app = SystemMonitorApp(root)
root.mainloop()
