[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](/fork) ![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/ahmedmokhalaf/devops-hands-on-project-hivebox?style=for-the-badge&logoColor=logoColor%3Dwhite&label=ossf%20scorecard) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ahmedmokhalaf/devops-hands-on-project-hivebox/scorecard.yml?style=for-the-badge&logo=github&logoColor=white&label=Scorecard%20supply-chain%20security) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ahmedmokhalaf/devops-hands-on-project-hivebox/ci.yml?style=for-the-badge&logo=github&logoColor=white&label=CI%20Pipeline) 



# HiveBox - DevOps End-to-End Hands-On Project
## 🐝 HiveBox Project – Phase 4: BuildingExpand - Constructing a Shell


<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox" style="display: block; padding: .5em 0; text-align: center;">
    <img alt="HiveBox - DevOps End-to-End Hands-On Project" border="0" width="90%" src="https://devopsroadmap.io/img/projects/hivebox-devops-end-to-end-project.png" />
  </a>
</p>

---


## 📌 Project Overview

- **Project Name:** HiveBox

- **Phase 4:** Expand-Constructing a Shell

- **Roadmap Module:** [Expand-Constructing a Shell](https://devopsroadmap.io/foundations/module-04/)

- **Objective:** Extend the application by integrating environment configurability, Kubernetes deployment, Prometheus metrics, and basic GitHub CI/CD workflows.

---

## 🚀 Features

- Dynamic configuration via environment variables.
- Prometheus-compatible metrics endpoint.
- Temperature status classification.
- Kubernetes deployment with KIND and Ingress.
- Optimized Docker build process.
- Extended CI/CD pipeline with static analysis and testing.

---

## 🎯 Goals for Phase 4
 1 - Make Application Configurable via Env Vars

- Configure senseBox IDs dynamically from environment variables.

 2 - Metrics Endpoint

- Implement /metrics endpoint to expose Prometheus metrics (using Starlette or Prometheus FastAPI exporter).

3 - Extend /temperature Endpoint

- Add status field based on average temperature:

  - <10°C → Too Cold

  - 11–36°C → Good

  - 37°C → Too Hot

4 - Kubernetes Deployment

  - Create KIND config with Ingress-Nginx.

  - Create basic Kubernetes manifests: Deployment, Service, Ingress.

5- Improve Containers

  - Apply Docker best practices (multi-stage build, smaller images).

 6- Extend CI Pipeline 

  - Lint Python code and Dockerfile.

  - Build and push Docker image.

  - Run integration tests.

  - Verify /version and /temperature endpoints.

  - Include SonarQube and Terrascan static analysis checks.


---

## ⚙️ Prerequisites & Development Tools

Before setting up the project, ensure the following tools are installed on your system:

- **Python**: Version 3.8 or higher. [Download Python](https://www.python.org/downloads/)
- **Docker**: For containerization. [Install Docker](https://docs.docker.com/get-docker/)
- **Kubernetes (KIND)**: For local Kubernetes cluster setup. [Install KIND](https://kind.sigs.k8s.io/docs/user/quick-start/)
- **kubectl**: Kubernetes command-line tool. [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
- **Make**: Build automation tool (optional but recommended). [Install Make](https://www.gnu.org/software/make/)

- **Prometheus**: Monitoring system and time series database. [Download Prometheus](https://prometheus.io/download)
- **Grafana**: Analytics and monitoring platform for visualizing metrics. [Install Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)

---

## 📦 Installing Dependencies

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ahmedmokhalaf/devops-hands-on-project-hivebox.git
   cd hivebox
   ```

2. **Set Up a Virtual Environment**

   Create and activate a virtual environment to manage project dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies**

   Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, for a more comprehensive setup including optional dependencies:

   ```bash
   pip install "fastapi[all]" uvicorn pytest
   ```
---



## 🚀 Getting Started

1. **Configure Environment Variables**

   Create a `.env` file in the project root with the following content:

   ```env
   VERSION=0.2.0
   BOX_IDS=5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c
   SENSEBOX_API=https://api.opensensemap.org
   ```

2. **Run the Application Locally**

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```



---

## 🐳 Docker Deployment

1. **Build the Docker Image**

   ```bash
   docker build -t hivebox:0.2.0 .
   ```

2. **Run the Docker Container**

   ```bash
   docker run --env-file .env -p 8000:8000 hivebox:0.2.0
   ```

   The application will be accessible at [http://localhost:8000](http://localhost:8000).

---

## ☸️ Kubernetes Deployment with KIND

1. **Create a KIND Cluster**

   ```bash
   kind create cluster --name hivebox-cluster
   ```

2. **Apply Kubernetes Manifests**

   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   kubectl apply -f k8s/ingress.yaml
   ```

3. **Access the Application**

   Configure your `/etc/hosts` file or DNS to route to the Ingress controller and access the application via the defined Ingress rules.

---

## 🧪 Testing

Run the test suite using `pytest`:

```bash
pytest --cov=app
```

This command will execute all unit and integration tests and provide a coverage report.

---

## 📈 Metrics

The `/metrics` endpoint exposes Prometheus-compatible metrics, including:

- HTTP request counts
- Application version
- Custom application-specific metrics

To scrape these metrics, configure Prometheus to target the `/metrics` endpoint.

---

## 🛠️ CI/CD Pipeline

The CI/CD pipeline includes:

- **Linting**: Python code and Dockerfile linting.
- **Testing**: Unit and integration tests.
- **Static Analysis**: SonarQube and Terrascan checks.
- **Docker Build**: Build and push Docker images.
- **Deployment**: Deploy to Kubernetes cluster.

---
