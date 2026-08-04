# Project Generator

![CI](https://github.com/OWNER/project-generator/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/OWNER/project-generator/actions/workflows/cd.yml/badge.svg)

`project-generator` — локальный CLI-инструмент для генерации структуры проекта по описанию.

Поддерживает ASCII-tree, JSON и YAML. Создаёт папки, файлы, `__init__.py`, `.env`, `README.md`, `.gitignore`, `requirements.txt` и другие базовые файлы.

---

## Возможности

- генерация проекта из tree / JSON / YAML;
- создание папок и файлов;
- поддержка комментариев в структуре;
- `--dry-run` режим;
- автоматическое создание `__init__.py`;
- добавление `README.md` и `.gitignore`;
- опциональный `git init`;
- защита от небезопасных путей;
- тесты и CI/CD через GitHub Actions.

---

## Требования

- Python 3.9+
- git, если нужен `git init`
- опционально `pyyaml` для YAML

---

## Установка

```bash
git clone https://github.com/OWNER/project-generator.git
cd project-generator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

Для разработки:

```bash
pip install -e ".[dev,yaml]"
```

---

## Использование

Проверить, что будет создано:

```bash
project-generator generate examples/telegram_bot.tree --dry-run
```

Создать проект:

```bash
project-generator generate examples/telegram_bot.tree
```

Создать проект с `README.md`, `.gitignore` и `git init`:

```bash
project-generator generate examples/telegram_bot.tree --git-init --add-defaults
```

Полный вариант:

```bash
project-generator generate examples/telegram_bot.tree \
  --git-init \
  --add-defaults \
  --auto-init
```

---

## Основные флаги

| Флаг              | Описание                                   |
| ----------------- | ------------------------------------------ |
| `--dry-run`       | показать действия без создания файлов      |
| `--force`         | перезаписывать существующие файлы          |
| `--root PATH`     | переопределить корень проекта              |
| `--git-init`      | выполнить `git init`                       |
| `--no-git-init`   | не выполнять `git init`                    |
| `--add-defaults`  | добавить `README.md` и `.gitignore`        |
| `--add-readme`    | добавить `README.md`                       |
| `--add-gitignore` | добавить `.gitignore`                      |
| `--auto-init`     | создать `__init__.py` в папках             |
| `--empty-files`   | создавать файлы без дефолтного содержимого |

---

## Пример tree-структуры

```text
my_bot_project/
│
├── handlers/              # Обработчики сообщений и команд
│   ├── __init__.py
│   ├── start.py           # Команды /start, /help
│   └── admin.py           # Панель управления администратора
│
├── keyboards/             # Кнопки и меню
│   ├── __init__.py
│   ├── reply.py
│   └── inline.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── requests.py
│
├── .env
├── config.py
├── main.py
└── requirements.txt
```

Комментарии после `#` могут использоваться как описание файлов.

---

## Пример JSON

```json
{
  "root": "my_project",
  "git_init": true,
  "structure": [
    {
      "type": "dir",
      "path": "src"
    },
    {
      "type": "file",
      "path": "src/__init__.py",
      "content": ""
    },
    {
      "type": "file",
      "path": "src/main.py",
      "comment": "Main entrypoint"
    }
  ]
}
```

---

## Пример YAML

```yaml
root: my_project
git_init: true

structure:
  - type: dir
    path: src

  - type: file
    path: src/__init__.py
    content: ""

  - type: file
    path: src/main.py
    comment: Main entrypoint
```

---

## Запуск без установки

Linux / macOS:

```bash
PYTHONPATH=src python -m project_generator.cli generate examples/telegram_bot.tree --dry-run
```

Windows:

```bash
set PYTHONPATH=src
python -m project_generator.cli generate examples/telegram_bot.tree --dry-run
```

---

## Разработка

Установка dev-зависимостей:

```bash
pip install -e ".[dev,yaml]"
```

Тесты:

```bash
pytest
```

Линтер:

```bash
ruff check src tests
```

Сборка пакета:

```bash
python -m build
```

Проверка пакета:

```bash
twine check dist/*
```

---

## Структура проекта

```text
project-generator/
│
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── examples/
│   ├── telegram_bot.tree
│   ├── project.json
│   └── project.yaml
│
├── src/
│   └── project_generator/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── security.py
│       ├── templates.py
│       ├── actions.py
│       ├── executor.py
│       └── parsers/
│           ├── __init__.py
│           ├── tree.py
│           └── dict_parser.py
│
├── tests/
├── README.md
├── LICENSE
├── .gitignore
└── pyproject.toml
```

---

## CI/CD

CI запускается на каждый pull request и push в `main`.

Что делает CI:

- линтер через Ruff;
- тесты на Python 3.9–3.12.

CD запускается при теге вида:

```bash
v0.1.0
```

Что делает CD:

- тесты перед релизом;
- сборка пакета;
- проверка пакета;
- GitHub Release;
- опциональная публикация в PyPI.

---

## Релиз

Обнови версию в:

```text
pyproject.toml
src/project_generator/__init__.py
```

Затем:

```bash
git add pyproject.toml src/project_generator/__init__.py
git commit -m "Bump version"
git push

git tag v0.1.0
git push origin v0.1.0
```

---

## Безопасность

- файлы создаются только внутри целевой директории;
- пути вроде `../../etc/passwd` отклоняются;
- произвольные shell-команды не выполняются;
- поддерживается только `git init` и только при явном флаге.

---

## License

MIT. Подробнее в файле `LICENSE`.
