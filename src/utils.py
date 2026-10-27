"""
utils.py
Utility helpers for Local Container Manager
Student: Kushagra Kaushik | Roll: S24BCAU0112
"""

import re
from datetime import datetime


def validate_port_mapping(port: str) -> bool:
    """
    Validate port mapping string like '8080:80' or '0.0.0.0:8080:80'.
    Returns True if valid, False otherwise.
    """
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:)?\d{1,5}:\d{1,5}$'
    return bool(re.match(pattern, port))


def validate_container_name(name: str) -> bool:
    """
    Container names must match [a-zA-Z0-9_.-].
    Returns True if valid.
    """
    return bool(re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$', name))


def format_size(size_bytes: int) -> str:
    """Convert bytes to human-readable size string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_timestamp(ts: str) -> str:
    """Convert ISO timestamp to readable format."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return ts


def truncate(text: str, max_len: int = 40) -> str:
    """Truncate long strings with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def parse_env_list(env_list: list) -> dict:
    """
    Parse list of 'KEY=VALUE' strings into a dict.
    Skips invalid entries.
    """
    result = {}
    for item in (env_list or []):
        if "=" in item:
            k, v = item.split("=", 1)
            result[k.strip()] = v.strip()
    return result
