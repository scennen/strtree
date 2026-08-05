from __future__ import annotations

from pathlib import Path
from typing import Any

from strtree.models import DirSpec, FileSpec, ProjectSpec


def _is_graphics(ch: str) -> bool:
    """
    True для пробельных символов и символов рисования дерева.

    Поддерживаются:
    - весь блок box-drawing U+2500..U+257F (─ │ ├ └ ━ ┃ и т.д.);
    - ASCII-варианты: | - +
    - пробелы и табы.
    """
    if ch.isspace():
        return True

    if "\u2500" <= ch <= "\u257f":
        return True

    return ch in "|+-"


def _strip_graphics_left(text: str) -> str:
    """Убрать символы-графику слева до первого «нормального» символа."""
    i = 0
    while i < len(text) and _is_graphics(text[i]):
        i += 1
    return text[i:]


def _remove_graphics(text: str) -> str:
    """Убрать всю графику из строки."""
    return "".join(ch for ch in text if not _is_graphics(ch))


def split_comment(line: str) -> tuple[str, str | None]:
    """
    Разделить строку на часть с путём и комментарий после #.
    """
    if "#" in line:
        left, right = line.split("#", 1)
        comment = right.strip()
        return left.rstrip(), comment or None

    return line.rstrip(), None


def tree_indent(line: str) -> int:
    """
    Превратить графику дерева в пробелы и посчитать отступ.
    """
    expanded = "".join(" " if _is_graphics(ch) else ch for ch in line)
    return len(expanded) - len(expanded.lstrip(" "))


def parse_tree_text(text: str) -> ProjectSpec:
    """
    Разобрать ASCII/Unicode tree-структуру.

    Поддерживает:
    - обычные tree-файлы (├──, └──, │);
    - ASCII-деревья (|--, +--, |);
    - многострочные комментарии.
    """
    items: list[dict[str, Any]] = []
    stack: list[tuple[int, int]] = []

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        left, comment = split_comment(raw_line)

        # Строка состоит только из графики дерева.
        if not _remove_graphics(left).strip():
            # Это продолжение многострочного комментария.
            if comment and items:
                prev = items[-1]
                if prev["comment"]:
                    prev["comment"] = f"{prev['comment']} {comment}"
                else:
                    prev["comment"] = comment
            continue

        indent = tree_indent(left)
        name = _strip_graphics_left(left).strip()

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

    # Определяем папки:
    # 1. имя заканчивается на "/"
    # 2. следующий элемент глубже
    for i, item in enumerate(items):
        name = item["name"]
        has_children = i + \
            1 < len(items) and items[i + 1]["depth"] > item["depth"]

        item["is_dir"] = name.endswith("/") or has_children

    first = items[0]
    first_name = first["name"].rstrip("/")
    first_has_children = len(items) > 1 and items[1]["depth"] > first["depth"]

    # Первая строка считается корнем, если она похожа на папку.
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

    dirs: list[DirSpec] = []
    files: list[FileSpec] = []
    dir_at_depth: dict[int, Path] = {}

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
