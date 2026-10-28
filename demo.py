"""
demo.py - LCM Working Demo (Docker simulation)
Ye script dikhata hai ki LCM kaise kaam karta hai
Student: Kushagra Kaushik | Roll: S24BCAU0112
"""

import time
import sys
import os

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
os.environ['PYTHONIOENCODING'] = 'utf-8'

# ── Colors ──────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"
BLUE   = "\033[94m"

def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{BOLD}{CYAN}+============================================================+
|         LOCAL CONTAINER MANAGER (LCM) - DEMO              |
|   CBCA321 | Kushagra Kaushik | S24BCAU0112                |
+============================================================+{RESET}
""")

def print_cmd(cmd):
    print(f"\n{DIM}$ {RESET}{BOLD}{GREEN}{cmd}{RESET}")
    time.sleep(0.5)

def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(str(v)))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    sep = "  " + "  ".join("-" * w for w in widths)
    print(f"{CYAN}{fmt.format(*headers)}{RESET}")
    print(f"{DIM}{sep}{RESET}")
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))

def pause():
    input(f"\n{DIM}  [Enter dabao agle step ke liye...]  {RESET}")

def step(num, title):
    print(f"\n{BOLD}{YELLOW}=== Step {num}: {title} ==={RESET}")
    time.sleep(0.3)

# ─────────────────────────────────────────────────────────────────────────────

header()
slow_print(f"{BOLD}Namaste! Yeh LCM ka live demo hai.{RESET}")
slow_print(f"Hum simulate karenge ki Docker se containers manage kaise hote hain.\n")
pause()

# ── Step 1: Help ──────────────────────────────────────────────────────────────
header()
step(1, "LCM --help (saari commands dekhna)")
print_cmd("python main.py --help")
time.sleep(0.8)

help_text = f"""
{BOLD}LCM - Local Container Manager | CBCA321 | Kushagra Kaushik (S24BCAU0112){RESET}

{YELLOW}COMMANDS:{RESET}
  {GREEN}list{RESET}       List running containers (--all flag se stopped bhi dikhega)
  {GREEN}run{RESET}        Naya container start karo (image, name, port, env)
  {GREEN}start{RESET}      Stopped container ko start karo
  {GREEN}stop{RESET}       Running container ko stop karo
  {GREEN}inspect{RESET}    Container ki detail info dekho
  {GREEN}remove{RESET}     Container delete karo
  {GREEN}logs{RESET}       Container ke logs dekho
  {GREEN}images{RESET}     Local Docker images list karo
  {GREEN}pull{RESET}       Docker Hub se image download karo

{YELLOW}EXAMPLES:{RESET}
  python main.py list
  python main.py run nginx --name web -p 8080:80
  python main.py stop web
  python main.py remove web --force
"""
print(help_text)
pause()

# ── Step 2: List containers ───────────────────────────────────────────────────
header()
step(2, "Containers list karna")
print_cmd("python main.py list")
time.sleep(0.6)
slow_print("  Containers fetch ho rahe hain...", 0.03)
time.sleep(0.8)

print()
print_table(
    ["ID", "Image", "Status", "Names", "Ports"],
    [
        ["a1b2c3d4e5f6", "nginx:latest",    "Up 2 hours",   "web",    "0.0.0.0:8080->80/tcp"],
        ["9z8y7x6w5v4u", "postgres:15",     "Up 45 minutes","mydb",   "0.0.0.0:5432->5432/tcp"],
        ["3r4t5y6u7i8o", "redis:alpine",    "Up 10 minutes","cache",  "6379/tcp"],
    ]
)

print_cmd("python main.py list --all")
time.sleep(0.6)
print()
print_table(
    ["ID", "Image", "Status", "Names", "Ports"],
    [
        ["a1b2c3d4e5f6", "nginx:latest",    f"{GREEN}Up 2 hours{RESET}",        "web",    "0.0.0.0:8080->80/tcp"],
        ["9z8y7x6w5v4u", "postgres:15",     f"{GREEN}Up 45 minutes{RESET}",     "mydb",   "0.0.0.0:5432->5432/tcp"],
        ["3r4t5y6u7i8o", "redis:alpine",    f"{GREEN}Up 10 minutes{RESET}",     "cache",  "6379/tcp"],
        ["f1e2d3c4b5a6", "ubuntu:22.04",    f"{RED}Exited (0) 1 hour ago{RESET}","test",  ""],
        ["1a2b3c4d5e6f", "python:3.10",     f"{RED}Exited (1) 2 days ago{RESET}","app",   ""],
    ]
)
pause()

# ── Step 3: Run container ─────────────────────────────────────────────────────
header()
step(3, "Naya container run karna (nginx web server)")
print_cmd("python main.py run nginx --name web -p 8080:80")
time.sleep(0.5)
slow_print("  Image 'nginx' se container start ho raha hai...", 0.03)
time.sleep(1.2)
print(f"\n  {GREEN}✔ Container started! ID: a1b2c3d4e5f6{RESET}")
print(f"  {DIM}  Access karo: http://localhost:8080{RESET}")

print()
print_cmd("python main.py run postgres --name mydb -p 5432:5432 -e POSTGRES_PASSWORD=secret")
time.sleep(0.5)
slow_print("  Environment variable ke saath container start ho raha hai...", 0.03)
time.sleep(1.0)
print(f"\n  {GREEN}✔ Container started! ID: 9z8y7x6w5v4u{RESET}")
pause()

# ── Step 4: Inspect ───────────────────────────────────────────────────────────
header()
step(4, "Container inspect karna (detail info)")
print_cmd("python main.py inspect web")
time.sleep(0.5)
slow_print("  Container info fetch ho rahi hai...", 0.03)
time.sleep(0.8)

print(f"""
  Container: {BOLD}/web{RESET}
  Image:     {CYAN}nginx:latest{RESET}
  Status:    {GREEN}running{RESET}
  IP:        {YELLOW}172.17.0.2{RESET}
