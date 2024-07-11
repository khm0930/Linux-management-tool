import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        self.recording_process = None
        self.paused = False

        tk.Label(root, text="Screen Recorder", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(root, text="Frame rate:").pack(pady=5)
        self.frame_rate = tk.Entry(root)
        self.frame_rate.insert(0, "30")
        self.frame_rate.pack(pady=5)

        tk.Label(root, text="Video width:").pack(pady=5)
        self.video_width = tk.Entry(root)
        self.video_width.insert(0, "1920")
        self.video_width.pack(pady=5)

        tk.Label(root, text="Video height:").pack(pady=5)
        self.video_height = tk.Entry(root)
        self.video_height.insert(0, "1080")
        self.video_height.pack(pady=5)

        tk.Label(root, text="Output file:").pack(pady=5)
        self.output_file = tk.Entry(root)
        self.output_file.insert(0, "output.avi")
        self.output_file.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(root, text="Pause Recording", command=self.pause_recording, state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        self.resume_button = tk.Button(root, text="Resume Recording", command=self.resume_recording, state=tk.DISABLED)
        self.resume_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def browse_file(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".avi",
                                                   filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
        if output_file:
            self.output_file.delete(0, tk.END)
            self.output_file.insert(0, output_file)

    def start_recording(self):
        frame_rate = self.frame_rate.get()
        video_width = self.video_width.get()
        video_height = self.video_height.get()
        output_file = self.output_file.get()

        # 절대 경로로 변환
        if not os.path.isabs(output_file):
            output_file = os.path.abspath(output_file)

        # 파일이 존재하면 사용자에게 새로운 파일 이름을 입력받음
        while os.path.exists(output_file):
            output_file = simpledialog.askstring("File exists", "File already exists. Enter a new file name:", initialvalue=output_file)
            if not output_file:
                messagebox.showerror("Error", "Recording canceled due to no valid file name.")
                return

        command = [
            'gst-launch-1.0',
            'ximagesrc', 'use-damage=0', '!',
            'video/x-raw,framerate={}/1,width={},height={}'.format(frame_rate, video_width, video_height), '!',
            'videoconvert', '!',
            'avenc_mpeg4', '!',
            'avimux', '!',
            'filesink', 'location={}'.format(output_file)
        ]

        self.recording_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        messagebox.showinfo("Screen Recorder", "Recording started")

    def pause_recording(self):
        if self.recording_process:
            self.recording_process.send_signal(subprocess.signal.SIGSTOP)
            self.paused = True
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            messagebox.showinfo("Screen Recorder", "Recording paused")

    def resume_recording(self):
        if self.recording_process and self.paused:
            self.recording_process.send_signal(subprocess.signal.SIGCONT)
            self.paused = False
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            messagebox.showinfo("Screen Recorder", "Recording resumed")

    def stop_recording(self):
        if self.recording_process:
            self.recording_process.terminate()
            stdout, stderr = self.recording_process.communicate()
            print("GStreamer stdout:", stdout.decode())
            print("GStreamer stderr:", stderr.decode())
            self.recording_process = None
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("Screen Recorder", "Recording stopped and saved")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
