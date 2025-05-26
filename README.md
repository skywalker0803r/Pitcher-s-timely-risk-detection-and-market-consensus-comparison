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
git clone https://github.com/your-username/Pitcher-s-timely-risk-detection-and-market-consensus-comparison.git
cd Pitcher-s-timely-risk-detection-and-market-consensus-comparison
```
### 2️⃣ 建立 Conda 環境並啟用
```bash
conda create -n pitcher_pose_env python=3.9
conda activate pitcher_pose_env
```

