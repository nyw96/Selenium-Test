import subprocess, datetime, time, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DELAY = 30  # 변경 감지 후 N초 후 커밋

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    return result.returncode == 0

class GitHandler(FileSystemEventHandler):
    def __init__(self):
        self.timer = None

    def on_any_event(self, event):
        if event.is_directory:
            return
        if ".git" in event.src_path:
            return
        print(f"변경 감지: {event.src_path}")
        if self.timer:
            self.timer.cancel()
        import threading
        self.timer = threading.Timer(DELAY, self.commit_and_push)
        self.timer.start()

    def commit_and_push(self):
        run("git add -A")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"auto: {now}"
        if run(f'git commit -m "{msg}"'):
            if run("git push origin main"):
                print(f"자동 푸시 완료 ({msg})")
            else:
                print("푸시 실패")
        else:
            print("커밋할 변경사항 없음")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"감시 시작: {path}  (변경 후 {DELAY}초 후 자동 커밋)")
    observer = Observer()
    observer.schedule(GitHandler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()