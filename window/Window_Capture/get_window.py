import mss
import numpy as np
import cv2
import threading

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            screenshot = sct.grab(monitor)  # 获取屏幕截图
            frame = np.array(screenshot)  # 转换为 numpy 数组

            #  保持 RGBA 格式（包括 Alpha 通道）
            frame = frame[:, :, :4]  # 只保留 R, G, B 通道

            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            cv2.imshow("Screen Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

# 在不同线程中捕捉和显示屏幕
thread = threading.Thread(target=capture_screen)
thread.start()
thread.join()
