# scripts/download_small_mnist_data.py
import os, random, torch
from torchvision import datasets, transforms
from pathlib import Path

# 프로젝트 root 기준으로 artifacts/data 경로 설정
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "modules" / "exercise_artifacts" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(f"Saving MNIST subsets to: {DATA_DIR}")

# 1. MNIST 다운로드
transform = transforms.ToTensor()
train_ds = datasets.MNIST(root=PROJECT_ROOT/"data_raw", train=True, download=True, transform=transform)
test_ds  = datasets.MNIST(root=PROJECT_ROOT/"data_raw", train=False, download=True, transform=transform)

# 2. 랜덤 subset 선택
train_idx = random.sample(range(len(train_ds)), 1000)
test_idx  = random.sample(range(len(test_ds)), 200)

def extract(ds, indices):
    images = []
    labels = []
    for idx in indices:
        x, y = ds[idx]
        images.append(x)
        labels.append(y)
    return torch.stack(images), torch.tensor(labels)

train_x, train_y = extract(train_ds, train_idx)
test_x,  test_y  = extract(test_ds, test_idx)

# 3. 저장
torch.save({"images": train_x, "labels": train_y}, DATA_DIR/"mnist_train_1k.pt")
torch.save({"images": test_x,  "labels": test_y},  DATA_DIR/"mnist_test_200.pt")

print("Done!")
print("Train subset:", train_x.shape, train_y.shape)
print("Test subset:",  test_x.shape,  test_y.shape)
