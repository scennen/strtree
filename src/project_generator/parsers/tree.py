from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from project_generator.models import DirSpec, FileSpec, ProjectSpec


TREE_PREFIX_RE = re.compile(r"^[\s│├└─]+")


def split_comment(line: str) -> Tuple[str, Optional[str]]:
    """
    Split tree line into path part and comment part.

    Example:
        ├── start.py           # Commands /start, /help

    Returns:
        ("├── start.py", "Commands /start, /help")
    """
    if "#" in line:
        left, right = line.split("#", 1)
        comment = right.strip()
        return left.rstrip(), comment or None

    return line.rstrip(), None


def tree_indent(line: str) -> int:
    """
    Convert tree graphics to spaces and return indentation size.
    """
    expanded = "".join(" " if ch in "│├└─\t" else ch for ch in line)
    return len(expanded) - len(expanded.lstrip(" "))


def parse_tree_text(text: str) -> ProjectSpec:
    """
    Parse ASCII tree-like structure.

    Example:
        my_bot_project/
        │
        ├── handlers/              # Handlers
        │   ├── __init__.py
        │   └── start.py           # /start
    """
    items: List[Dict[str, Any]] = []
    stack: List[Tuple[int, int]] = []

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        left, comment = split_comment(raw_line)

        # Skip lines containing only tree graphics, e.g. "│"
        cleaned_for_name = re.sub(r"[│├└─]", "", left)
        if not cleaned_for_name.strip():
            continue

        indent = tree_indent(left)
        name = TREE_PREFIX_RE.sub("", left).strip()

        if not name:
            continue

        while stack and indent <= stack[-1][0]:
            stack.pop()

        depth = len(stack)

        items.append(
            {
                "name": name,
                "comment": comment,
                "depth": depth,
            }
        )

        stack.append((indent, len(items) - 1))

    if not items:
        return ProjectSpec(root=Path("project"))

    # Infer directories.
    # Directory if:
    # 1. name ends with "/"
    # 2. next item is deeper
    for i, item in enumerate(items):
        name = item["name"]
        has_children = i + 1 < len(items) and items[i + 1]["depth"] > item["depth"]

        if name.endswith("/") or has_children:
            item["is_dir"] = True
        else:
            item["is_dir"] = False

    first = items[0]
    first_name = first["name"].rstrip("/")
    first_has_children = len(items) > 1 and items[1]["depth"] > first["depth"]

    # Treat first line as root if it is directory-like.
    first_is_root = (
        first["name"].endswith("/")
        or first_has_children
        or (len(items) == 1 and "." not in first_name)
    )

    if first_is_root:
        root_name = first_name or "project"
        entries = items[1:]
        offset = first["depth"] + 1
    else:
        root_name = "project"
        entries = items
        offset = min(item["depth"] for item in items) if items else 0

    dirs: List[DirSpec] = []
    files: List[FileSpec] = []
    dir_at_depth: Dict[int, Path] = {}

    for item in entries:
        depth = item["depth"] - offset
        if depth < 0:
            depth = 0

        name = item["name"].rstrip("/")
        if not name:
            continue

        parent = dir_at_depth.get(depth - 1, Path(""))
        rel_path = parent / name

        if item["is_dir"]:
            dirs.append(DirSpec(path=rel_path, comment=item["comment"]))
            dir_at_depth[depth] = rel_path

            # Remove deeper directory references when going up.
            for key in list(dir_at_depth.keys()):
                if key > depth:
                    del dir_at_depth[key]
        else:
            files.append(
                FileSpec(
                    path=rel_path,
                    content=None,
                    comment=item["comment"],
                    executable=False,
                )
            )

    return ProjectSpec(root=Path(root_name), dirs=dirs, files=files)