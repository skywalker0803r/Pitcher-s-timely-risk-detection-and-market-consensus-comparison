import cv2
import torch
import numpy as np
from model import TCNClassifier
from utils import extract_pose_from_frame

# Load model
model = TCNClassifier()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

# Video load
cap = cv2.VideoCapture("徐若熙 155kph 96mph 投球慢動作 20240420.mp4")
pose_sequence = []
frame_buffer = []

WINDOW_SIZE = 30

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose = extract_pose_from_frame(img_rgb)
    frame_buffer.append(frame)

    if pose is not None:
        pose_sequence.append(pose)
    else:
        pose_sequence.append(np.zeros(99))

    if len(pose_sequence) >= WINDOW_SIZE:
        clip = np.array(pose_sequence[-WINDOW_SIZE:]).T  # (99, 30)
        clip_tensor = torch.tensor(clip, dtype=torch.float32).unsqueeze(0)  # (1, 99, 30)
        print(clip_tensor.shape)

        with torch.no_grad():
            logits = model(clip_tensor)
            pred = torch.argmax(logits, dim=1).item()

        # 標記在畫面上
        label = "Good" if pred == 1 else "Bad"
        color = (0, 255, 0) if pred == 1 else (0, 0, 255)
        cv2.putText(frame, f"Pose: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Pose Classification", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
