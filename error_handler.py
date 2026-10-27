import docker.errors


class ErrorHandler:
    """
    Centralised error handler that maps Docker SDK exceptions and
    common Python exceptions to user-friendly messages.
    """

    def handle(self, exception: Exception) -> str:
        """
        Translate an exception into a readable error string.
        :param exception: The raised exception.
        :return: User-friendly error message string.
        """

        # Docker not running / socket not found
        if isinstance(exception, docker.errors.DockerException):
            msg = str(exception).lower()
            if "connection refused" in msg or "named pipe" in msg or "socket" in msg:
                return (
                    "❌  Cannot connect to Docker. "
                    "Please make sure Docker Desktop (or Docker Engine) is running."
                )

        # Container not found
        if isinstance(exception, docker.errors.NotFound):
            return f"❌  Container not found: {exception.explanation}"

        # API error from Docker daemon
        if isinstance(exception, docker.errors.APIError):
            explanation = exception.explanation or str(exception)
            if "conflict" in explanation.lower():
                return f"❌  Conflict: {explanation}. Try using a different container name."
            if "is running" in explanation.lower():
                return "❌  Cannot remove a running container. Stop it first, or use --force."
            return f"❌  Docker API error: {explanation}"

        # Image not found (pull error)
        if isinstance(exception, docker.errors.ImageNotFound):
            return f"❌  Image not found: {exception.explanation}. Check the image name and try again."

        # Connection error (requests/urllib)
        if "ConnectionError" in type(exception).__name__ or "Timeout" in type(exception).__name__:
            return (
                "❌  Network error while connecting to Docker. "
                "Ensure Docker is running and try again."
            )

        # Generic fallback
        return f"❌  Unexpected error: {str(exception)}"
