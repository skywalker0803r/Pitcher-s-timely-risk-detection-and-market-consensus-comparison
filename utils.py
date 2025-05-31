import numpy as np
import mediapipe as mp
import numpy as np

def get_landmark_vector(lm, index):
    if isinstance(lm, list):
        return np.array([[frame[index].x, frame[index].y, frame[index].z] for frame in lm])
    else:
        return np.array([lm[index].x, lm[index].y, lm[index].z])


def calculate_angle(a, b, c):
    def calculate_angle_single_frame(a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)
    if a.ndim == 2 and b.ndim == 2 and c.ndim == 2:
        return np.array([calculate_angle_single_frame(a[i], b[i], c[i]) for i in range(len(a))])
    else:
        return calculate_angle_single_frame(a, b, c)

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
