import sys
import cv2
import mediapipe as mp
import numpy as np
import os
from utils import calculate_angle, get_landmark_vector

mp_pose = mp.solutions.pose


# 使用左右腳踝 z 軸的平均，越小表示越靠近攝影機
def detect_foot_strike(landmarks):
    left_ankle = landmarks[27]  # 左腳踝
    right_ankle = landmarks[28]  # 右腳踝
    avg_z = (left_ankle.z + right_ankle.z) / 2
    return avg_z


# 手腕與肩膀的 y 軸差越小，表示越水平
def detect_arm_horizontal_score(landmarks):
    l_sh, l_wr = landmarks[11], landmarks[15]  # 左肩膀 左手腕
    r_sh, r_wr = landmarks[12], landmarks[16]  # 右肩膀 右手腕
    l_y_span = abs(l_sh.y - l_wr.y)  # 左肩與左手腕的 Y 差
    r_y_span = abs(r_sh.y - r_wr.y)  # 右肩與右手腕的 Y 差
    return l_y_span + r_y_span


# 用手腕移動速度最大當作出手幀
def detect_release_frame_index(landmark_seq):
    velocities = []
    for i in range(1, len(landmark_seq)):
        prev = landmark_seq[i - 1][16]  # 前一幀手腕座標
        curr = landmark_seq[i][16]  # 當前幀手腕座標
        speed = np.linalg.norm(  # 三維歐幾里得距離
            np.array([curr.x, curr.y, curr.z]) - np.array([prev.x, prev.y, prev.z])
        )
        velocities.append(speed)
    return velocities


# 左右髖的 z 值差越大，表示轉動幅度越大
def detect_hip_rotation_score(landmarks):
    l_hip = landmarks[23]  # 左髖
    r_hip = landmarks[24]  # 右髖
    return abs(r_hip.z - l_hip.z)  # Z 軸差


# 手肘彎曲角度
def calc_elbow_angle(lm):
    return calculate_angle(
        get_landmark_vector(lm, 12),  # 右肩
        get_landmark_vector(lm, 14),  # 右手肘
        get_landmark_vector(lm, 16),  # 右手腕
    )


# 腳踝出發看兩邊髖部延伸形成的角度
def calc_leg_angle(lm):
    return calculate_angle(
        get_landmark_vector(lm, 23),  # 左髖
        get_landmark_vector(lm, 27),  # 左腳踝
        get_landmark_vector(lm, 24),  # 右髖
    )


def calc_arm_horizontal_symmetry(lm):
    def calc_arm_horizontal_symmetry_single_frame(lm):
        return 1 - abs(lm[15].y - lm[16].y)  # 左右手腕 Y 差越小越對稱
    if isinstance(lm, list):
        return np.array([calc_arm_horizontal_symmetry_single_frame(frame) for frame in lm])
    else:
        return calc_arm_horizontal_symmetry_single_frame(lm)


def calc_hip_twist_z(lm):
    if isinstance(lm, list):
        return np.array([abs(frame[23].z - frame[24].z) for frame in lm])
    else:
        return abs(lm[23].z - lm[24].z)  # 髖部左右 z 軸差異


# 主流程
def extract_four_keyframes(video_path, output_dir):
    # 讀取影片
    cap = cv2.VideoCapture(video_path)
    # 骨架模型初始化
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

    frame_landmarks = []
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
    if len(frame_landmarks) < 5:
        print(f"⚠️ 無法從 {video_path} 擷取足夠幀")
        return
    
    # 確保有足夠的幀數進行特徵擷取
    # 設定安全邊界，避免索引超出範圍
    # 改成只在有效區間內做搜尋[30:-30]，避免邊界問題
    # 最後再加上 30 幀的偏移量
    foot_idx = np.argmin([detect_foot_strike(lm) for lm in frame_landmarks][30:-30]) + 30
    arm_idx = np.argmin([detect_arm_horizontal_score(lm) for lm in frame_landmarks][30:-30]) + 30
    release_idx = np.argmax([detect_release_frame_index(frame_landmarks[30:-30])]) + 1 + 30
    hip_idx = np.argmax([detect_hip_rotation_score(lm) for lm in frame_landmarks][30:-30]) + 30
    print(f"⚠️ 偵測到的腳踝出發幀：{foot_idx}, 手臂水平幀：{arm_idx}, 出手幀：{release_idx}, 髖部轉動幀：{hip_idx}")

    # 組合特徵資料
    features = {
        "leg_angle": calc_leg_angle(frame_landmarks[foot_idx-30:foot_idx+30]),
        "arm_symmetry": calc_arm_horizontal_symmetry(frame_landmarks[arm_idx-30:arm_idx+30]),
        "elbow_angle": calc_elbow_angle(frame_landmarks[release_idx-30:release_idx+30]),
        "hip_twist": calc_hip_twist_z(frame_landmarks[hip_idx-30:hip_idx+30]),
    }
    
    # 儲存為 .npy 檔
    filename = os.path.splitext(os.path.basename(video_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    np.save(
        os.path.join(output_dir, filename + "_keyframe_feats.npy"),
        np.array(list(features.values())),
    )
    # 打印成功訊息和資料shape
    print(f"✅ 已儲存四幀特徵：{filename}, shape:{np.array(list(features.values())).shape}")


# 若用命令列執行
if __name__ == "__main__":
    video_path = sys.argv[1]  # 第 1 個參數：影片路徑
    output_dir = sys.argv[2]  # 第 2 個參數：儲存資料夾
    extract_four_keyframes(video_path, output_dir)
