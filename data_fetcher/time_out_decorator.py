import threading
import time
import sys


def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 定义一个内部函数来运行目标函数
            stop_event = threading.Event()

            def run_func():
                try:
                    func(stop_event=stop_event, *args, **kwargs)
                except Exception as e:
                    print(f"Function error: {e}")

            # 创建并启动线程
            thread = threading.Thread(target=run_func)
            thread.daemon = True
            thread.start()

            # 等待指定时间
            thread.join(seconds)

            if thread.is_alive():
                stop_event.set()  # 通知函数应该停止
                thread.join(1)  # 再给1秒时间清理
                print(f"Function timed out after {seconds} seconds")
                # 这里不能直接终止线程，但可以设置标志让函数自行退出

        return wrapper

    return decorator


# 示例使用
@timeout(3)
def my_function():
    print("Fetch started at", time.time())
    time.sleep(2.5)  # 模拟耗时操作
    print("Fetch completed at", time.time())  # 这行不会执行因为会超时


if __name__ == "__main__":
    while True:
        print("Loop start at", time.time())
        my_function()
        time.sleep(4)
        print("Loop end at", time.time())
