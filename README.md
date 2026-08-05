# Project Generator

![CI](https://github.com/OWNER/strtree/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/OWNER/strtree/actions/workflows/cd.yml/badge.svg)

`strtree` вЂ” Р»РѕРєР°Р»СЊРЅС‹Р№ CLI-РёРЅСЃС‚СЂСѓРјРµРЅС‚ РґР»СЏ РіРµРЅРµСЂР°С†РёРё СЃС‚СЂСѓРєС‚СѓСЂС‹ РїСЂРѕРµРєС‚Р° РїРѕ РѕРїРёСЃР°РЅРёСЋ.

РџРѕРґРґРµСЂР¶РёРІР°РµС‚ ASCII-tree, JSON Рё YAML. РЎРѕР·РґР°С‘С‚ РїР°РїРєРё, С„Р°Р№Р»С‹, `__init__.py`, `.env`, `README.md`, `.gitignore`, `requirements.txt` Рё РґСЂСѓРіРёРµ Р±Р°Р·РѕРІС‹Рµ С„Р°Р№Р»С‹.

---

## Р’РѕР·РјРѕР¶РЅРѕСЃС‚Рё

- РіРµРЅРµСЂР°С†РёСЏ РїСЂРѕРµРєС‚Р° РёР· tree / JSON / YAML;
- СЃРѕР·РґР°РЅРёРµ РїР°РїРѕРє Рё С„Р°Р№Р»РѕРІ;
- РїРѕРґРґРµСЂР¶РєР° РєРѕРјРјРµРЅС‚Р°СЂРёРµРІ РІ СЃС‚СЂСѓРєС‚СѓСЂРµ;
- `--dry-run` СЂРµР¶РёРј;
- Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРѕРµ СЃРѕР·РґР°РЅРёРµ `__init__.py`;
- РґРѕР±Р°РІР»РµРЅРёРµ `README.md` Рё `.gitignore`;
- РѕРїС†РёРѕРЅР°Р»СЊРЅС‹Р№ `git init`;
- Р·Р°С‰РёС‚Р° РѕС‚ РЅРµР±РµР·РѕРїР°СЃРЅС‹С… РїСѓС‚РµР№;
- С‚РµСЃС‚С‹ Рё CI/CD С‡РµСЂРµР· GitHub Actions.

---

## РўСЂРµР±РѕРІР°РЅРёСЏ

- Python 3.9+
- git, РµСЃР»Рё РЅСѓР¶РµРЅ `git init`
- РѕРїС†РёРѕРЅР°Р»СЊРЅРѕ `pyyaml` РґР»СЏ YAML

---

## РЈСЃС‚Р°РЅРѕРІРєР°

```bash
git clone https://github.com/OWNER/strtree.git
cd strtree
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

Р”Р»СЏ СЂР°Р·СЂР°Р±РѕС‚РєРё:

```bash
pip install -e ".[dev,yaml]"
```

---

## РСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ

РџСЂРѕРІРµСЂРёС‚СЊ, С‡С‚Рѕ Р±СѓРґРµС‚ СЃРѕР·РґР°РЅРѕ:

```bash
strtree generate examples/telegram_bot.tree --dry-run
```

РЎРѕР·РґР°С‚СЊ РїСЂРѕРµРєС‚:

```bash
strtree generate examples/telegram_bot.tree
```

РЎРѕР·РґР°С‚СЊ РїСЂРѕРµРєС‚ СЃ `README.md`, `.gitignore` Рё `git init`:

```bash
strtree generate examples/telegram_bot.tree --git-init --add-defaults
```

РџРѕР»РЅС‹Р№ РІР°СЂРёР°РЅС‚:

```bash
strtree generate examples/telegram_bot.tree \
  --git-init \
  --add-defaults \
  --auto-init
```

---

## РћСЃРЅРѕРІРЅС‹Рµ С„Р»Р°РіРё

| Р¤Р»Р°Рі              | РћРїРёСЃР°РЅРёРµ                                   |
| ----------------- | ------------------------------------------ |
| `--dry-run`       | РїРѕРєР°Р·Р°С‚СЊ РґРµР№СЃС‚РІРёСЏ Р±РµР· СЃРѕР·РґР°РЅРёСЏ С„Р°Р№Р»РѕРІ      |
| `--force`         | РїРµСЂРµР·Р°РїРёСЃС‹РІР°С‚СЊ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ С„Р°Р№Р»С‹          |
| `--root PATH`     | РїРµСЂРµРѕРїСЂРµРґРµР»РёС‚СЊ РєРѕСЂРµРЅСЊ РїСЂРѕРµРєС‚Р°              |
| `--git-init`      | РІС‹РїРѕР»РЅРёС‚СЊ `git init`                       |
| `--no-git-init`   | РЅРµ РІС‹РїРѕР»РЅСЏС‚СЊ `git init`                    |
| `--add-defaults`  | РґРѕР±Р°РІРёС‚СЊ `README.md` Рё `.gitignore`        |
| `--add-readme`    | РґРѕР±Р°РІРёС‚СЊ `README.md`                       |
| `--add-gitignore` | РґРѕР±Р°РІРёС‚СЊ `.gitignore`                      |
| `--auto-init`     | СЃРѕР·РґР°С‚СЊ `__init__.py` РІ РїР°РїРєР°С…             |
| `--empty-files`   | СЃРѕР·РґР°РІР°С‚СЊ С„Р°Р№Р»С‹ Р±РµР· РґРµС„РѕР»С‚РЅРѕРіРѕ СЃРѕРґРµСЂР¶РёРјРѕРіРѕ |

---

## РџСЂРёРјРµСЂ tree-СЃС‚СЂСѓРєС‚СѓСЂС‹

```text
my_bot_project/
в”‚
в”њв”Ђв”Ђ handlers/              # РћР±СЂР°Р±РѕС‚С‡РёРєРё СЃРѕРѕР±С‰РµРЅРёР№ Рё РєРѕРјР°РЅРґ
в”‚   в”њв”Ђв”Ђ __init__.py
в”‚   в”њв”Ђв”Ђ start.py           # РљРѕРјР°РЅРґС‹ /start, /help
в”‚   в””в”Ђв”Ђ admin.py           # РџР°РЅРµР»СЊ СѓРїСЂР°РІР»РµРЅРёСЏ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РѕСЂР°
в”‚
в”њв”Ђв”Ђ keyboards/             # РљРЅРѕРїРєРё Рё РјРµРЅСЋ
в”‚   в”њв”Ђв”Ђ __init__.py
в”‚   в”њв”Ђв”Ђ reply.py
в”‚   в””в”Ђв”Ђ inline.py
в”‚
в”њв”Ђв”Ђ database/
в”‚   в”њв”Ђв”Ђ __init__.py
в”‚   в”њв”Ђв”Ђ connection.py
в”‚   в””в”Ђв”Ђ requests.py
в”‚
в”њв”Ђв”Ђ .env
в”њв”Ђв”Ђ config.py
в”њв”Ђв”Ђ main.py
в””в”Ђв”Ђ requirements.txt
```

РљРѕРјРјРµРЅС‚Р°СЂРёРё РїРѕСЃР»Рµ `#` РјРѕРіСѓС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊСЃСЏ РєР°Рє РѕРїРёСЃР°РЅРёРµ С„Р°Р№Р»РѕРІ.

---

## РџСЂРёРјРµСЂ JSON

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

## РџСЂРёРјРµСЂ YAML

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

## Р—Р°РїСѓСЃРє Р±РµР· СѓСЃС‚Р°РЅРѕРІРєРё

Linux / macOS:

```bash
PYTHONPATH=src python -m strtree.cli generate examples/telegram_bot.tree --dry-run
```

Windows:

```bash
set PYTHONPATH=src
python -m strtree.cli generate examples/telegram_bot.tree --dry-run
```

---

## Р Р°Р·СЂР°Р±РѕС‚РєР°

РЈСЃС‚Р°РЅРѕРІРєР° dev-Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№:

```bash
pip install -e ".[dev,yaml]"
```

РўРµСЃС‚С‹:

```bash
pytest
```

Р›РёРЅС‚РµСЂ:

```bash
ruff check src tests
```

РЎР±РѕСЂРєР° РїР°РєРµС‚Р°:

```bash
python -m build
```

РџСЂРѕРІРµСЂРєР° РїР°РєРµС‚Р°:

```bash
twine check dist/*
```

---

## РЎС‚СЂСѓРєС‚СѓСЂР° РїСЂРѕРµРєС‚Р°

```text
strtree/
в”‚
в”њв”Ђв”Ђ .github/
в”‚   в”њв”Ђв”Ђ dependabot.yml
в”‚   в””в”Ђв”Ђ workflows/
в”‚       в”њв”Ђв”Ђ ci.yml
в”‚       в””в”Ђв”Ђ cd.yml
в”‚
в”њв”Ђв”Ђ examples/
в”‚   в”њв”Ђв”Ђ telegram_bot.tree
в”‚   в”њв”Ђв”Ђ project.json
в”‚   в””в”Ђв”Ђ project.yaml
в”‚
в”њв”Ђв”Ђ src/
в”‚   в””в”Ђв”Ђ strtree/
в”‚       в”њв”Ђв”Ђ __init__.py
в”‚       в”њв”Ђв”Ђ cli.py
в”‚       в”њв”Ђв”Ђ models.py
в”‚       в”њв”Ђв”Ђ security.py
в”‚       в”њв”Ђв”Ђ templates.py
в”‚       в”њв”Ђв”Ђ actions.py
в”‚       в”њв”Ђв”Ђ executor.py
в”‚       в””в”Ђв”Ђ parsers/
в”‚           в”њв”Ђв”Ђ __init__.py
в”‚           в”њв”Ђв”Ђ tree.py
в”‚           в””в”Ђв”Ђ dict_parser.py
в”‚
в”њв”Ђв”Ђ tests/
в”њв”Ђв”Ђ README.md
в”њв”Ђв”Ђ LICENSE
в”њв”Ђв”Ђ .gitignore
в””в”Ђв”Ђ pyproject.toml
```

---

## CI/CD

CI Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ РЅР° РєР°Р¶РґС‹Р№ pull request Рё push РІ `main`.

Р§С‚Рѕ РґРµР»Р°РµС‚ CI:

- Р»РёРЅС‚РµСЂ С‡РµСЂРµР· Ruff;
- С‚РµСЃС‚С‹ РЅР° Python 3.9вЂ“3.12.

CD Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ РїСЂРё С‚РµРіРµ РІРёРґР°:

```bash
v0.1.0
```

Р§С‚Рѕ РґРµР»Р°РµС‚ CD:

- С‚РµСЃС‚С‹ РїРµСЂРµРґ СЂРµР»РёР·РѕРј;
- СЃР±РѕСЂРєР° РїР°РєРµС‚Р°;
- РїСЂРѕРІРµСЂРєР° РїР°РєРµС‚Р°;
- GitHub Release;
- РѕРїС†РёРѕРЅР°Р»СЊРЅР°СЏ РїСѓР±Р»РёРєР°С†РёСЏ РІ PyPI.

---

## Р РµР»РёР·

РћР±РЅРѕРІРё РІРµСЂСЃРёСЋ РІ:

```text
pyproject.toml
src/strtree/__init__.py
```

Р—Р°С‚РµРј:

```bash
git add pyproject.toml src/strtree/__init__.py
git commit -m "Bump version"
git push

git tag v0.1.0
git push origin v0.1.0
```

---

## Р‘РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ

- С„Р°Р№Р»С‹ СЃРѕР·РґР°СЋС‚СЃСЏ С‚РѕР»СЊРєРѕ РІРЅСѓС‚СЂРё С†РµР»РµРІРѕР№ РґРёСЂРµРєС‚РѕСЂРёРё;
- РїСѓС‚Рё РІСЂРѕРґРµ `../../etc/passwd` РѕС‚РєР»РѕРЅСЏСЋС‚СЃСЏ;
- РїСЂРѕРёР·РІРѕР»СЊРЅС‹Рµ shell-РєРѕРјР°РЅРґС‹ РЅРµ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ;
- РїРѕРґРґРµСЂР¶РёРІР°РµС‚СЃСЏ С‚РѕР»СЊРєРѕ `git init` Рё С‚РѕР»СЊРєРѕ РїСЂРё СЏРІРЅРѕРј С„Р»Р°РіРµ.

---

## License

MIT. РџРѕРґСЂРѕР±РЅРµРµ РІ С„Р°Р№Р»Рµ `LICENSE`.

