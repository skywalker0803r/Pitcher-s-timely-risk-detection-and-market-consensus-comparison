import torch
import torch.nn as nn

class TCNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dilation):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size,
                              padding='same',
                              dilation=dilation)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.residual = nn.Conv1d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()

    def forward(self, x):
        out = self.conv(x)
        out = self.relu(out)
        out = self.dropout(out)
        return out + self.residual(x)

class TCNClassifier(nn.Module):
    def __init__(self, input_size=99, num_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            TCNBlock(input_size, 64, 3, 1),
            TCNBlock(64, 64, 3, 2),
            TCNBlock(64, 64, 3, 4),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.net(x)

# ✅ 當直接執行時：儲存一個隨機初始化的模型
if __name__ == "__main__":
    model = TCNClassifier(input_size=99, num_classes=2)
    torch.save(model.state_dict(), "model.pth")
    print("✅ 模型結構已儲存為 model.pth（尚未訓練）")
    x = torch.randn(10, 99, 100)  # batch=1, channel=99, seq_len=30
    out = model(x)
    print(out.shape)  # 預期輸出 torch.Size([1, 2])
