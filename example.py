import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os
import threading

def select_source_dir():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_dir)

def select_target_dir():
    target_dir = filedialog.askdirectory()
    if target_dir:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, target_dir)

def copy_with_progress(src, dst, progress, progress_label, progress_window, skipped_files):
    total_size = 0
    copied_size = 0

    # 전체 크기를 계산, 예외 처리 포함
    for dirpath, _, filenames in os.walk(src):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)  # 소스 디렉토리의 총 파일 크기를 계산합니다.
            except (PermissionError, FileNotFoundError):
                skipped_files.append(filepath)
                continue

    if not os.path.exists(dst):
        os.makedirs(dst)
    
    # 파일을 복사하면서 진행 상태 업데이트
    for dirpath, dirnames, filenames in os.walk(src):
        dst_dirpath = dirpath.replace(src, dst, 1)
        if not os.path.exists(dst_dirpath):
            os.makedirs(dst_dirpath)
        for filename in filenames:
            src_filepath = os.path.join(dirpath, filename)
            dst_filepath = os.path.join(dst_dirpath, filename)
            try:
                shutil.copy2(src_filepath, dst_filepath)
                copied_size += os.path.getsize(src_filepath)  # 복사된 파일의 크기를 추적합니다.
                progress_value = int((copied_size / total_size) * 100)
                progress['value'] = progress_value
                progress_label.config(text=f"{progress_value}%")
                root.update_idletasks()
            except (PermissionError, FileNotFoundError):
                skipped_files.append(src_filepath)
                continue

    # 복사가 완료되면 상태 표시 창을 닫고 완료 메시지를 표시
    progress_window.destroy()
    messagebox.showinfo("Success", "Backup completed successfully!")

def start_backup_thread(source, target, progress, progress_label, progress_window):
    target_path = os.path.join(target, os.path.basename(source))
    skipped_files = []
    try:
        if os.path.exists(target_path):
            shutil.rmtree(target_path)  # 타겟 디렉토리가 존재하면 삭제
        threading.Thread(target=copy_with_progress, args=(source, target_path, progress, progress_label, progress_window, skipped_files)).start()
    except Exception as e:
        progress_window.destroy()
        messagebox.showerror("Error", f"Backup failed: {str(e)}")
    else:
        if skipped_files:
            with open(os.path.join(target, "skipped_files.log"), "w") as log_file:
                for file in skipped_files:
                    log_file.write(f"{file}\n")
            messagebox.showwarning("Warning", f"Some files were not backed up due to permission issues or missing files. See skipped_files.log in the target directory.")

def backup():
    source = source_entry.get()
    target = target_entry.get()
    if not source or not target:
        messagebox.showerror("Error", "Both source and target directories must be selected!")
    else:
        # 백업 진행 상태를 보여주는 새로운 창 생성
        progress_window = tk.Toplevel(root)
        progress_window.title("Backup Progress")
        progress_window.geometry("400x100")

        # 진행 바 생성
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=20)

        # 진행 퍼센트를 보여주는 레이블 생성
        progress_label = tk.Label(progress_window, text="0%")
        progress_label.pack()

        start_backup_thread(source, target, progress, progress_label, progress_window)

def full_backup():
    backup()

def incremental_backup():
    backup()

# 메인 윈도우 생성
root = tk.Tk()
root.title("Backup Tool")
root.geometry("500x300")

# 제목 레이블 생성
title_label = tk.Label(root, text="Backup Tool", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# 소스 디렉토리 선택 레이블 및 입력 필드 생성
source_label = tk.Label(root, text="소스 디렉토리 선택", font=("Helvetica", 12))
source_label.grid(row=1, column=0, padx=10, pady=10)

source_entry = tk.Entry(root, width=40)
source_entry.grid(row=1, column=1, padx=10, pady=10)

source_button = tk.Button(root, text="파일선택", command=select_source_dir)
source_button.grid(row=1, column=2, padx=10, pady=10)

# 타겟 디렉토리 선택 레이블 및 입력 필드 생성
target_label = tk.Label(root, text="목적지 디렉토리 선택", font=("Helvetica", 12))
target_label.grid(row=2, column=0, padx=10, pady=10)

target_entry = tk.Entry(root, width=40)
target_entry.grid(row=2, column=1, padx=10, pady=10)

target_button = tk.Button(root, text="파일선택", command=select_target_dir)
target_button.grid(row=2, column=2, padx=10, pady=10)

# 백업 버튼 생성
backup_button = tk.Button(root, text="백업", command=backup)
backup_button.grid(row=3, column=0, padx=10, pady=20)

# 풀 백업 버튼 생성
full_backup_button = tk.Button(root, text="풀백업", command=full_backup)
full_backup_button.grid(row=3, column=1, padx=10, pady=20)

# 증분 백업 버튼 생성
incremental_backup_button = tk.Button(root, text="incremental 백업", command=incremental_backup)
incremental_backup_button.grid(row=3, column=2, padx=10, pady=20)

# GUI 이벤트 루프 시작
root.mainloop()
