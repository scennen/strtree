from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from project_generator.models import ProjectSpec
from project_generator.parsers.dict_parser import parse_dict_spec
from project_generator.parsers.tree import parse_tree_text

try:
    import yaml
except ImportError:
    yaml = None


def load_spec(
    path: Path,
    root_override: Optional[Path] = None,
    git_init: Optional[bool] = None,
) -> ProjectSpec:
    """
    Load project specification from a file.

    Supported formats:
    - .tree / .txt: ASCII tree
    - .json
    - .yaml / .yml, if PyYAML installed
    """
    if not path.exists():
        raise ValueError(f"Spec file not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        spec = parse_dict_spec(data)

    elif suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise ValueError("PyYAML is required for YAML specs. Install with: pip install pyyaml")

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        spec = parse_dict_spec(data)

    else:
        # Treat as ASCII tree by default.
        text = path.read_text(encoding="utf-8")
        spec = parse_tree_text(text)

    if root_override:
        spec.root = root_override

    if git_init is not None:
        spec.git_init = git_init

    return spec