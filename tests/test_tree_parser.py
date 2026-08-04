from pathlib import Path

from project_generator.parsers.tree import parse_tree_text


def test_parse_basic_tree():
    text = """demo/
│
├── src/
│   ├── __init__.py
│   └── main.py
└── README.md
"""

    spec = parse_tree_text(text)

    assert spec.root == Path("demo")

    dirs = {d.path for d in spec.dirs}
    files = {f.path for f in spec.files}

    assert Path("src") in dirs
    assert Path("src/__init__.py") in files
    assert Path("src/main.py") in files
    assert Path("README.md") in files


def test_parse_comments():
    text = """demo/
├── main.py  # Main entrypoint
"""

    spec = parse_tree_text(text)

    assert len(spec.files) == 1
    assert spec.files[0].comment == "Main entrypoint"