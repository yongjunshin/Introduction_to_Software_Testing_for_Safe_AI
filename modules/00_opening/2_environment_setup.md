# **Environment Setup**

Follow the steps below to set up your exercise environment and start working with JupyterLab for the course.

---

## **1. Prerequisites**

Make sure your system has the following installed **before class**:

- **Git**
- **Docker** (Docker Desktop on Windows/Mac, Docker Engine on Linux)

You can verify by running:
```bash
git --version
docker --version
```

---

## **2. Clone the course repository**

Open a terminal and run:

```bash
git clone https://github.com/yongjunshin/Introduction_to_Software_Testing_for_Safe_AI.git
cd Introduction_to_Software_Testing_for_Safe_AI
```

This will create a local copy of all course materials.

---

## **3. Set up the Docker environment**

You have two options to get the required Docker image:

### **Option A: Pull the prepared Docker image (Recommended)**

The instructor has prepared a Docker image with all required libraries.
Download it with:

```bash
docker pull <DOCKERHUB_ID>/ai-testing
```

### **Option B: Build the image locally**

If you prefer to build the image yourself, run:

```bash
docker build -t ai-testing -f env/Dockerfile .
```

This will create a local Docker image named `ai-testing` with all the required dependencies.

---

## **4. Start JupyterLab**

Run the provided script:

```bash
./scripts/run_jupyter.sh
```

💡 **Troubleshooting**: If you see a permission denied error the first time, run:

```bash
chmod +x scripts/run_jupyter.sh
```

This script will:
- Start a Docker container with the `ai-testing` image
- Mount your current directory to `/workspace` in the container
- Launch JupyterLab on port 8888

---

## **5. Open Jupyter in your browser**

After running the script, open your browser at:
👉 **http://localhost:8888/lab**

You will see the course notebooks under the `modules/` folder.

---

## **6. Verify your environment**

To ensure everything is working correctly:

1. Open `modules/00_opening/exercises/hello.ipynb` in JupyterLab
2. Run all cells (Cell → Run All or Shift+Enter for each cell)
3. You should see output similar to the following:

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

**Ready to start?** 🚀  
Once you see all the checkmarks in the environment verification, you're all set for the course!

---

👉 **Move on to next section**: [Software Engineering Fundamentals](../01_fundamentals/1_se_fundamentals.md)