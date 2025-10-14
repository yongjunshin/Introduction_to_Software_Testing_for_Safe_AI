#!/usr/bin/env bash
set -e

# 컨테이너 이름
CONTAINER_NAME="ai-testing-lab"
# 이미지 이름 (빌드할 때 태그한 이름)
IMAGE_NAME="ai-testing"
# 포트 설정 (겹치면 8890 등으로 바꿔도 됨)
PORT=8888

echo "[INFO] Starting JupyterLab from image: $IMAGE_NAME"
echo "[INFO] Mapping local folder $(pwd) to /workspace in container"
echo "[INFO] Access at http://127.0.0.1:$PORT (no token)"

docker run -it --rm \
  --name "$CONTAINER_NAME" \
  -p $PORT:8888 \
  -v "$(pwd)":/workspace \
  "$IMAGE_NAME" \
  jupyter lab --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token=''