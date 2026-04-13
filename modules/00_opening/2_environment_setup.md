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

## **3. Start JupyterLab (do this first)**

From the repository root, run:

```bash
./scripts/run_jupyter.sh
```

💡 **Troubleshooting**: If you see a permission denied error the first time, run:

```bash
chmod +x scripts/run_jupyter.sh
```

The script chooses the Docker image automatically:

- If you already have a **local** image named `ai-testing`, it uses that.
- Otherwise it uses the **course image on Docker Hub** (see `DOCKERHUB_IMAGE` in `scripts/run_jupyter.sh`). On first use, Docker will **pull** that image if it is not cached yet.

The script then:

- Starts a container and mounts your project folder to `/workspace` in the container
- Launches JupyterLab on port **8888**

You do **not** need to run `docker pull` or `docker build` beforehand unless something goes wrong (next step).

---

### **If the script fails: get the image explicitly**

Try the steps below if you see errors such as **image not found**, **pull denied**, **network timeout**, or **build needed** (for example, you are offline or want a self-built image).

#### **Option A: Pull the prepared image**

The instructor provides an image with all required libraries:

```bash
docker pull yongjunshin/ai-testing:latest
```



#### **Option B: Build the image locally**

```bash
docker build -t ai-testing -f env/Dockerfile .
```

This A and B creates a local image named `yongjunshin/ai-testing` or `ai-testing`. 

Run `./scripts/run_jupyter.sh` again.

---

## **4. Open Jupyter in your browser**

After running the script, open your browser at:
👉 **http://localhost:8888/lab**

You will see the course notebooks under the `modules/` folder.

---

## **5. Verify your environment**

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

👉 **Move on to exercise**: [Environment Setup Exercise](./exercises/hello.ipynb)

👉 **Move on to next section**: [Software Engineering Fundamentals](../01_fundamentals/1_se_fundamentals.md)