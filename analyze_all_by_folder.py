import os
import subprocess


# 檢查資料夾是否同時包含影片（.mp4）與 CSV（.csv）
def is_valid_data_folder(folder_path):
    has_csv = any(f.endswith(".csv") for f in os.listdir(folder_path))
    has_video = any(f.endswith(".mp4") for f in os.listdir(folder_path))
    return has_csv and has_video


# 執行分析流程：對資料夾中的每一球影片進行四點特徵擷取
def run_analysis_on_folder(folder_path):
    print(f"分析資料夾：{folder_path}")

    # 建立輸出資料夾：features/
    output_dir = os.path.join(folder_path, "features")
    os.makedirs(output_dir, exist_ok=True)

    # 逐一處理該資料夾下的影片
    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            video_path = os.path.join(folder_path, file)
            basename = os.path.splitext(file)[0]  # 例如 pitch_0001
            feature_path = os.path.join(output_dir, f"{basename}_keyframe_feats.npy")

            # 如果已經存在對應的特徵檔案，略過
            #if os.path.exists(feature_path):
            #    print(f"略過已處理影片：{file}")
            #    continue

            # 呼叫 pose_extractor_with_keyframes.py
            subprocess.run(
                ["python", "pose_extractor_with_keyframes.py", video_path, output_dir]
            )


# 遍歷 data/ 資料夾下的每個子資料夾（投手 × 球種）
if __name__ == "__main__":
    base_dir = "data"
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        # 只針對同時有影片與 CSV 的資料夾進行處理
        if os.path.isdir(folder_path) and is_valid_data_folder(folder_path):
            run_analysis_on_folder(folder_path)