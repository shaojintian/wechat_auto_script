import pyautogui
import time
import threading
import tkinter as tk
import cv2
import numpy as np

class AutoLiker:
    def __init__(self):
        self.running = False

    def like_message(self, template_path, threshold=0.8):
        # 截取屏幕
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 读取点赞按钮模板图像
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

        # 匹配模板
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果匹配度超过阈值，则认为找到了按钮
        if max_val >= threshold:
            button_x = max_loc[0] + template.shape[1] // 2
            button_y = max_loc[1] + template.shape[0] // 2
            pyautogui.moveTo(button_x, button_y, duration=0.5)
            pyautogui.click()
            return True
        return False

    def scroll_down(self, times, interval=1):
        for _ in range(times):
            pyautogui.scroll(-500)
            time.sleep(interval)

    def auto_like(self, template_path, scroll_times, interval_between_scroll=1, threshold=0.8):
        for _ in range(scroll_times):
            if not self.running:  # 检查脚本是否应该停止
                break

            # 搜索并点击所有可见的点赞按钮
            if not self.like_message(template_path, threshold):
                print("未找到点赞按钮，滚动屏幕")
            self.scroll_down(1, interval_between_scroll)

    def start(self, template_path, scroll_times, interval_between_scroll, threshold):
        if not self.running:
            self.running = True
            threading.Thread(target=self.auto_like, args=(template_path, scroll_times, interval_between_scroll, threshold)).start()

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
        # 传入点赞按钮模板的路径
        self.auto_liker.start(template_path='like_button.png', scroll_times=10, interval_between_scroll=2, threshold=0.8)

    def stop(self):
        self.auto_liker.stop()


if __name__ == "__main__":
    auto_liker = AutoLiker()

    root = tk.Tk()
    gui = AutoLikerGUI(root, auto_liker)

    root.mainloop()
