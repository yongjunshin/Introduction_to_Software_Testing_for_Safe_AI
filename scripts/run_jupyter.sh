#!/usr/bin/env bash
set -e

# 컨테이너 이름
CONTAINER_NAME="ai-testing-lab"
# 로컬 우선: 같은 이름이 있으면 로컬 빌드, 없으면 Hub (docker run 시 없으면 pull)
DOCKERHUB_IMAGE="yongjunshin/ai-testing:latest"
if docker image inspect ai-testing >/dev/null 2>&1; then
  IMAGE_NAME="ai-testing"
  echo "[INFO] Using local image: $IMAGE_NAME"
else
  IMAGE_NAME="$DOCKERHUB_IMAGE"
  echo "[INFO] Local 'ai-testing' not found; using $IMAGE_NAME (Docker pulls if not cached)"
fi
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