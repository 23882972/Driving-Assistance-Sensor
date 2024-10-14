import subprocess
import os
from datetime import datetime
import time


class GitHandler:
    def __init__(self):
        """
        初始化 GitHandler 类
        设置固定的 Git 仓库路径、要提交的文件和文件夹
        """
        self.repo_path = "/path/to/your/repo"  # 固定的 Git 仓库路径
        self.files_to_commit = ["data1.csv", "data2.csv"]  # 固定的 CSV 文件列表
        self.folder_to_commit = "your_folder"  # 固定的文件夹
        self.last_commit_time = time.time()  # 记录上次提交的时间
        self.commit_interval = 10  # 每 10 秒提交一次

    def add_and_commit(self):
        """
        添加文件到 Git 暂存区并提交更改
        """
        try:
            os.chdir(self.repo_path)
            # 添加 CSV 文件和文件夹到 Git 暂存区
            subprocess.run(["git", "add"] + self.files_to_commit, check=True)
            subprocess.run(["git", "add", self.folder_to_commit], check=True)

            # 检查是否有更改需要提交
            if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
                commit_message = f"Auto commit: {datetime.now()}"
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                print(f"Committed: {commit_message}")
            else:
                print("No changes to commit")
        except subprocess.CalledProcessError as e:
            print(f"Error during Git add or commit: {e}")

    def push(self):
        """
        将本地更改推送到远程仓库
        """
        try:
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("Pushed changes to GitHub")
        except subprocess.CalledProcessError as e:
            print(f"Error during Git push: {e}")

    def commit_and_push(self):
        """
        完整的提交和推送过程
        """
        current_time = time.time()
        if current_time - self.last_commit_time >= self.commit_interval:
            self.add_and_commit()
            self.push()
            self.last_commit_time = current_time
