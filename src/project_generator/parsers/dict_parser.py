from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from project_generator.models import DirSpec, FileSpec, ProjectSpec
from project_generator.parsers.tree import parse_tree_text


def parse_structure_nodes(
    nodes: List[Any],
    base: Path = Path(),
) -> Tuple[List[DirSpec], List[FileSpec]]:
    """
    Parse JSON/YAML structure nodes.

    Supports flat paths:
        {"type": "file", "path": "src/main.py"}

    And nested children:
        {
          "type": "dir",
          "path": "src",
          "children": [...]
        }
    """
    dirs: List[DirSpec] = []
    files: List[FileSpec] = []

    for node in nodes:
        if isinstance(node, str):
            raw = node
            rel = Path(raw.rstrip("/"))
            path = base / rel

            if raw.endswith("/"):
                dirs.append(DirSpec(path=path))
            else:
                files.append(FileSpec(path=path))

            continue

        if not isinstance(node, dict):
            continue

        raw_path = node.get("path") or node.get("name")
        if not raw_path:
            continue

        rel = Path(str(raw_path).rstrip("/"))
        path = base / rel

        children = node.get("children", [])
        node_type = node.get("type")

        if node_type is None:
            node_type = "dir" if str(raw_path).endswith("/") or children else "file"

        if node_type == "dir":
            dirs.append(DirSpec(path=path, comment=node.get("comment")))

            if children:
                sub_dirs, sub_files = parse_structure_nodes(children, path)
                dirs.extend(sub_dirs)
                files.extend(sub_files)
        else:
            files.append(
                FileSpec(
                    path=path,
                    content=node.get("content"),
                    comment=node.get("comment"),
                    executable=bool(node.get("executable", False)),
                )
            )

    return dirs, files


def parse_dict_spec(data: Dict[str, Any]) -> ProjectSpec:
    """
    Parse JSON/YAML dictionary spec.
    """
    data = data or {}

    if "tree" in data:
        spec = parse_tree_text(str(data.get("tree")))
    else:
        root = data.get("root") or data.get("name") or "project"
        dirs, files = parse_structure_nodes(data.get("structure", []))
        spec = ProjectSpec(root=Path(root), dirs=dirs, files=files)

    if data.get("root") or data.get("name"):
        spec.root = Path(data.get("root") or data.get("name"))

    spec.git_init = bool(data.get("git_init", spec.git_init))
    spec.variables = data.get("variables", {}) or {}

    return spec