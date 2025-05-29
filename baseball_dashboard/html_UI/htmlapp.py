from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import threading
import time
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global vars to share state
video_path = None
processing_thread = None
processing = False
selected_joint_idx = 0

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

@app.route('/')
def index():
    return render_template('index.html', joint_names=joint_names)

@app.route('/upload', methods=['POST'])
def upload():
    global video_path, processing, processing_thread

    f = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, 'uploaded.mp4')
    f.save(video_path)

    # 開啟串流分析線程
    if processing_thread is None or not processing_thread.is_alive():
        processing = True
        processing_thread = threading.Thread(target=process_video)
        processing_thread.start()

    return {"success": True}

@app.route('/video_feed')
def video_feed():
    # 回傳串流的 Motion JPEG 影片
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('select_joint')
def handle_select_joint(data):
    global selected_joint_idx
    selected_joint_idx = int(data['joint'])
    print(f"Selected joint changed to: {selected_joint_idx}")

def gen_frames():
    """產生含骨架標記的影像串流"""
    global video_path, processing

    cap = cv2.VideoCapture(video_path) if video_path else None
    while processing and cap and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        ret2, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(1/30)  # 控制約30fps

def process_video():
    """讀影片，分析骨架關節座標，透過 socketio 發送資料"""
    global video_path, processing, selected_joint_idx

    cap = cv2.VideoCapture(video_path) if video_path else None
    if not cap or not cap.isOpened():
        return

    while processing and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        # 傳送指定關節座標給前端
        if results.pose_landmarks:
            j = results.pose_landmarks.landmark[selected_joint_idx]
            data = {'x': j.x, 'y': j.y, 'z': j.z}
        else:
            data = {'x': None, 'y': None, 'z': None}

        socketio.emit('joint_data', data)
        socketio.sleep(1/30)  # 保持與影像 fps 同步

    cap.release()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
