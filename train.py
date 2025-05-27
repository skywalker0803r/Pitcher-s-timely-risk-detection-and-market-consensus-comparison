import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
import matplotlib.pyplot as plt
from model import TCNClassifier

# ===== 參數設定 =====
BATCH_SIZE = 1
EPOCHS = 30
LEARNING_RATE = 1e-3
TEST_RATIO = 0.2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ===== 載入資料 =====
data = np.load('train_data/all_data.npy', allow_pickle=True)  # shape: (batch, frames, features)
X = torch.tensor(data[:, :, :], dtype=torch.float32)  # 保留所有特徵
B,T,N = X.shape[0],X.shape[1],X.shape[2]
X = X.reshape(B,N,T)
y = torch.randint(0, 2, (X.shape[0],), dtype=torch.long)

# ===== 製作 Dataset 與 DataLoader =====
dataset = TensorDataset(X, y)
test_size = int(TEST_RATIO * len(dataset))
train_size = len(dataset) - test_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# ===== 模型與損失函數設定 =====
input_size = X.shape[1]
num_classes = len(torch.unique(y))
model = TCNClassifier(input_size=input_size, num_classes=num_classes).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ===== 訓練與評估迴圈 =====
train_losses, test_losses = [], []
train_accuracies, test_accuracies = [], []

for epoch in range(EPOCHS):
    model.train()
    train_loss, correct, total = 0.0, 0, 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    avg_train_loss = train_loss / total
    train_acc = correct / total
    train_losses.append(avg_train_loss)
    train_accuracies.append(train_acc)

    # ===== 評估模型 =====
    model.eval()
    test_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            test_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    avg_test_loss = test_loss / total
    test_acc = correct / total
    test_losses.append(avg_test_loss)
    test_accuracies.append(test_acc)

    print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {avg_train_loss:.4f} | Acc: {train_acc:.4f} | Test Loss: {avg_test_loss:.4f} | Acc: {test_acc:.4f}")

# ===== 繪圖 =====
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label="Train Loss")
plt.plot(test_losses, label="Test Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.title("Loss Curve")

plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label="Train Accuracy")
plt.plot(test_accuracies, label="Test Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Accuracy Curve")

plt.tight_layout()
plt.savefig("training_curve.png")
plt.show()

# ===== 儲存模型 =====
torch.save(model.state_dict(), "tcn_model.pth")
print("✅ 模型已保存為 tcn_model.pth")
