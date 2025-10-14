# Python 3.10 slim 베이스 (3.11, 3.12도 가능)
FROM python:3.10-slim

# 시스템 패키지 (PyTorch, matplotlib 등에서 필요한 라이브러리)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential libgl1 libgomp1 ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --no-cache-dir -U pip

# requirements.txt 복사 & 설치
WORKDIR /workspace
COPY env/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt


# ------------------------------------------------------
# JupyterLab system default settings (Markdown Preview)
# ------------------------------------------------------
# Make sure directory exists, then copy overrides.json
RUN mkdir -p /usr/local/share/jupyter/lab/settings
COPY env/jlab-overrides/overrides.json /usr/local/share/jupyter/lab/settings/overrides.json

# Jupyter 포트 오픈
EXPOSE 8888

# 기본 실행 = JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
