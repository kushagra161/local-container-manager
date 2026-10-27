import docker
import logging
from typing import Optional
from error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class ContainerService:
    """
    Core service class for all Docker container operations.
    Communicates with the local Docker Engine via the docker-py SDK.
    """

    def __init__(self):
        self.error_handler = ErrorHandler()
        try:
            self.client = docker.from_env()
            self.client.ping()
            logger.info("Successfully connected to Docker Engine.")
        except Exception as e:
            raise ConnectionError(self.error_handler.handle(e))

    def list_containers(self, all: bool = True) -> list:
        """
        List containers on the local system.
        :param all: If True, include stopped containers. Default True.
        :return: List of container dicts with id, name, image, status.
        """
        try:
            containers = self.client.containers.list(all=all)
            result = []
            for c in containers:
                result.append({
                    "id": c.short_id,
                    "name": c.name,
                    "image": c.image.tags[0] if c.image.tags else "<none>",
                    "status": c.status,
                    "created": c.attrs.get("Created", "")[:10],
                })
            logger.info(f"Listed {len(result)} containers.")
            return result
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))

    def run_container(self, image: str, name: Optional[str] = None, ports: Optional[dict] = None, detach: bool = True) -> dict:
        """
        Run (create + start) a container from the given image.
        :param image: Docker image name (e.g., 'nginx', 'ubuntu:22.04')
        :param name: Optional container name.
        :param ports: Optional port mapping dict, e.g. {'80/tcp': 8080}
        :param detach: Run in background. Default True.
        :return: Dict with container info.
        """
        try:
            container = self.client.containers.run(
                image=image,
                name=name,
                ports=ports,
                detach=detach,
            )
            logger.info(f"Container '{container.name}' started from image '{image}'.")
            return {
                "id": container.short_id,
                "name": container.name,
                "image": image,
                "status": container.status,
            }
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))

    def start_container(self, container_id: str) -> bool:
        """
        Start a stopped container by name or ID.
        :param container_id: Container name or short/full ID.
        :return: True if started successfully.
        """
        try:
            container = self.client.containers.get(container_id)
            container.start()
            logger.info(f"Container '{container_id}' started.")
            return True
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))

    def stop_container(self, container_id: str) -> bool:
        """
        Stop a running container by name or ID.
        :param container_id: Container name or short/full ID.
        :return: True if stopped successfully.
        """
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            logger.info(f"Container '{container_id}' stopped.")
            return True
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))

    def remove_container(self, container_id: str, force: bool = False) -> bool:
        """
        Remove a container by name or ID.
        :param container_id: Container name or short/full ID.
        :param force: If True, forcefully remove even if running.
        :return: True if removed successfully.
        """
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            logger.info(f"Container '{container_id}' removed.")
            return True
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))

    def inspect_container(self, container_id: str) -> dict:
        """
        Inspect and return detailed info about a container.
        :param container_id: Container name or short/full ID.
        :return: Dict with detailed container attributes.
        """
        try:
            container = self.client.containers.get(container_id)
            attrs = container.attrs
            info = {
                "id": container.id,
                "short_id": container.short_id,
                "name": container.name,
                "status": attrs["State"]["Status"],
                "image": attrs["Config"]["Image"],
                "created": attrs.get("Created", "")[:19].replace("T", " "),
                "ip_address": attrs["NetworkSettings"]["IPAddress"] or "N/A",
                "ports": attrs["NetworkSettings"].get("Ports", {}),
                "restart_count": attrs["RestartCount"],
                "platform": attrs.get("Platform", "linux"),
                "cmd": attrs["Config"].get("Cmd") or [],
                "env": attrs["Config"].get("Env") or [],
            }
            logger.info(f"Inspected container '{container_id}'.")
            return info
        except Exception as e:
            raise RuntimeError(self.error_handler.handle(e))
