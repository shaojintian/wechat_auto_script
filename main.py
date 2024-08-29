import pyautogui
import time

def like_message(x, y):
    """
    点击指定坐标位置来模拟点赞动作
    :param x: x坐标
    :param y: y坐标
    """
    pyautogui.moveTo(x, y, duration=0.5)  # 移动到指定位置
    pyautogui.click()  # 点击鼠标

def scroll_down(times, interval=1):
    """
    向下滚动微信消息列表
    :param times: 滚动的次数
    :param interval: 每次滚动之间的间隔时间
    """
    for _ in range(times):
        pyautogui.scroll(-500)  # 向下滚动
        time.sleep(interval)

def auto_like(start_x, start_y, steps, scroll_times, interval_between_scroll=1):
    """
    自动点赞脚本
    :param start_x: 第一个消息的点赞按钮的x坐标
    :param start_y: 第一个消息的点赞按钮的y坐标
    :param steps: 每次点赞后移动的步数
    :param scroll_times: 向下滚动的次数
    :param interval_between_scroll: 滚动之间的间隔时间
    """
    current_y = start_y
    
    for _ in range(scroll_times):
        # 对当前可见的消息进行点赞
        for _ in range(steps):
            like_message(start_x, current_y)
            current_y += 100  # 假设每个消息的点赞按钮纵向间隔为100像素
        
        # 滚动屏幕
        scroll_down(1, interval_between_scroll)
        current_y = start_y  # 重置y坐标

if __name__ == "__main__":
    time.sleep(5)  # 给用户5秒钟时间来切换到微信窗口
    auto_like(start_x=500, start_y=300, steps=5, scroll_times=10, interval_between_scroll=2)
