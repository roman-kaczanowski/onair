# Agent instructions

`onair` is an interactive internet radio REPL for the terminal. It finds stations through Radio Browser and plays them with VLC. Python 3.12+, `uv`, Hatchling, Ruff, pytest, and `mdformat`.

## Commands

- `uv sync`: install the dev and test groups.
- `poe format` / `poe check`: format or verify Python with Ruff.
- `poe format_docs` / `poe check_docs`: format or verify tracked Markdown.
- `poe test`: run pytest.
- `uv lock --check`: verify the lockfile.
- `poe hooks`: install git hooks.

## Non-negotiables

- Treat `pyproject.toml` as the source of truth for tools, versions, and dependencies. Use `uv`.
- Type-hint every function and method. ASCII only in code, comments, and docs.
- No docstrings except on base or abstract classes and methods, and on complex functions where they genuinely help.
- Fix the root cause, not the symptom. Reuse existing code before adding abstractions.
- Run `poe check`, `poe check_docs`, and `poe test` before claiming work is done.
- Do not commit secrets, `.env` files, or local virtualenvs.

## Context

Read only what the task needs.

- `src/onair/AGENTS.md`: package map and data flow.
- `src/onair/commands/AGENTS.md`: command and alias rules.
- `tests/AGENTS.md`: test layout, fixtures, and test commands.
- `.agents/skills/project-standards/SKILL.md`: full coding standards.
- `.agents/skills/markdown/SKILL.md`: Markdown rules for `*.md`.
