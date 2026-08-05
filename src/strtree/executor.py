from __future__ import annotations

import subprocess
import sys

from strtree.models import Action


def print_action(action: Action, dry_run: bool) -> None:
    prefix = "[dry-run] " if dry_run else ""

    if action.kind == "RUN":
        command = " ".join(action.command or [])
        print(f"{prefix}{action.kind:<12} {command} in {action.target}")
        return

    line = f"{prefix}{action.kind:<18} {action.target}"

    if action.comment:
        line += f"  # {action.comment}"

    print(line)


def execute_actions(actions: list[Action], dry_run: bool = False) -> None:
    for action in actions:
        print_action(action, dry_run)

        if dry_run:
            continue

        try:
            if action.kind == "CREATE DIR":
                action.target.mkdir(parents=True, exist_ok=True)

            elif action.kind == "EXISTS DIR":
                pass

            elif action.kind in {"CREATE FILE", "OVERWRITE FILE"}:
                action.target.parent.mkdir(parents=True, exist_ok=True)
                action.target.write_text(action.content or "", encoding="utf-8")

                if action.executable:
                    action.target.chmod(0o755)

            elif action.kind.startswith("SKIP"):
                pass

            elif action.kind == "RUN":
                subprocess.run(action.command or [], cwd=action.target, check=True)

        except FileNotFoundError as exc:
            print(f"ERROR: command or file not found: {exc}", file=sys.stderr)
            sys.exit(1)

        except subprocess.CalledProcessError as exc:
            print(f"ERROR: command failed: {exc}", file=sys.stderr)
            sys.exit(1)

        except OSError as exc:
            print(f"ERROR: {action.target}: {exc}", file=sys.stderr)
            sys.exit(1)
