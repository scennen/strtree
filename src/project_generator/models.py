from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DirSpec:
    path: Path
    comment: str | None = None


@dataclass
class FileSpec:
    path: Path
    content: str | None = None
    comment: str | None = None
    executable: bool = False


@dataclass
class ProjectSpec:
    root: Path
    dirs: list[DirSpec] = field(default_factory=list)
    files: list[FileSpec] = field(default_factory=list)
    git_init: bool = False
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass
class Action:
    kind: str
    target: Path
    comment: str | None = None
    content: str | None = None
    executable: bool = False
    command: list[str] | None = None
