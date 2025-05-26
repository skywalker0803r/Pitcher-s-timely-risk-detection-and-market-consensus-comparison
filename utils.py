import mediapipe as mp
import numpy as np

def extract_pose_from_frame(image,mp_pose,mp_drawing,pose_detector):
    """提取 3D pose 並在原圖上畫出關節骨架"""
    results = pose_detector.process(image)
    if results.pose_landmarks:
        # 繪製骨架
        mp_drawing.draw_landmarks(
            image, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )
        # 印出所有關鍵點的 x, y, z
        for i, landmark in enumerate(results.pose_landmarks.landmark):
            print(f"Landmark {i}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}, visibility={landmark.visibility:.2f}")

        # 提取 99 維 pose 特徵
        keypoints = []
        for lm in results.pose_landmarks.landmark:
            keypoints.extend([lm.x, lm.y, lm.z])
        return np.array(keypoints)
    else:
        return None
