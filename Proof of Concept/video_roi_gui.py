import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

def select_video():
    path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if path:
        video_path_var.set(path)

def process_video():
    video_path = video_path_var.get()
    if not video_path or not os.path.exists(video_path):
        messagebox.showerror("錯誤", "請選擇有效的影片檔案")
        return

    try:
        start_time = float(start_time_var.get())
        end_time = float(end_time_var.get())
        if end_time <= start_time:
            raise ValueError
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的開始與結束時間（秒）")
        return

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 讀一幀供框選
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("錯誤", "無法讀取影片")
        cap.release()
        return

    roi = cv2.selectROI("選擇錄製區域", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("選擇錄製區域")
    x, y, w, h = map(int, roi)

    output_path = os.path.splitext(video_path)[0] + f"_cropped_{int(start_time)}_{int(end_time)}.mp4"
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    # 重新定位
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_num = start_frame
    while frame_num < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        cropped = frame[y:y+h, x:x+w]
        out.write(cropped)
        frame_num += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("完成", f"影片儲存為：\n{output_path}")

# === 建立 GUI ===
root = tk.Tk()
root.title("影片區段與區域裁切工具")

video_path_var = tk.StringVar()
start_time_var = tk.StringVar(value="10")
end_time_var = tk.StringVar(value="20")

tk.Label(root, text="影片檔案：").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=video_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="選擇影片", command=select_video).grid(row=0, column=2)

tk.Label(root, text="開始時間 (秒)：").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=start_time_var).grid(row=1, column=1)

tk.Label(root, text="結束時間 (秒)：").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=end_time_var).grid(row=2, column=1)

tk.Button(root, text="開始處理", command=process_video, bg="green", fg="white").grid(row=3, column=1, pady=10)

root.mainloop()
