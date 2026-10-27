"""
test_container_manager.py
Unit Tests for ContainerManager core logic
Student: Kushagra Kaushik | Roll: S24BCAU0112
Course: CBCA321 - Software Containerization in DevOps
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.container_manager import ContainerManager


class TestContainerManagerInit(unittest.TestCase):
    """Tests for ContainerManager initialization."""

    @patch("src.container_manager.subprocess.run")
    def test_init_docker_running(self, mock_run):
        """Should initialize successfully when Docker is running."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        manager = ContainerManager()
        self.assertIsNotNone(manager)

    @patch("src.container_manager.subprocess.run")
    def test_init_docker_not_running(self, mock_run):
        """Should raise EnvironmentError when Docker is not running."""
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Cannot connect")
        with self.assertRaises(EnvironmentError):
            ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_init_docker_not_installed(self, mock_run):
        """Should raise EnvironmentError when Docker binary not found."""
        mock_run.side_effect = FileNotFoundError("No such file: docker")
        with self.assertRaises(EnvironmentError):
            ContainerManager()


class TestListContainers(unittest.TestCase):
    """Tests for list_containers method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_list_running_containers(self, mock_run):
        """Should return list of running containers."""
        mock_json = '{"ID":"abc123","Image":"nginx","Status":"Up 5 minutes","Names":"web","Ports":"0.0.0.0:8080->80/tcp"}'
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_json, stderr="")
        result = self.manager.list_containers()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Image"], "nginx")

    @patch("src.container_manager.subprocess.run")
    def test_list_empty(self, mock_run):
        """Should return empty list when no containers."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = self.manager.list_containers()
        self.assertEqual(result, [])

    @patch("src.container_manager.subprocess.run")
    def test_list_all_flag(self, mock_run):
        """Should include -a flag when all_containers=True."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        self.manager.list_containers(all_containers=True)
        cmd = mock_run.call_args[0][0]
        self.assertIn("-a", cmd)

    @patch("src.container_manager.subprocess.run")
    def test_list_docker_error(self, mock_run):
        """Should return empty list on Docker error."""
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        result = self.manager.list_containers()
        self.assertEqual(result, [])


class TestRunContainer(unittest.TestCase):
    """Tests for run_container method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_run_basic(self, mock_run):
        """Should run container and return container ID."""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="abc1234567890def", stderr=""
        )
        result = self.manager.run_container("nginx")
        self.assertTrue(result["success"])
        self.assertEqual(result["container_id"], "abc123456789")

    @patch("src.container_manager.subprocess.run")
    def test_run_with_name_and_port(self, mock_run):
        """Should include --name and -p in command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123", stderr="")
        self.manager.run_container("nginx", name="web", port="8080:80")
        cmd = mock_run.call_args[0][0]
        self.assertIn("--name", cmd)
        self.assertIn("web", cmd)
        self.assertIn("-p", cmd)
        self.assertIn("8080:80", cmd)

    @patch("src.container_manager.subprocess.run")
    def test_run_with_env(self, mock_run):
        """Should include -e flag for environment variables."""
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123", stderr="")
        self.manager.run_container("postgres", env={"POSTGRES_PASSWORD": "secret"})
        cmd = mock_run.call_args[0][0]
        self.assertIn("-e", cmd)
        self.assertIn("POSTGRES_PASSWORD=secret", cmd)

    @patch("src.container_manager.subprocess.run")
    def test_run_failure(self, mock_run):
        """Should return failure when Docker returns non-zero."""
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="Image not found"
        )
        result = self.manager.run_container("nonexistent_image")
        self.assertFalse(result["success"])


class TestStopContainer(unittest.TestCase):
    """Tests for stop_container method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_stop_success(self, mock_run):
        """Should stop container successfully."""
        mock_run.return_value = MagicMock(returncode=0, stdout="web", stderr="")
        result = self.manager.stop_container("web")
        self.assertTrue(result["success"])

    @patch("src.container_manager.subprocess.run")
    def test_stop_not_found(self, mock_run):
        """Should return failure for non-existent container."""
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="No such container"
        )
        result = self.manager.stop_container("ghost")
        self.assertFalse(result["success"])


class TestInspectContainer(unittest.TestCase):
    """Tests for inspect_container method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_inspect_returns_data(self, mock_run):
        """Should parse JSON and return container data."""
        sample = '[{"Id":"abc123","Name":"/web","State":{"Status":"running"},"Config":{"Image":"nginx"},"NetworkSettings":{"IPAddress":"172.17.0.2"}}]'
        mock_run.return_value = MagicMock(returncode=0, stdout=sample, stderr="")
        result = self.manager.inspect_container("web")
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["Name"], "/web")

    @patch("src.container_manager.subprocess.run")
    def test_inspect_not_found(self, mock_run):
        """Should return failure for non-existent container."""
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="No such container"
        )
        result = self.manager.inspect_container("ghost")
        self.assertFalse(result["success"])


class TestRemoveContainer(unittest.TestCase):
    """Tests for remove_container method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_remove_success(self, mock_run):
        """Should remove container successfully."""
        mock_run.return_value = MagicMock(returncode=0, stdout="web", stderr="")
        result = self.manager.remove_container("web")
        self.assertTrue(result["success"])

    @patch("src.container_manager.subprocess.run")
    def test_remove_force_flag(self, mock_run):
        """Should include -f flag when force=True."""
        mock_run.return_value = MagicMock(returncode=0, stdout="web", stderr="")
        self.manager.remove_container("web", force=True)
        cmd = mock_run.call_args[0][0]
        self.assertIn("-f", cmd)

    @patch("src.container_manager.subprocess.run")
    def test_remove_running_without_force(self, mock_run):
        """Should fail to remove running container without force."""
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="Cannot remove running container"
        )
        result = self.manager.remove_container("web", force=False)
        self.assertFalse(result["success"])


class TestStartContainer(unittest.TestCase):
    """Tests for start_container method."""

    def setUp(self):
        with patch("src.container_manager.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            self.manager = ContainerManager()

    @patch("src.container_manager.subprocess.run")
    def test_start_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="web", stderr="")
        result = self.manager.start_container("web")
        self.assertTrue(result["success"])

    @patch("src.container_manager.subprocess.run")
    def test_start_already_running(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1, stdout="", stderr="Container already started"
        )
        result = self.manager.start_container("web")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
