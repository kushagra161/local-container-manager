# Assessment 1 - Analysis and Requirements

**Student:** Kushagra Kaushik | **Roll No:** S24BCAU0112  
**Course:** CBCA321 – Software Containerization in DevOps  
**Faculty:** Omkarendra Tiwari | **Submission:** 15/09/2026

---

## 1. Problem Understanding

Docker is the industry standard for containerization, but its CLI has a steep learning curve for beginners. Commands like `docker run -d --name web -p 8080:80 nginx` are not intuitive, leading to errors and frustration.

**Problem Statement:**  
Build a tool that abstracts Docker commands into a simple interface, making container management accessible to students and beginners learning DevOps.

---

## 2. Input / Processing / Output

| Stage | Description |
|-------|-------------|
| **Input** | Container name, Docker image, port mapping, environment variables |
| **Processing** | LCM validates inputs → constructs Docker CLI command → executes via subprocess |
| **Output** | Human-readable status, container ID, table-formatted container list |

---

## 3. Actors / Stakeholders

| Actor | Role |
|-------|------|
| **User (Beginner/Student)** | Primary user who interacts with LCM CLI |
| **Project Developer** | Maintains and extends LCM |
| **Container Runtime (Docker)** | Backend that executes container operations |
| **Faculty / Evaluator** | Reviews project code and documentation |

---

## 4. Technology Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| Language | Python 3.8+ | Easy to learn, rich stdlib |
| Container Runtime | Docker | Industry standard |
| Docker Integration | subprocess (Docker CLI) | No extra dependencies needed |
| CLI | argparse | Built into Python stdlib |
| Testing | unittest + pytest | Industry standard testing |
| VCS | Git + GitHub | Version control + collaboration |
| CI/CD | GitHub Actions | Free for open source |

---

## 5. Functional Requirements

| ID | Requirement | Priority |
|----|------------|---------|
| FR1 | User can list all running containers | High |
| FR2 | User can list all containers (including stopped) | High |
| FR3 | User can run a new container with image, name, port | High |
| FR4 | User can start a stopped container | High |
| FR5 | User can stop a running container | High |
| FR6 | User can inspect container details (IP, status, image) | Medium |
| FR7 | User can remove a container with confirmation | High |
| FR8 | User can view container logs | Medium |
| FR9 | User can list local Docker images | Medium |
| FR10 | User can pull images from Docker Hub | Medium |
| FR11 | System displays clear error messages | High |

---

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR1 | Response time for list operations | < 2 seconds |
| NFR2 | Error messages must be human-readable | 100% |
| NFR3 | Unit test coverage | ≥ 80% |
| NFR4 | Compatible with Python 3.8+ | Yes |
| NFR5 | Works on Windows, Linux, macOS | Yes |
| NFR6 | CI/CD pipeline passes on all commits | Yes |

---

## 7. Assumptions & Constraints

- Docker Desktop must be installed and running on the host machine
- User has basic Python knowledge
- Internet connection required for pulling images
- Tool does not manage Docker networks or volumes (out of scope for Assessment 1)
