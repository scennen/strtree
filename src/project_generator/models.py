from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DirSpec:
    path: Path
    comment: Optional[str] = None


@dataclass
class FileSpec:
    path: Path
    content: Optional[str] = None
    comment: Optional[str] = None
    executable: bool = False


@dataclass
class ProjectSpec:
    root: Path
    dirs: List[DirSpec] = field(default_factory=list)
    files: List[FileSpec] = field(default_factory=list)
    git_init: bool = False
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Action:
    kind: str
    target: Path
    comment: Optional[str] = None
    content: Optional[str] = None
    executable: bool = False
    command: Optional[List[str]] = None
