import cv2
import torch
import numpy as np
import mediapipe as mp
from model import TCNClassifier
from utils import extract_pose_from_frame

# 初始化 MediaPipe Pose 和繪圖工具
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose_detector = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False)

# Load model
model = TCNClassifier()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

# Video load
cap = cv2.VideoCapture("徐若熙 155kph 96mph 投球慢動作 20240420.mp4")

# 取得影片資訊
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 建立輸出影片 writer
output_path = "output_with_pose_and_label.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or 'XVID'
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

pose_sequence = []

WINDOW_SIZE = 30

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose = extract_pose_from_frame(img_rgb,mp_pose,mp_drawing,pose_detector)  # frame 上會直接畫骨架
    frame = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)  # 轉回 BGR 給 OpenCV 顯示

    if pose is not None:
        pose_sequence.append(pose)
    else:
        pose_sequence.append(np.zeros(99))

    if len(pose_sequence) >= WINDOW_SIZE:
        clip = np.array(pose_sequence[-WINDOW_SIZE:]).T  # (99, 30)
        clip_tensor = torch.tensor(clip, dtype=torch.float32).unsqueeze(0)  # (1, 99, 30)

        with torch.no_grad():
            logits = model(clip_tensor)
            print(logits)
            pred = torch.argmax(logits, dim=1).item()

        # 標記分類結果在畫面上
        label = "Good" if pred == 1 else "Bad"
        color = (0, 255, 0) if pred == 1 else (0, 0, 255)
        cv2.putText(frame, f"Pose: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Pose Classification", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
video_writer.release()
cv2.destroyAllWindows()
pose_detector.close()

print(f"影片已儲存為：{output_path}")
