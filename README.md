# Local Container Manager (LCM)

> **Student:** Kushagra Kaushik | **Roll No:** S24BCAU0112  
> **Course:** CBCA321 – Software Containerization in DevOps  
> **Faculty:** Omkarendra Tiwari  

---

## 📌 What is LCM?

**Local Container Manager (LCM)** is a beginner-friendly command-line tool built in Python that wraps Docker CLI commands into simple, human-readable operations.

Instead of memorizing complex Docker commands, beginners can use LCM to:
- 📋 List running/all containers
- ▶️ Run new containers (with image, name, port, env vars)
- ⏸ Start / Stop containers
- 🔍 Inspect container details
- 🗑 Remove containers
- 📜 View container logs
- 🖼 Manage Docker images

---

## 🗂 Project Structure

```
local-container-manager/
├── src/
│   ├── __init__.py
│   ├── container_manager.py   ← Core Docker wrapper logic
│   ├── cli.py                 ← CLI interface (argparse)
│   └── utils.py               ← Helper utilities
├── tests/
│   ├── test_container_manager.py  ← Unit tests for core logic
│   └── test_utils.py              ← Unit tests for utils
├── .github/
│   └── workflows/
│       └── ci.yml             ← GitHub Actions CI/CD pipeline
├── docs/
│   ├── assessment1_requirements.md
│   └── assessment2_architecture.md
├── main.py                    ← Entry point
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.8+
- Docker Desktop installed and running
- Git

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/local-container-manager.git
cd local-container-manager
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install LCM as a CLI tool

```bash
pip install -e .
```

Now you can use `lcm` from anywhere!

---

## 💻 Usage

### List Containers

```bash
# Show running containers
python main.py list

# Show ALL containers (including stopped)
python main.py list --all
```

### Run a Container

```bash
# Run nginx in background
python main.py run nginx --name web -p 8080:80

# Run with environment variables
python main.py run postgres --name mydb -p 5432:5432 -e POSTGRES_PASSWORD=secret

# Run interactively (foreground)
python main.py run ubuntu --name myubuntu -i
```

### Start / Stop Containers

```bash
python main.py start web
python main.py stop web
```

### Inspect a Container

```bash
# Basic info
python main.py inspect web

# Full JSON output
python main.py inspect web --json
```

### Remove a Container

```bash
# Remove (asks for confirmation)
python main.py remove web

# Force remove (even if running)
python main.py remove web --force
```

### View Logs

```bash
# Last 50 lines (default)
python main.py logs web

# Custom tail
python main.py logs web --tail 100
```

### Manage Images

```bash
# List local images
python main.py images

# Pull an image
python main.py pull python:3.10
python main.py pull nginx
```

---

## 🧪 Running Tests

```bash
# Run all unit tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for automated testing on every push/PR.

The pipeline (`.github/workflows/ci.yml`) runs:
1. **Lint check** using `flake8`
2. **Unit tests** using `pytest` with coverage
3. Tests on Python **3.8, 3.10, 3.11**

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language  | Python 3.8+ |
| Docker Integration | Docker CLI (subprocess) |
| CLI Framework | argparse (stdlib) |
| Testing | unittest, pytest |
| CI/CD | GitHub Actions |
| Version Control | Git + GitHub |

---

## 📋 Functional Requirements

| # | Feature | Status |
|---|---------|--------|
| FR1 | List running containers | ✅ |
| FR2 | List all containers | ✅ |
| FR3 | Run container with image/name/port | ✅ |
| FR4 | Start stopped container | ✅ |
| FR5 | Stop running container | ✅ |
| FR6 | Inspect container details | ✅ |
| FR7 | Remove container | ✅ |
| FR8 | View container logs | ✅ |
| FR9 | List local images | ✅ |
| FR10 | Pull image from Docker Hub | ✅ |
| FR11 | Error handling & clear messages | ✅ |

---

## 📝 Assessment Details

| Assessment | Description | Status |
|-----------|-------------|--------|
| Assessment 1 | Problem Analysis & Requirements | ✅ Submitted |
| Assessment 2 | Architecture & Implementation | 🔄 In Progress |
| Assessment 3 | Feature Implementation + Unit Tests | 🔄 In Progress |

---

## 📄 License

MIT License © 2026 Kushagra Kaushik
