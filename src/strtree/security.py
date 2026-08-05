from __future__ import annotations

from pathlib import Path


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def safe_join(root: Path, rel: Path) -> Path:
    """
    Join root and relative path safely.

    Prevents path traversal attacks like:
        ../../etc/passwd
    """
    root_resolved = root.expanduser().resolve()
    target = (root_resolved / rel).resolve()

    if not is_relative_to(target, root_resolved):
        raise ValueError(f"Unsafe path detected: {rel}")

    return target
