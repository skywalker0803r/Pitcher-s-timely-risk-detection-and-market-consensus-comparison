import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import time
import os

# 初始化 MediaPipe Pose 模型
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=False,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

st.title("⚾ 即時棒球投手姿勢分析儀表板")

# 上傳影片
uploaded_file = st.file_uploader("請上傳影片", type=["mp4", "mov", "avi"])

if uploaded_file:
    os.makedirs("temp", exist_ok=True)
    video_path = "temp/uploaded.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    joint_names = {
        0: "鼻子", 1: "左眼內角", 2: "左眼", 3: "左眼外角", 4: "右眼內角",
        5: "右眼", 6: "右眼外角", 7: "左耳", 8: "右耳", 9: "嘴巴左側", 10: "嘴巴右側",
        11: "左肩膀", 12: "右肩膀", 13: "左手肘", 14: "右手肘",
        15: "左手腕", 16: "右手腕", 17: "左手小指", 18: "右手小指",
        19: "左手拇指", 20: "右手拇指", 21: "左手掌心", 22: "右手掌心",
        23: "左髖", 24: "右髖", 25: "左膝蓋", 26: "右膝蓋",
        27: "左腳踝", 28: "右腳踝", 29: "左腳後跟", 30: "右腳後跟",
        31: "左腳拇指", 32: "右腳拇指"
    }

    joint_options = [f"{i}: {joint_names[i]}" for i in range(33)]
    selected_joint_str = st.selectbox("選擇一個關節", joint_options)
    selected_joint_idx = int(selected_joint_str.split(":")[0])

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1.0 / fps if fps > 0 else 0.03

    joint_series = []

    # 分兩欄顯示：左邊影片，右邊圖表
    col1, col2 = st.columns(2)
    video_display = col1.empty()
    col2.subheader(f"關節 {selected_joint_idx}: {joint_names[selected_joint_idx]} 位置變化 (x/y/z)")
    chart_container = col2.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            j = results.pose_landmarks.landmark[selected_joint_idx]
            joint_series.append({"x": j.x, "y": j.y, "z": j.z})
        else:
            joint_series.append({"x": None, "y": None, "z": None})

        video_display.image(frame, channels="BGR")

        df = pd.DataFrame(joint_series)
        if len(df) > 100:
            df = df.tail(100)
        chart_container.line_chart(df)

        time.sleep(delay)

    cap.release()
    st.success("分析完成！")
