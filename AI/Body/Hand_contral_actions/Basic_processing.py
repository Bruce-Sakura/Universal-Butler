import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

def basic_processing(holistic_results, image, previous_hand_center, movement_threshold=0.01):
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
                return previous_hand_center  # 返回上一次的手部中心点

        # 更新手部中心点
        return (hand_center_x, hand_center_y)
    return previous_hand_center  # 如果没有检测到手部，返回上一帧的手部中心点
