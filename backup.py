import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os
import threading
from concurrent.futures import ThreadPoolExecutor

BUFFER_SIZE = 1024 * 1024  # 1MB 버퍼

exclude_paths = []  # 제외할 경로를 저장하는 리스트

# 소스 디렉토리를 선택하는 함수
def select_source_dir():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, source_dir)

# 타겟 디렉토리를 선택하는 함수
def select_target_dir():
    target_dir = filedialog.askdirectory()
    if target_dir:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, target_dir)

# 제외할 경로들을 선택하는 함수
def select_exclude_paths():
    # 파일 선택
    file_paths = filedialog.askopenfilenames(title="제외할 파일 선택")
    if file_paths:
        for path in file_paths:
            if path not in exclude_paths:
                exclude_paths.append(path)
                exclude_listbox.insert(tk.END, path)
    
    # 디렉토리 선택
    dir_path = filedialog.askdirectory(title="제외할 디렉토리 선택")
    if dir_path:
        if dir_path not in exclude_paths:
            exclude_paths.append(dir_path)
            exclude_listbox.insert(tk.END, dir_path)



# 제외할 경로들을 리스트에서 제거하는 함수
def remove_exclude_paths():
    selected_items = exclude_listbox.curselection()
    for index in selected_items[::-1]:
        exclude_listbox.delete(index)
        del exclude_paths[index]

# 파일을 버퍼를 사용하여 복사하는 함수
def copy_file_with_buffer(src_filepath, dst_filepath):
    with open(src_filepath, 'rb') as src_file:
        with open(dst_filepath, 'wb') as dst_file:
            while True:
                buffer = src_file.read(BUFFER_SIZE)
                if not buffer:
                    break
                dst_file.write(buffer)

# 복사 진행 상태를 보여주면서 파일을 복사하는 함수
def copy_with_progress(src, dst, progress, progress_label, progress_window, skipped_files):
    total_size = 0
    copied_size = 0

    # 전체 파일 크기를 계산, 예외 처리 포함
    for dirpath, _, filenames in os.walk(src):
        if should_exclude(dirpath):
            continue  # 제외할 경로는 무시
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if not os.path.islink(filepath):  # 심볼릭 링크가 아닌 경우에만 크기를 계산
                    total_size += os.path.getsize(filepath)  # 소스 디렉토리의 총 파일 크기를 계산
            except (PermissionError, FileNotFoundError, OSError):
                skipped_files.append(filepath)
                continue

    if not os.path.exists(dst):
        os.makedirs(dst)

    # ThreadPoolExecutor를 사용하여 멀티스레딩으로 파일 복사
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for dirpath, dirnames, filenames in os.walk(src):
            if should_exclude(dirpath):
                continue  # 제외할 경로는 무시
            dst_dirpath = dirpath.replace(src, dst, 1)
            if not os.path.exists(dst_dirpath):
                os.makedirs(dst_dirpath)
            for filename in filenames:
                src_filepath = os.path.join(dirpath, filename)
                dst_filepath = os.path.join(dst_dirpath, filename)
                if should_exclude(src_filepath):
                    continue  # 제외할 파일은 무시
                futures.append(executor.submit(copy_file, src_filepath, dst_filepath, skipped_files, total_size, progress, progress_label))

        for future in futures:
            try:
                future.result()  # 예외가 발생하면 여기서 다시 발생시킴
            except Exception as e:
                skipped_files.append(str(e))

    # 복사가 완료되면 상태 표시 창을 닫고 완료 메시지를 표시
    progress_window.destroy()
    messagebox.showinfo("Success", "Backup completed successfully!")

# 특정 경로가 제외할 경로에 포함되는지 확인하는 함수
def should_exclude(path):
    for exclude_path in exclude_paths:
        if path.startswith(exclude_path):
            return True
    return False

# 파일을 복사하면서 진행 상태를 업데이트하는 함수
def copy_file(src_filepath, dst_filepath, skipped_files, total_size, progress, progress_label):
    global copied_size
    try:
        if os.path.islink(src_filepath):
            # 심볼릭 링크를 복사
            linkto = os.readlink(src_filepath)
            os.symlink(linkto, dst_filepath)
        else:
            # 심볼릭 링크가 아닌 경우에만 복사
            copy_file_with_buffer(src_filepath, dst_filepath)
            file_size = os.path.getsize(src_filepath)
            with copied_size_lock:
                copied_size += file_size  # 복사된 파일의 크기를 추적
                progress_value = int((copied_size / total_size) * 100)
                progress['value'] = progress_value
                progress_label.config(text=f"{progress_value}%")
                root.update_idletasks()
    except (PermissionError, FileNotFoundError, OSError) as e:
        skipped_files.append(src_filepath)
        return str(e)

# 백업을 시작하는 스레드를 생성하는 함수
def start_backup_thread(source, target, progress, progress_label, progress_window):
    target_path = os.path.join(target, os.path.basename(source))
    skipped_files = []
    global copied_size, copied_size_lock
    copied_size = 0
    copied_size_lock = threading.Lock()
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

# 풀 백업을 시작하는 함수
def full_backup():
    source = "/"  # 시스템 전체를 소스로 설정
    target = target_entry.get()
    if not target:
        messagebox.showerror("Error", "Target directory must be selected!")
    else:
        # 풀 백업을 수행하기 전에 타겟 디렉토리를 비움
        target_path = os.path.join(target, "full_backup")
        if os.path.exists(target_path):
            shutil.rmtree(target_path)  # 기존 타겟 디렉토리를 삭제

        # 백업 진행 상태를 보여주는 새로운 창 생성
        progress_window = tk.Toplevel(root)
        progress_window.title("Full Backup Progress")
        progress_window.geometry("400x100")

        # 진행 바 생성
        progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress.pack(pady=20)

        # 진행 퍼센트를 보여주는 레이블 생성
        progress_label = tk.Label(progress_window, text="0%")
        progress_label.pack()

        start_backup_thread(source, target, progress, progress_label, progress_window)

# 증분 백업을 시작하는 함수
def incremental_backup():
    backup()

# 메인 윈도우 생성
root = tk.Tk()
root.title("Backup Tool")
root.geometry("660x500")

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

# 제외할 파일/디렉토리 선택 레이블 및 리스트박스 생성
exclude_label = tk.Label(root, text="제외할 파일/디렉토리", font=("Helvetica", 12))
exclude_label.grid(row=3, column=0, padx=10, pady=10)

exclude_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=40, height=10)
exclude_listbox.grid(row=3, column=1, padx=10, pady=10, rowspan=2)

add_exclude_button = tk.Button(root, text="제외 경로 추가", command=select_exclude_paths)
add_exclude_button.grid(row=3, column=2, padx=10, pady=10)

remove_exclude_button = tk.Button(root, text="제외 경로 삭제", command=remove_exclude_paths)
remove_exclude_button.grid(row=4, column=2, padx=10, pady=10)

# 백업 버튼 생성
backup_button = tk.Button(root, text="백업", command=backup)
backup_button.grid(row=5, column=0, padx=10, pady=20)

# 풀 백업 버튼 생성
full_backup_button = tk.Button(root, text="풀백업", command=full_backup)
full_backup_button.grid(row=5, column=1, padx=10, pady=20)

# 증분 백업 버튼 생성
incremental_backup_button = tk.Button(root, text="incremental 백업", command=incremental_backup)
incremental_backup_button.grid(row=5, column=2, padx=10, pady=20)

# GUI 이벤트 루프 시작
root.mainloop()
