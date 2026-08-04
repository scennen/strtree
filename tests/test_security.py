from pathlib import Path

import pytest

from project_generator.security import safe_join


def test_safe_join_prevents_traversal(tmp_path):
    with pytest.raises(ValueError):
        safe_join(tmp_path, Path("../../etc/passwd"))


def test_safe_join_allows_normal_path(tmp_path):
    target = safe_join(tmp_path, Path("src/main.py"))
    assert target.name == "main.py"