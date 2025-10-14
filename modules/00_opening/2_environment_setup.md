# Environment Setup Guide

Welcome! 🎉  
Follow the steps below to set up your exercise environment and start working with JupyterLab for the course.

---

## 1. Prerequisites

Make sure your system has the following installed **before class**:

- **Git**
- **Docker** (Docker Desktop on Windows/Mac, Docker Engine on Linux)

You can verify by running:
```bash
git --version
docker --version
```

## 2. Clone the course repository

Open a terminal and run:

```bash
git clone https://github.com/yongjunshin/Introduction_to_Software_Testing_for_Safe_AI.git
cd Introduction_to_Software_Testing_for_Safe_AI
```

This will create a local copy of all course materials.

## 3. Pull the prepared Docker image

The instructor has prepared a Docker image with all required libraries.
Download it with:

```bash
docker pull <DOCKERHUB_ID>/ai-testing:final-2025-10-01
```

## 4. Start JupyterLab

Run the provided script:

```bash
./scripts/run_jupyter.sh
```

💡 If you see a permission denied error the first time, run:

```bash
chmod +x scripts/run_jupyter.sh
```

## 5. Open Jupyter in your browser

After running the script, open your browser at:
👉 **http://127.0.0.1:8888**

You will see the course notebooks under the `modules/` folder.

## 6. Verify your environment

Open `modules/module00/hello.ipynb` and run all cells.
It should print out versions of required libraries and show:

```
Python version: 3.10.18 (main, ...)

Testing library imports and versions...
==================================================
✓ torch           | version: 2.3.1+cpu
✓ torchvision     | version: 0.18.1+cpu
✓ numpy           | version: 1.26.4
✓ pandas          | version: 2.2.2
✓ matplotlib      | version: 3.8.4
✓ sklearn         | version: 1.4.2
✓ jupyterlab      | version: 4.2.3
✓ ipywidgets      | version: 8.1.2
✓ httpx           | version: 0.28.1
==================================================
Import test complete!
```

---

**Ready to start?** 🚀  
Once you see all the checkmarks in the environment verification, you're all set for the course!