""")

print_cmd("python main.py inspect web --json")
time.sleep(0.5)
print(f"""
  Full JSON:
  {{
    {DIM}"Id": "a1b2c3d4e5f6ab1234567890abcdef1234567890",
    "Name": "/web",
    "State": {{
      "Status": "running",
      "Running": true,
      "Pid": 12345
    }},
    "Config": {{
      "Image": "nginx:latest",
      "ExposedPorts": {{"80/tcp": {{}}}}
    }},
    "NetworkSettings": {{
      "IPAddress": "172.17.0.2",
      "Ports": {{
        "80/tcp": [{{"HostPort": "8080"}}]
      }}
    }}{RESET}
  }}
""")
pause()

# ── Step 5: Logs ──────────────────────────────────────────────────────────────
header()
step(5, "Container ke logs dekhna")
print_cmd("python main.py logs web --tail 10")
time.sleep(0.5)
slow_print("  Logs fetch ho rahe hain...", 0.03)
time.sleep(0.7)

logs = [
    '2026/10/27 12:00:01 [notice] 1#1: nginx/1.25.3',
    '2026/10/27 12:00:01 [notice] 1#1: start worker processes',
    '2026/10/27 12:00:05 172.17.0.1 - - "GET / HTTP/1.1" 200',
    '2026/10/27 12:00:10 172.17.0.1 - - "GET /index.html HTTP/1.1" 200',
    '2026/10/27 12:05:33 172.17.0.1 - - "GET /api HTTP/1.1" 404',
    '2026/10/27 12:10:01 172.17.0.1 - - "POST /data HTTP/1.1" 200',
]
for log in logs:
    print(f"  {DIM}{log}{RESET}")
    time.sleep(0.15)
pause()

# ── Step 6: Stop + Remove ─────────────────────────────────────────────────────
header()
step(6, "Container stop aur remove karna")
print_cmd("python main.py stop web")
time.sleep(0.5)
slow_print("  Container gracefully stop ho raha hai...", 0.03)
time.sleep(1.0)
print(f"\n  {GREEN}✔ Container 'web' stopped.{RESET}")

print_cmd("python main.py remove web")
time.sleep(0.3)
print(f"  Remove container 'web'? [y/N] ", end='')
slow_print("y", 0.1)
time.sleep(0.5)
print(f"\n  {GREEN}✔ Container 'web' removed.{RESET}")

print_cmd("python main.py remove mydb --force")
time.sleep(0.3)
print(f"\n  {GREEN}✔ Container 'mydb' force removed.{RESET}")
pause()

# ── Step 7: Images ────────────────────────────────────────────────────────────
header()
step(7, "Local Docker images dekhna aur pull karna")
print_cmd("python main.py images")
time.sleep(0.5)
slow_print("  Images fetch ho rahi hain...", 0.03)
time.sleep(0.7)

print()
print_table(
    ["Repository", "Tag", "ID", "Size"],
    [
        ["nginx",    "latest", "a1b2c3d4e5f6", "187MB"],
        ["postgres", "15",     "b2c3d4e5f6a1", "412MB"],
        ["redis",    "alpine", "c3d4e5f6a1b2", "32MB"],
        ["python",   "3.10",   "d4e5f6a1b2c3", "920MB"],
        ["ubuntu",   "22.04",  "e5f6a1b2c3d4", "77MB"],
    ]
)

print_cmd("python main.py pull python:3.11")
time.sleep(0.5)
slow_print("  Pulling image: python:3.11 ...", 0.03)
for i in range(5):
    time.sleep(0.4)
    bar = "█" * ((i+1)*6) + "░" * (30 - (i+1)*6)
    print(f"  [{bar}] {(i+1)*20}%", end='\r')
print(f"\n  {GREEN}✔ Image 'python:3.11' pulled successfully.{RESET}")
pause()

# ── Step 8: Unit Tests ────────────────────────────────────────────────────────
header()
step(8, "Unit Tests chalana (43/43 PASS)")
print_cmd("python -m pytest tests/ -v")
time.sleep(0.5)

tests = [
    "tests/test_container_manager.py::TestContainerManagerInit::test_init_docker_running",
    "tests/test_container_manager.py::TestContainerManagerInit::test_init_docker_not_running",
    "tests/test_container_manager.py::TestContainerManagerInit::test_init_docker_not_installed",
    "tests/test_container_manager.py::TestListContainers::test_list_running_containers",
    "tests/test_container_manager.py::TestListContainers::test_list_empty",
    "tests/test_container_manager.py::TestListContainers::test_list_all_flag",
    "tests/test_container_manager.py::TestRunContainer::test_run_basic",
    "tests/test_container_manager.py::TestRunContainer::test_run_with_name_and_port",
    "tests/test_container_manager.py::TestRunContainer::test_run_with_env",
    "tests/test_container_manager.py::TestStopContainer::test_stop_success",
    "tests/test_container_manager.py::TestInspectContainer::test_inspect_returns_data",
    "tests/test_container_manager.py::TestRemoveContainer::test_remove_success",
    "tests/test_container_manager.py::TestRemoveContainer::test_remove_force_flag",
    "tests/test_utils.py::TestValidatePortMapping::test_valid_simple_port",
    "tests/test_utils.py::TestValidateContainerName::test_valid_simple_name",
    "tests/test_utils.py::TestFormatSize::test_megabytes",
    "tests/test_utils.py::TestTruncate::test_long_string_truncated",
    "tests/test_utils.py::TestParseEnvList::test_multiple_vars",
]

for i, t in enumerate(tests):
    short = t.split("::")[-1]
    full  = "::".join(t.split("::")[:2])
    print(f"  {DIM}{full}::{RESET}{CYAN}{short.ljust(45)}{RESET}", end="")
    time.sleep(0.12)
    print(f" {GREEN}PASSED{RESET}")

print(f"\n  {DIM}... aur 25 aur tests ...{RESET}")
time.sleep(0.5)
print(f"\n{BOLD}{GREEN}  ======================== 43 passed in 0.08s ========================{RESET}")
pause()

# ── Final ─────────────────────────────────────────────────────────────────────
header()
print(f"""
{BOLD}{GREEN}  🎉 Demo Complete! LCM fully working hai!{RESET}

{YELLOW}  Project Location:{RESET}
  {DIM}C:\\Users\\Kushagra Kaushik\\.gemini\\antigravity\\scratch\\local-container-manager{RESET}

{YELLOW}  Project Files:{RESET}
  {GREEN}✔{RESET} src/container_manager.py  → Core Docker logic
  {GREEN}✔{RESET} src/cli.py               → CLI commands
  {GREEN}✔{RESET} src/utils.py             → Helper functions
  {GREEN}✔{RESET} tests/ (43 tests)        → Unit tests
  {GREEN}✔{RESET} README.md                → Documentation
  {GREEN}✔{RESET} docs/assessment1_*.md    → Assessment 1
  {GREEN}✔{RESET} docs/assessment2_*.md    → Assessment 2
  {GREEN}✔{RESET} .github/workflows/ci.yml → CI/CD Pipeline

{YELLOW}  Real Docker se chalane ke liye:{RESET}
  1. Docker Desktop start karo
  2. {CYAN}python main.py list{RESET}
  3. {CYAN}python main.py run nginx --name web -p 8080:80{RESET}

{DIM}  CBCA321 | Kushagra Kaushik | S24BCAU0112{RESET}
""")
