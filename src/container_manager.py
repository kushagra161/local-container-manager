"""
container_manager.py
Core logic for Local Container Manager (LCM)
Student: Kushagra Kaushik | Roll: S24BCAU0112
Course: CBCA321 - Software Containerization in DevOps
"""

import subprocess
import json
from typing import Optional


class ContainerManager:
    """
    Local Container Manager - wraps Docker CLI to provide
    a simple, beginner-friendly interface for managing containers.
    """

    def __init__(self):
        self._verify_docker()

    def _verify_docker(self):
        """Check if Docker is installed and running."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                raise EnvironmentError(
                    "Docker is not running. Please start Docker Desktop first."
                )
        except FileNotFoundError:
            raise EnvironmentError(
                "Docker is not installed. Please install Docker from https://docker.com"
            )

    def _run(self, cmd: list, timeout: int = 30) -> dict:
        """Run a docker command and return structured result."""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "Command timed out.", "returncode": -1}
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

    # ─── LIST ────────────────────────────────────────────────────────────────

    def list_containers(self, all_containers: bool = False) -> list:
        """
        List running (or all) containers.
        Returns a list of container dicts.
        """
        cmd = ["docker", "ps", "--format", "json"]
        if all_containers:
            cmd.insert(2, "-a")

        result = self._run(cmd)
        if not result["success"]:
            return []

        containers = []
        for line in result["stdout"].splitlines():
            line = line.strip()
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return containers

    # ─── RUN ─────────────────────────────────────────────────────────────────

    def run_container(
        self,
        image: str,
        name: Optional[str] = None,
        port: Optional[str] = None,
        detach: bool = True,
        env: Optional[dict] = None,
    ) -> dict:
        """
        Run a new container from a Docker image.

        Args:
            image:  Docker image name (e.g. 'nginx', 'python:3.10')
            name:   Optional container name
            port:   Port mapping string e.g. '8080:80'
            detach: Run in background (default True)
            env:    Environment variables dict

        Returns:
            Result dict with success flag and container ID.
        """
        cmd = ["docker", "run"]
        if detach:
            cmd.append("-d")
        if name:
            cmd += ["--name", name]
        if port:
            cmd += ["-p", port]
        if env:
            for k, v in env.items():
                cmd += ["-e", f"{k}={v}"]
        cmd.append(image)

        result = self._run(cmd, timeout=120)
        if result["success"]:
            result["container_id"] = result["stdout"][:12]
        return result

    # ─── START ───────────────────────────────────────────────────────────────

    def start_container(self, container_id_or_name: str) -> dict:
        """Start a stopped container."""
        return self._run(["docker", "start", container_id_or_name])

    # ─── STOP ────────────────────────────────────────────────────────────────

    def stop_container(self, container_id_or_name: str, timeout: int = 10) -> dict:
        """Stop a running container gracefully."""
        return self._run(
            ["docker", "stop", "-t", str(timeout), container_id_or_name]
        )

    # ─── INSPECT ─────────────────────────────────────────────────────────────

    def inspect_container(self, container_id_or_name: str) -> dict:
        """
        Get detailed info about a container.
        Returns parsed JSON data.
        """
        result = self._run(["docker", "inspect", container_id_or_name])
        if result["success"]:
            try:
                data = json.loads(result["stdout"])
                result["data"] = data[0] if data else {}
            except json.JSONDecodeError:
                result["data"] = {}
        return result

    # ─── REMOVE ──────────────────────────────────────────────────────────────

    def remove_container(self, container_id_or_name: str, force: bool = False) -> dict:
        """Remove a stopped (or running, if force=True) container."""
        cmd = ["docker", "rm"]
        if force:
            cmd.append("-f")
        cmd.append(container_id_or_name)
        return self._run(cmd)

    # ─── LOGS ────────────────────────────────────────────────────────────────

    def get_logs(self, container_id_or_name: str, tail: int = 50) -> dict:
        """Fetch container logs (last N lines)."""
        return self._run(
            ["docker", "logs", "--tail", str(tail), container_id_or_name]
        )

    # ─── IMAGES ──────────────────────────────────────────────────────────────

    def list_images(self) -> list:
        """List all locally available Docker images."""
        result = self._run(["docker", "images", "--format", "json"])
        images = []
        for line in result["stdout"].splitlines():
            line = line.strip()
            if line:
                try:
                    images.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return images

    def pull_image(self, image: str) -> dict:
        """Pull a Docker image from Docker Hub."""
        return self._run(["docker", "pull", image], timeout=300)

    # ─── STATS ───────────────────────────────────────────────────────────────

    def get_stats(self, container_id_or_name: str) -> dict:
        """Get live resource usage stats (snapshot)."""
        return self._run(
            ["docker", "stats", "--no-stream", "--format", "json", container_id_or_name]
        )
