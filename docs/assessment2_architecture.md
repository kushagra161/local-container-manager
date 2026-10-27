# Assessment 2 - Architecture & Implementation

**Student:** Kushagra Kaushik | **Roll No:** S24BCAU0112  
**Course:** CBCA321 – Software Containerization in DevOps

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User (Terminal)                    │
│              python main.py <command>                │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                   CLI Layer (cli.py)                 │
│  - Parses user commands via argparse                 │
│  - Validates arguments                               │
│  - Calls appropriate ContainerManager methods        │
│  - Formats and displays output                       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           Core Logic (container_manager.py)          │
│  - ContainerManager class                            │
│  - Constructs Docker CLI commands                    │
│  - Executes via subprocess                           │
│  - Returns structured result dicts                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Docker Engine (Docker CLI)              │
│  - Manages containers, images, networks              │
│  - Communicates with container runtime               │
└─────────────────────────────────────────────────────┘
```

---

## 2. Component Description

### `src/container_manager.py` — Core Logic
- Wraps Docker CLI via Python `subprocess`
- All methods return structured `dict` with `success`, `stdout`, `stderr`
- Docker availability is verified at initialization
- Methods: `list_containers`, `run_container`, `start_container`, `stop_container`, `inspect_container`, `remove_container`, `get_logs`, `list_images`, `pull_image`

### `src/cli.py` — CLI Interface
- Built with Python's `argparse`
- Subcommands: `list`, `run`, `start`, `stop`, `inspect`, `remove`, `logs`, `images`, `pull`
- Pretty table output for lists
- Color-coded success/error messages

### `src/utils.py` — Utilities
- Input validation (`validate_port_mapping`, `validate_container_name`)
- Display helpers (`format_size`, `truncate`, `print_table`)
- Data helpers (`parse_env_list`)

### `tests/` — Unit Tests
- Full mock-based tests using `unittest.mock`
- Tests for all methods in both success and failure scenarios
- Test coverage ≥ 80%

### `.github/workflows/ci.yml` — CI/CD
- Runs on every push to `main` and `develop`
- Tests on Python 3.8, 3.10, 3.11
- Lint with flake8 + tests with pytest

---

## 3. Data Flow Diagram

```
User Input: "lcm run nginx --name web -p 8080:80"
     │
     ▼
argparse parses: image="nginx", name="web", port="8080:80"
     │
     ▼
cli.cmd_run() called → ContainerManager.run_container("nginx", name="web", port="8080:80")
     │
     ▼
subprocess.run(["docker", "run", "-d", "--name", "web", "-p", "8080:80", "nginx"])
     │
     ▼
Docker Engine creates container → returns container ID
     │
     ▼
Result: {"success": True, "container_id": "abc1234567890"}
     │
     ▼
CLI prints: "✔ Container started! ID: abc123456789"
```

---

## 4. Error Handling Strategy

| Error Scenario | Handling |
|----------------|----------|
| Docker not installed | `EnvironmentError` on init |
| Docker not running | `EnvironmentError` on init |
| Container not found | Returns `{"success": False}` with error message |
| Image not found on Docker Hub | Returns failure result |
| Command timeout | Caught, returns `{"success": False, "stderr": "Command timed out"}` |
| Permission denied | Caught and returned as structured error |

---

## 5. Git Workflow

```
main       ← Production-ready code
develop    ← Integration branch
feature/*  ← Individual feature branches
```

Commit convention: `feat:`, `fix:`, `test:`, `docs:`, `chore:`
