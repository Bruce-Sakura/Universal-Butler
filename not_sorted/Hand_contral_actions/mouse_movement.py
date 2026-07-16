import pyautogui

def mouse_movement(hand_landmarks, screen_width, screen_height, scale_factor,hand_center_x, hand_center_y):
    """
    处理鼠标移动逻辑
    """

    # 获取食指尖端位置
    index_finger_tip = hand_landmarks[8]  # 食指尖端索引

    # 映射食指尖端位置到屏幕分辨率
    finger_tip_screen_x = int((1 - index_finger_tip.x) * screen_width * scale_factor)
    finger_tip_screen_y = int(index_finger_tip.y * screen_height * scale_factor)

    # 更新鼠标位置到食指指尖位置
    pyautogui.moveTo(finger_tip_screen_x, finger_tip_screen_y, duration=0)

    # 更新手部中心点位置
    return (hand_center_x, hand_center_y)
