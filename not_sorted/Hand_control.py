import cv2
import mediapipe as mp
import pyautogui
from screeninfo import get_monitors  # 获取多屏幕信息
from Hand_contral_actions.mouse_movement import mouse_movement  # 导入鼠标控制模块
from Hand_contral_actions.mouse_click import mouse_click

# 禁用 PyAutoGUI 的 fail-safe 功能
pyautogui.FAILSAFE = False

# Mediapipe 初始化
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# 获取屏幕分辨率
monitors = get_monitors()
screen_width = monitors[0].width  # 只使用第一个屏幕的宽度
screen_height = monitors[0].height  # 只使用第一个屏幕的高度

# 参数初始化
scale_factor = 1  # 鼠标放大倍率
previous_hand_center = None  # 上一帧的手部中心位置
movement_threshold = 0.01  # 最小移动阈值
Click_threshold = 0.2  # 触发点击的距离阈值
double_click_threshold = 0.3  # 双击间隔阈值（秒）

# Mediapipe Holistic 模型
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 转换帧为 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mediapipe 检测
        holistic_results = holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 检测右手并处理手势
        if holistic_results.right_hand_landmarks:
            hand_landmarks = holistic_results.right_hand_landmarks.landmark
            mp_drawing.draw_landmarks(
                image, holistic_results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )

            # 计算手部中心点
            x_coords = [landmark.x for landmark in hand_landmarks]
            y_coords = [landmark.y for landmark in hand_landmarks]
            hand_center_x = sum(x_coords) / len(x_coords)
            hand_center_y = sum(y_coords) / len(y_coords)

            # 检测手部中心点的移动（避免细微抖动）
            if previous_hand_center:
                prev_x, prev_y = previous_hand_center
                movement_x = abs(hand_center_x - prev_x)
                movement_y = abs(hand_center_y - prev_y)
                if movement_x < movement_threshold and movement_y < movement_threshold:
                    continue  # 跳过本次循环，避免过度处理

            # 鼠标移动逻辑
            previous_hand_center = mouse_movement(
                hand_landmarks=hand_landmarks,
                screen_width=screen_width,
                screen_height=screen_height,
                scale_factor=scale_factor,
                hand_center_x=hand_center_x,
                hand_center_y=hand_center_y
            )

            # 执行鼠标点击
            previous_hand_center = mouse_click(
                hand_landmarks=hand_landmarks,
                hand_center=(hand_center_x, hand_center_y),
                Click_threshold=Click_threshold,
                movement_threshold=movement_threshold,
                previous_hand_center=previous_hand_center,
                double_click_threshold=double_click_threshold
            )

        # 显示图像
        cv2.imshow('Holistic + Hand Gesture Detection', image)

        # 按 'q' 键退出
        if cv2.waitKey(16) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
