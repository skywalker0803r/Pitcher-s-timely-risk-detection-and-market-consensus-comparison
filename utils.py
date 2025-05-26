import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

def extract_pose_from_frame(frame):
    results = pose.process(frame)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        coords = np.array([[l.x, l.y, l.z] for l in landmarks])
        return coords.flatten()  # shape = (99,)
    else:
        return None
