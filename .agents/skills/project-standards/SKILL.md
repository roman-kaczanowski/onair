---
name: project-standards
description: Coding standards for the onair Python project. Use when writing, reviewing, refactoring, debugging, adding dependencies, or changing tests, packaging, or the agent harness.
---

# Project standards

## Before writing code

Read the task and the code it touches. Trace the real flow end to end, then stop at the first rung that holds:

1. Does this need to be built at all? (YAGNI)
2. Does it already exist in this codebase? Reuse it.
3. Does the standard library already do this? Use it.
4. Does an already-declared dependency solve it? Use it.
5. Can this be one boring line? Make it one line.
6. Only then: write the minimum code that works.

A bug fix addresses the root cause, not the symptom. Search every caller of the function you touch and fix the shared function once.

## Toolchain

- Match the existing layout: `src/` for the package, `tests/` for tests, entry point in `pyproject.toml`.
- Do not add a dependency unless it is declared in `pyproject.toml` and locked in `uv.lock`. Prefer the standard library.
- Style is enforced by Ruff. Follow `pyproject.toml`; the points below apply even when Ruff cannot check them.
- After editing Python, run `poe format`. After editing Markdown, run `poe format_docs`.

## Comments and docs

- No docstrings except on base or abstract classes and methods (the contract for implementors) and on complex functions where extra explanation genuinely helps.
- No unnecessary comments. Code should be self-explanatory. If a comment is needed, explain why, not what.
- No section-divider comments inside classes or functions. Group related methods by proximity. Dividers are allowed only in test classes.
- Mark a deliberate simplification that cuts a real corner (global lock, O(n^2) scan, naive heuristic) with a `ponytail:` comment naming the ceiling and the upgrade path.

## Language

- Type-hint every function and method. Do not nest annotations so deeply that they hurt readability.
- No unnecessary imports.
- Use f-strings for all string formatting.
- Avoid unnecessary `Path` wrappers; join with `/` on `Path` objects.
- ASCII only in identifiers, comments, and docs. No emojis. Non-ASCII letters are allowed only when the content is actually in another language.

## Quality

- Use `poe format` and `poe format_docs` instead of hand-formatting.
- Deletion over addition. Boring over clever. Fewest files possible. The shortest working diff wins once you understand the problem.
- No abstractions, boilerplate, or dependencies that were not requested.
- Question complex requests: "Do you actually need X, or does Y cover it?"
- When two standard-library approaches are the same size, pick the edge-case-correct one.
- Non-trivial logic leaves one runnable check: the smallest test that fails if the logic breaks. Run the test command before claiming work is done.
- Do not commit secrets, `.env` files, or local virtualenvs.

Not lazy about: understanding the problem, input validation at trust boundaries, error handling that prevents data loss, security, and anything explicitly requested.

## Vendored and generated files

Never read or grep a vendored or generated file whole. Search a capped slice instead, preferring portable commands such as `grep -o 'pattern' file | head` when `rg` may not be installed.

## Agent harness

- Keep root `AGENTS.md` compact and always-on. Put directory context in nested `AGENTS.md` files and task context in `.agents/skills/`.
- Use `.agents/skills/` as the shared Agent Skills location. Do not duplicate the same rule in Cursor config and AGENTS.md.
- Keep platform-specific config local. The tracked harness is `AGENTS.md`, nested `AGENTS.md`, and `.agents/`.
- If a nested `AGENTS.md` sits inside a packaged directory, keep it out of the wheel.
