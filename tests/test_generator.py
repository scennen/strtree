from pathlib import Path

from strtree.actions import plan_actions
from strtree.models import DirSpec, FileSpec, ProjectSpec


def test_plan_actions(tmp_path):
    spec = ProjectSpec(
        root=tmp_path / "demo",
        dirs=[DirSpec(path=Path("src"))],
        files=[FileSpec(path=Path("src/main.py"))],
    )

    actions = plan_actions(spec)

    kinds = [action.kind for action in actions]

    assert "CREATE DIR" in kinds
    assert "CREATE FILE" in kinds


def test_plan_actions_git_init(tmp_path):
    spec = ProjectSpec(
        root=tmp_path / "demo",
        git_init=True,
    )

    actions = plan_actions(spec)

    run_actions = [action for action in actions if action.kind == "RUN"]

    assert len(run_actions) == 1
    assert run_actions[0].command == ["git", "init"]
