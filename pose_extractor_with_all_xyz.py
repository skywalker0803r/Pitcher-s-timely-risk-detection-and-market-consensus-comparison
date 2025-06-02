import sys
import cv2
import mediapipe as mp
import numpy as np
import os

mp_pose = mp.solutions.pose

# 主流程
def extract_four_keyframes(video_path, output_dir):
    
    # 讀取影片
    cap = cv2.VideoCapture(video_path)
    
    # 骨架模型初始化
    pose = mp_pose.Pose(static_image_mode=False, # 使用影片模式，自動追蹤關鍵點
                        min_detection_confidence=0.5, # 預設值，平衡準確度與覆蓋率
                        smooth_landmarks=True, # 啟用平滑，減少 jitter
                        )

    frame_landmarks = []
    
    # 逐幀讀取影片
    while cap.isOpened():  # 確保影片成功打開
        ret, frame = cap.read()  # 每次從影片讀取「一幀」
        if not ret:
            break
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
        results = pose.process(image_rgb)  # 回傳抓到 33 個關鍵點
        if results.pose_landmarks:  # 骨架資訊（若沒偵測成功則是 None）
            frame_landmarks.append(results.pose_landmarks.landmark)

    cap.release()  # 關閉影片檔案、釋放記憶體
    pose.close()  # 關閉 MediaPipe 的姿勢模型、釋放 GPU / CPU 記憶體
    
    # 錯誤處理
    if len(frame_landmarks) < 5:
        print(f"⚠️ 無法從 {video_path} 擷取足夠幀")
        return
    
    # 將frame_landmarks轉換為numpy陣列(num_frames, num_landmarks, 3)
    all_xyz = np.array([[(lm.x, lm.y, lm.z) for lm in landmarks]for landmarks in frame_landmarks], dtype=np.float32)
    if all_xyz.shape[1] != 33 or all_xyz.shape[2] != 3:
        print(f"資料形狀錯誤: {all_xyz.shape}")
        return
    
    # 儲存為 .npy 檔
    filename = os.path.splitext(os.path.basename(video_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    np.save(os.path.join(output_dir, filename + "_all_xyz.npy"), all_xyz)
    
    # 打印成功訊息和資料shape
    print(f"✅ 已儲存全部特徵：{filename}, shape:{all_xyz.shape}")


# 若用命令列執行
if __name__ == "__main__":
    video_path = sys.argv[1]  # 第 1 個參數：影片路徑
    output_dir = sys.argv[2]  # 第 2 個參數：儲存資料夾
    extract_four_keyframes(video_path, output_dir)
