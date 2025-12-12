# modules/exercise_artifacts/code/mnist_model.py
import torch
import torch.nn as nn
import torch.nn.functional as F


class MnistCNN(nn.Module):
    """MNIST 28x28용 최소한의 간단 CNN 모델."""

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1)   # [B,8,28,28]
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1)  # [B,16,14,14]
        self.fc1 = nn.Linear(16 * 7 * 7, 32)
        self.fc2 = nn.Linear(32, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)    # [B,8,14,14]
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)    # [B,16,7,7]
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)


def load_trained_model(weights_path: str, device: str = "cpu") -> nn.Module:
    """
    학습된 model weight를 로드해서 모델 객체를 반환하는 최소 헬퍼 함수.

    Args:
        weights_path (str): 저장된 .pt 모델 weight 파일 경로
        device (str): "cpu" 또는 "cuda"

    Returns:
        nn.Module: weight가 로드되어 eval 모드로 설정된 모델
    """
    model = MnistCNN()
    state = torch.load(weights_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.to(device)
    model.eval()   # inference/testing 모드
    return model
