from __future__ import annotations

from pathlib import Path

PYTHON_GITIGNORE = """__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
.env
.venv/
venv/
env/
.git/
.idea/
.vscode/
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/
*.log
"""


def default_content(rel_path: Path, comment: str | None, root_name: str) -> str:
    """
    Generate useful default content for known files.
    """
    rel_path = Path(rel_path)
    name = rel_path.name
    suffix = rel_path.suffix

    comment_block = f"# {comment}\n" if comment else ""

    if name == "requirements.txt":
        return comment_block + "aiogram>=3.0.0\npython-dotenv>=1.0.0\n"

    if name == ".env":
        return comment_block + "BOT_TOKEN=\n"

    if name == ".env.example":
        return comment_block + "BOT_TOKEN=\n"

    if name == ".gitignore":
        return PYTHON_GITIGNORE

    if name == "README.md":
        text = f"# {root_name}\n"

        if comment:
            text += f"\n{comment}\n"

        return text

    if rel_path == Path("config.py"):
        docstring = f'"""{comment}"""\n\n' if comment else ""

        return docstring + '''from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str


def get_config() -> Config:
    token = os.getenv("BOT_TOKEN", "")

    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    return Config(bot_token=token)
'''

    if rel_path == Path("main.py"):
        docstring = f'"""{comment}"""\n\n' if comment else ""

        return docstring + '''import asyncio

from aiogram import Bot, Dispatcher

from config import get_config


async def main() -> None:
    config = get_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    # TODO: register routers and middlewares here.

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

    if suffix == ".py":
        if name == "__init__.py":
            return ""

        if comment:
            safe_comment = comment.replace('"""', "'''")
            return f'"""{safe_comment}"""\n'

        return ""

    if suffix in {".txt", ".cfg", ".ini", ".toml", ".yaml", ".yml"}:
        return comment_block

    if comment:
        return f"# {comment}\n"

    return ""

