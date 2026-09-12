import string
from collections.abc import Iterable

from onair.utils.colorize import Colors, colorize

PREVIEW_LIMIT = 5
HOME_GROUP_LIMIT = 4
DEFAULT_TERMINAL_ROWS = 24
# prompt_toolkit PromptSession default; home screen must leave this room for the REPL.
PROMPT_MENU_RESERVE = 8
HOME_GROUP_KEYS = frozenset({'#', '@'} | set(string.ascii_uppercase))


def letter_key(title: str) -> str:
    first = title[0]
    if first in string.digits:
        return '#'
    return first.upper()


def group_by_letter(names: Iterable[str]) -> dict[str, list[str]]:
    titles: dict[str, list[str]] = {}
    for title in sorted(names):
        if not title:
            continue
        first_letter = letter_key(title)
        titles[first_letter] = titles.get(first_letter, list()) + [title]
    return titles


def filter_grouped_titles(titles: dict[str, list[str]], needle: str) -> dict[str, list[str]]:
    if not needle:
        return titles
    needle = needle.lower()
    filtered: dict[str, list[str]] = {}
    for key, names in titles.items():
        matched = [name for name in names if needle in name.lower()]
        if matched:
            filtered[key] = matched
    return filtered


def format_grouped_titles(
    titles: dict[str, list[str]],
    indent: str,
    *,
    limit: int | None = None,
) -> str:
    parts: list[str] = []
    for key in sorted(titles):
        names = titles[key]
        suffix = ''
        if limit is not None and len(names) > limit:
            names = names[:limit]
            suffix = colorize(Colors.GRAY, ', ...')
        parts.append(colorize(Colors.LIME, f'{key} - ') + colorize(Colors.LIME, ', ').join(names) + suffix)
    return ('\n' + indent).join(parts)
