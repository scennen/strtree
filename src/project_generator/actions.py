from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from project_generator.models import Action, FileSpec, ProjectSpec
from project_generator.security import safe_join
from project_generator.templates import default_content


def add_default_files(
    spec: ProjectSpec,
    add_readme: bool = False,
    add_gitignore: bool = False,
) -> None:
    """
    Add README.md and .gitignore if missing.
    """
    existing_files = {Path(f.path) for f in spec.files}

    if add_readme and Path("README.md") not in existing_files:
        spec.files.append(
            FileSpec(
                path=Path("README.md"),
                comment="Generated project",
            )
        )

    if add_gitignore and Path(".gitignore") not in existing_files:
        spec.files.append(
            FileSpec(
                path=Path(".gitignore"),
            )
        )


def add_python_init_files(spec: ProjectSpec) -> None:
    """
    Add __init__.py into every non-hidden generated directory if missing.
    """
    existing_files = {Path(f.path) for f in spec.files}
    dirs = {Path(d.path) for d in spec.dirs}

    # Include implicit directories from file paths.
    for file in spec.files:
        for parent in Path(file.path).parents:
            if str(parent) in {".", "/"}:
                continue
            dirs.add(parent)

    for dir_path in sorted(dirs, key=lambda p: str(p)):
        # Skip hidden directories like .git, .venv, etc.
        if any(part.startswith(".") for part in dir_path.parts):
            continue

        init_path = dir_path / "__init__.py"

        if init_path not in existing_files:
            spec.files.append(FileSpec(path=init_path, content=""))
            existing_files.add(init_path)


def plan_actions(
    spec: ProjectSpec,
    force: bool = False,
    empty_files: bool = False,
) -> List[Action]:
    """
    Build execution plan.
    """
    root = Path(spec.root).expanduser()

    if root.exists() and not root.is_dir():
        raise ValueError(f"Target path already exists and is not a directory: {root}")

    root_name = root.name or "project"
    actions: List[Action] = []

    if root.exists():
        actions.append(Action(kind="EXISTS DIR", target=root))
    else:
        actions.append(Action(kind="CREATE DIR", target=root))

    # Collect explicit and implicit directories.
    dir_comments: Dict[Path, str | None] = {}
    all_dirs = set()

    for d in spec.dirs:
        rel = Path(d.path)
        dir_comments[rel] = d.comment
        all_dirs.add(rel)

    for f in spec.files:
        for parent in Path(f.path).parents:
            if str(parent) in {".", "/"}:
                continue
            all_dirs.add(parent)

    for rel in sorted(all_dirs, key=lambda p: (len(p.parts), str(p))):
        target = safe_join(root, rel)
        kind = "EXISTS DIR" if target.exists() else "CREATE DIR"
        actions.append(Action(kind=kind, target=target, comment=dir_comments.get(rel)))

    # Deduplicate files by path.
    files_by_path: Dict[Path, FileSpec] = {}
    for f in spec.files:
        files_by_path[Path(f.path)] = f

    for rel_path in sorted(files_by_path.keys(), key=lambda p: str(p)):
        file_spec = files_by_path[rel_path]
        target = safe_join(root, rel_path)

        if target.exists():
            if target.is_dir():
                kind = "SKIP FILE"
            elif force:
                kind = "OVERWRITE FILE"
            else:
                kind = "SKIP FILE"
        else:
            kind = "CREATE FILE"

        if file_spec.content is not None:
            content = file_spec.content
        elif empty_files:
            content = ""
        else:
            content = default_content(rel_path, file_spec.comment, root_name)

        actions.append(
            Action(
                kind=kind,
                target=target,
                comment=file_spec.comment,
                content=content,
                executable=file_spec.executable,
            )
        )

    if spec.git_init:
        actions.append(
            Action(
                kind="RUN",
                target=root,
                command=["git", "init"],
            )
        )

    return actions