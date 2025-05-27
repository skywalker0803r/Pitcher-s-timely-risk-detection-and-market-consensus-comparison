# Pitcher-s-timely-risk-detection-and-market-consensus-comparison

## 🧠 專案簡介

本專案旨在透過姿勢偵測技術，分析棒球投手的投球動作是否符合標準姿勢，從而及早發現潛在的受傷風險或技術偏差。我們使用 MediaPipe 擷取投手的骨架關鍵點，並使用時序卷積神經網路（Temporal Convolutional Network, TCN）進行姿勢分類。

---

## 📦 環境需求

- Python 3.9（建議使用 Anaconda 管理環境）
- OpenCV
- MediaPipe
- PyTorch
- numpy、pandas 等相關科學運算套件

---

## 🛠️ 安裝教學

請依照以下步驟安裝並執行本專案：

### 1️⃣ Clone 專案

```bash
git clone https://github.com/skywalker0803r/Pitcher-s-timely-risk-detection-and-market-consensus-comparison.git
cd Pitcher-s-timely-risk-detection-and-market-consensus-comparison
```
### 2️⃣ 建立 Conda 環境並啟用
```bash
conda create -n pitcher_pose_env python=3.9
conda activate pitcher_pose_env
```
### 3️⃣ 安裝套件
```bash
pip install -r requirements.txt
```
### 🚀 使用方式
1️⃣ 產生模型
首先執行 model.py 訓練並產生模型檔案 model.pth：
```bash
python model.py
```
### 2️⃣ 進行影片推論
使用已訓練的模型進行影片分析與姿勢分類：
```bash
python infer_video.py
```
輸出將會在影片中標註判斷結果，並可視化姿勢分類結果
### 📁 專案架構
```bash
Pitcher-s-timely-risk-detection-and-market-consensus-comparison/
├── model.py                 # 模型訓練程式碼，產生 model.pth
├── infer_video.py           # 讀取影片並進行姿勢推論
├── train_data/              # 訓練數據
├── model.pth                # 模型
├── requirements.txt         # 所需套件
├── train.py                 # 模型訓練
├── Proof of Concept         # 概念驗證
├── utils                    # 工具函數
└── README.md                # 使用說明文件
```

<video src='https://github.com/skywalker0803r/Pitcher-s-timely-risk-detection-and-market-consensus-comparison/blob/main/output_with_pose_and_label.mp4' width=180/>
