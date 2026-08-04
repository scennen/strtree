from __future__ import annotations

import argparse
import sys
from pathlib import Path

from project_generator import __version__
from project_generator.actions import add_default_files, add_python_init_files, plan_actions
from project_generator.executor import execute_actions
from project_generator.parsers import load_spec


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="project-generator",
        description="Local CLI project generator",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser(
        "generate",
        aliases=["gen"],
        help="Generate project from spec file",
    )

    gen.add_argument(
        "spec",
        type=Path,
        help="Path to spec file: .tree, .txt, .json, .yaml",
    )

    gen.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Override root directory from spec",
    )

    gen.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show what will be done",
    )

    gen.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )

    gen.add_argument(
        "--git-init",
        dest="git_init",
        action="store_true",
        default=None,
        help="Run git init after generation",
    )

    gen.add_argument(
        "--no-git-init",
        dest="git_init",
        action="store_false",
        default=None,
        help="Do not run git init",
    )

    gen.add_argument(
        "--add-defaults",
        action="store_true",
        help="Add README.md and .gitignore if missing",
    )

    gen.add_argument(
        "--add-readme",
        action="store_true",
        help="Add README.md if missing",
    )

    gen.add_argument(
        "--add-gitignore",
        action="store_true",
        help="Add .gitignore if missing",
    )

    gen.add_argument(
        "--auto-init",
        action="store_true",
        help="Create __init__.py in every generated non-hidden directory if missing",
    )

    gen.add_argument(
        "--empty-files",
        action="store_true",
        help="Do not generate default content for known files",
    )

    args = parser.parse_args(argv)

    if args.command in {"generate", "gen"}:
        try:
            spec = load_spec(
                args.spec,
                root_override=args.root,
                git_init=args.git_init,
            )

            if args.add_defaults:
                args.add_readme = True
                args.add_gitignore = True

            # If git init is enabled, add .gitignore by default for safety.
            if spec.git_init:
                args.add_gitignore = True

            add_default_files(
                spec,
                add_readme=args.add_readme,
                add_gitignore=args.add_gitignore,
            )

            if args.auto_init:
                add_python_init_files(spec)

            actions = plan_actions(
                spec,
                force=args.force,
                empty_files=args.empty_files,
            )

            execute_actions(actions, dry_run=args.dry_run)

        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()