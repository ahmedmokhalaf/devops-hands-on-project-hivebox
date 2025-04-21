[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](/fork)

# HiveBox - DevOps End-to-End Hands-On Project
## 🐝 HiveBox Project – Phase 2: DevOps Core Fundamentals


<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox" style="display: block; padding: .5em 0; text-align: center;">
    <img alt="HiveBox - DevOps End-to-End Hands-On Project" border="0" width="90%" src="https://devopsroadmap.io/img/projects/hivebox-devops-end-to-end-project.png" />
  </a>
</p>

---

Welcome to Phase 2 of the **HiveBox** project In this phase, we focus on establishing core DevOps competencies, including implementing a basic Python application, containerizing it with Docker, and performing local testing

---

## 📌 Project Overview

- **Project Name:** HiveBox
- **Phase 2:**  – DevOps Core
- **Roadmap Module:** [Module 2: Basics - DevOps Core](https://devopsroadmap.io/foundations/module-02/)
- **Objective:** Develop a foundational Python application, containerize it using Docker, and ensure it functions correctly through local testing.

---

## 🎯 Goals for Phase 2

1. **Implement Initial Application:**
  - Create a Python function that prints the application version.
  - Adopt Semantic Versioning, starting with version `v0.0.1`.

2. **Containerize the Application:**
  - Write a `Dockerfile` to containerize the Python application.
  - Build and run the Docker image locally.

3. **Test the Containerized Application:**
  - Execute the Docker container to verify it outputs the correct version.
  - Document the testing process for future reference.

---

## 🛠️ Getting Started

### 1. Clone the Repository

Ensure you have forked the HiveBox project repository:


### Clone application
```bash

git clone https://github.com/ahmedmokhalaf/devops-hands-on-project-hivebox.git
cd hivebox
```
### Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -t hivebox:0.0.1 .
```


This command creates a Docker image tagged as `hivebox:0.0.1`.

### Run the Docker Container

Execute the Docker container:

```bash
docker run  hivebox:0.0.1
```

You should see the following output:

`HiveBox Application Version: 0.0.1`


---


## 📚 Resources

- **Semantic Versioning:** [semver.org](https://semver.org/)

- **Docker Documentation:** [Docker Docs](https://docs.docker.com/)

- **Python Official Website:** [Python Docs](https://www.python.org/)

---

## ✅ Deliverables for Phase2

- A Python script (`app.py`) that prints the application version.

- A `Dockerfile` that containerizes the application.

- A successfully built Docker image tagged as `hivebox:0.0.1`.

- Documentation outlining the steps to build and run the Docker container.

---
