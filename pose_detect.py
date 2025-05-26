import cv2
import mediapipe as mp
import numpy as np

# 初始化 MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 讀取影片檔案（將 'your_video.mp4' 換成你的影片路徑）
video_path = '徐若熙 155kph 96mph 投球慢動作 20240420.mp4'
cap = cv2.VideoCapture(video_path)
all_pose_data = []
with mp_pose.Pose(static_image_mode=False,
                  model_complexity=2,  # 使用更高精度模型
                  enable_segmentation=False,
                  min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("無法讀取影像")
            break

        # 影像前處理：轉成 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 偵測姿勢
        results = pose.process(image)

        # 影像後處理：轉回 BGR 並可寫
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 畫出姿勢關鍵點

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            print(results.pose_landmarks.landmark,type(results.pose_landmarks.landmark))
            tensor = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark],dtype=np.float32)
            all_pose_data.append(tensor)
            # 印出所有關鍵點的 x, y, z
            for i, landmark in enumerate(results.pose_landmarks.landmark):
                print(f"Landmark {i}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}, visibility={landmark.visibility:.2f}")

        # 顯示畫面
        cv2.imshow('MediaPipe Pose 3D', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
all_pose_data = np.array(all_pose_data)
print(all_pose_data,all_pose_data.shape)
cap.release()
cv2.destroyAllWindows()
