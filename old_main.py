import pyautogui
import time
import threading
import tkinter as tk
import signal
import sys

class AutoLiker:
    def __init__(self):
        self.running = False

    def like_message(self, x, y):
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()

    def scroll_down(self, times, interval=1):
        for _ in range(times):
            pyautogui.scroll(-500)
            time.sleep(interval)

    def auto_like(self, start_x, start_y, steps, scroll_times, interval_between_scroll=1):
        current_y = start_y
        
        for _ in range(scroll_times):
            if not self.running:  # 检查脚本是否应该停止
                break

            for _ in range(steps):
                self.like_message(start_x, current_y)
                current_y += 100  # 假设每个消息的点赞按钮纵向间隔为100像素

            self.scroll_down(1, interval_between_scroll)
            current_y = start_y  # 重置y坐标

    def start(self, start_x, start_y, steps, scroll_times, interval_between_scroll):
        if not self.running:
            self.running = True
            threading.Thread(target=self.auto_like, args=(start_x, start_y, steps, scroll_times, interval_between_scroll)).start()

    def stop(self):
        self.running = False


class AutoLikerGUI:
    def __init__(self, root, auto_liker):
        self.root = root
        self.auto_liker = auto_liker

        self.root.title("WeChat Auto Liker")

        start_button = tk.Button(root, text="Start", command=self.start)
        start_button.pack(pady=10)

        stop_button = tk.Button(root, text="Stop", command=self.stop)
        stop_button.pack(pady=10)

    def start(self):
        # 在这里指定你希望的坐标和参数
        self.auto_liker.start(start_x=500, start_y=300, steps=5, scroll_times=10, interval_between_scroll=2)

    def stop(self):
        self.auto_liker.stop()
        self.root.quit()  # 退出 Tkinter GUI


def signal_handler(sig, frame):
    print('Stopping script...')
    auto_liker.stop()
    root.quit()  # 退出 Tkinter GUI
    sys.exit(0)

if __name__ == "__main__":
    auto_liker = AutoLiker()

    root = tk.Tk()
    gui = AutoLikerGUI(root, auto_liker)

    # 捕获 Ctrl+C 信号
    signal.signal(signal.SIGINT, signal_handler)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        # 捕获到 KeyboardInterrupt 异常时，执行清理操作
        auto_liker.stop()
        root.quit()
        sys.exit(0)
