# Assessment-2: Architecture and First Deliverable

## 1. Project Title and Description

**Project Title:** Local Container Manager

**Description:**
Local Container Manager is a Python-based CLI + Web UI tool that simplifies Docker container management for beginners and students. Instead of memorizing complex Docker commands, users interact with a clean, intuitive interface to create, start, stop, inspect, and remove containers on their local system. The project bridges the gap between raw Docker CLI complexity and user-friendly container management.

---

## 2. Major Components

### UI Layer
- **CLI Interface** – Command-line interface built with Python's `argparse` and `rich` library for formatted, colorful terminal output.
- **Web Dashboard** – A lightweight Flask-based web UI displaying containers in a browser with action buttons.

### Logic Layer (Business Logic)
- **ContainerService** – Core service class that handles all container operations: list, create/run, start, stop, inspect, remove.
- **ErrorHandler** – Centralized error handling module that interprets Docker API errors and provides user-friendly messages.
- **CommandRouter** – Routes user input (CLI or Web) to the appropriate ContainerService method.

### Persistence (Data) Layer
- **Docker Engine (via Docker SDK)** – All container state is managed by Docker itself; no external database is needed.
- **Config File (`config.json`)** – Stores user preferences such as default Docker socket path and output verbosity level.
- **Log File (`app.log`)** – Persistent logs of all operations performed via the manager.

---

## 3. Architecture

**Architecture Pattern:** Layered Architecture (3-Tier)

```
+------------------------------+
|        UI Layer              |
|  CLI (argparse + rich)       |
|  Web Dashboard (Flask)       |
+------------------------------+
           |
           v
+------------------------------+
|      Logic Layer             |
|  ContainerService            |
|  ErrorHandler                |
|  CommandRouter               |
+------------------------------+
           |
           v
+------------------------------+
|     Persistence Layer        |
|  Docker SDK (docker-py)      |
|  config.json                 |
|  app.log                     |
+------------------------------+
           |
           v
+------------------------------+
|     Container Runtime        |
|  Docker Engine (local)       |
+------------------------------+
```

This layered architecture ensures clear separation of concerns and makes it easy to swap or extend individual layers independently.

---

## 4. Minimal Feature Set (First Deliverable – Next 4 Days)

The following minimal features will be implemented in the first deliverable:

1. **List Containers** – View all containers (running and stopped) with their ID, name, image, and status.
2. **Run/Create a Container** – Create and start a container from a specified Docker image.
3. **Stop a Container** – Stop a running container by name or ID.
4. **Start a Container** – Start a stopped container by name or ID.
5. **Remove a Container** – Remove a stopped container by name or ID.
6. **Inspect a Container** – View detailed information about a specific container.
7. **Error Handling** – Graceful messages when Docker is not running, container doesn't exist, or invalid input is provided.

---

## 5. Users Who Would Benefit

| User Type | Benefit |
|-----------|---------|
| Students learning Docker | Easier to learn Docker concepts without memorizing commands |
| Beginner developers | Quickly manage containers without CLI expertise |
| Educators/TAs | Demonstrate container lifecycle operations simply |
| DevOps learners | Understand container lifecycle before moving to advanced tools |

---

## 6. Components of First Deliverable

| Component | Description |
|-----------|-------------|
| `container_service.py` | Core logic for all Docker operations using docker-py SDK |
| `cli.py` | CLI entry point with argparse-based command routing |
| `error_handler.py` | Maps Docker API errors to user-friendly messages |
| `config.json` | Default configuration (Docker socket, log level) |
| `app.log` | Operation log file |
| `tests/test_container_service.py` | Unit tests for ContainerService |

---

## 7. Component Interfaces

### ContainerService (`container_service.py`)
```python
class ContainerService:
    def list_containers(self, all: bool = True) -> List[dict]
    def run_container(self, image: str, name: str = None, ports: dict = None) -> dict
    def start_container(self, container_id: str) -> bool
    def stop_container(self, container_id: str) -> bool
    def remove_container(self, container_id: str, force: bool = False) -> bool
    def inspect_container(self, container_id: str) -> dict
```

### CLI (`cli.py`)
```
usage: lcm <command> [options]

commands:
  list              List all containers
  run <image>       Run a container from an image
  start <id/name>   Start a stopped container
  stop <id/name>    Stop a running container
  remove <id/name>  Remove a container
  inspect <id/name> Show container details
```

### ErrorHandler (`error_handler.py`)
```python
class ErrorHandler:
    def handle(self, exception: Exception) -> str
    # Returns: User-friendly error string
```

---

## 8. Technology Stack

| Category | Technology |
|----------|-----------|
| Programming Language | Python 3.10+ |
| Container Runtime | Docker Engine (local) |
| Docker Integration | `docker` Python SDK (`docker-py`) |
| CLI Framework | `argparse` + `rich` (for formatted output) |
| Web UI (optional) | Flask + HTML/CSS/JS |
| Unit Testing | `pytest` + `unittest.mock` |
| Version Control | Git + GitHub |
| Logging | Python `logging` module |
| Configuration | JSON (`config.json`) |
| CI/CD (future) | GitHub Actions |

---

## 9. Assumptions and Modifications

- **Assumption 1:** Docker Desktop or Docker Engine is installed and running on the user's local machine.
- **Assumption 2:** The user has sufficient permissions to interact with the Docker socket.
- **Assumption 3:** Only local Docker operations are in scope; no remote Docker host management.
- **Modification 1:** A lightweight Flask web dashboard was added as an optional UI layer beyond the original CLI-only scope to improve usability and demonstrability.
- **Modification 2:** A config file (`config.json`) was added to allow basic customization without code changes.
- **Modification 3:** Logging (`app.log`) was added as a non-functional improvement for maintainability and debugging.
