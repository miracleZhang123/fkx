import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import sys
import os

# 将 backend 路径加入 sys.path 以便导入模型定义
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from core.models import EmotionViT

# 模拟一个数据集类 (实际中你需要在这里读取 FER2013 CSV 或图片文件夹)
class DummyImageDataset(Dataset):
    def __init__(self, size=100):
        self.size = size
    def __len__(self): return self.size
    def __getitem__(self, idx):
        # 模拟 3通道 48x48 图像
        return torch.randn(3, 48, 48), torch.randint(0, 7, (1,)).item()

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training Vision Transformer on {device}...")

    # 初始化模型
    model = EmotionViT(num_classes=7).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    # 数据加载
    dataset = DummyImageDataset(size=200) # 替换为真实 Dataset
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    # 训练循环
    model.train()
    for epoch in range(5): # 演示训练5轮
        total_loss = 0
        for imgs, labels in dataloader:
            imgs, labels = imgs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(dataloader):.4f}")

    # 保存模型 (这一点非常重要，后端要用)
    save_path = "../backend/weights/vit_emotion.pth"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train()