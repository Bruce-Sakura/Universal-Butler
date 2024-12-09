import pyautogui
import time

# 记录上一次点击时间
last_click_time = None

def mouse_click(hand_landmarks, hand_center, Click_threshold, movement_threshold, previous_hand_center, double_click_threshold):
    """
    处理鼠标点击功能
    """
    global last_click_time

    # 如果手心位置变化超过阈值，则跳过点击
    if previous_hand_center is not None:
        prev_x, prev_y = previous_hand_center
        movement_x = abs(hand_center[0] - prev_x)
        movement_y = abs(hand_center[1] - prev_y)
        if movement_x > movement_threshold or movement_y > movement_threshold:
            previous_hand_center = hand_center  # 更新手心位置
            return previous_hand_center  # 返回更新后的手心位置，跳过点击

    # 获取大拇指指尖和食指指尖的位置
    thumb_tip = hand_landmarks[4]  # 大拇指指尖
    index_finger_tip = hand_landmarks[8]  # 食指指尖

    # 计算大拇指指尖和食指指尖之间的距离
    distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5

    # 判断是否触发点击
    if distance < Click_threshold:  # 如果距离小于阈值，可能是点击
        current_time = time.time()  # 获取当前时间

        if last_click_time is not None:
            # 判断是否为双击
            if current_time - last_click_time < double_click_threshold:
                # 双击
                pyautogui.doubleClick()
                last_click_time = None  # 重置时间
                return previous_hand_center  # 返回更新后的手心位置

        # 单击
        pyautogui.click()
        last_click_time = current_time  # 记录当前点击时间

    # 更新手心位置
    previous_hand_center = hand_center
    return previous_hand_center  # 返回更新后的手心位置
