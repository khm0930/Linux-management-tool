import paramiko
from tkinter import messagebox

class VirtualServer:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def execute_command(self, command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh.exec_command(command)
            messagebox.showinfo("Virtual Server", stdout.read().decode())
            ssh.close()
        except Exception as e:
            messagebox.showerror("Virtual Server", f"서버 제어 실패: {e}")

if __name__ == "__main__":
    host = "your.server.ip"
    username = "your-username"
    password = "your-password"
    command = "echo 'Hello, World!'"
    server = VirtualServer(host, username, password)
    server.execute_command(command)
