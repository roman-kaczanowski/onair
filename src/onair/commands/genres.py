from typing import Any

from onair.commands.base import Command, CommandError
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import PREVIEW_LIMIT, filter_grouped_titles, format_grouped_titles


def home_preview(app: Any) -> str:
    grouped = app.client.home_genres_titles if app.client else {}
    header = (
        app.INDENT
        + render('{{y}}--- GENRES ----------------------------------------------------{{e}}')
        + '\n'
        + app.INDENT
    )
    footer = render('\n' + app.INDENT + '{{l}}... {{e-y}}Run{{e}} genres {{y}}to see more, or try{{e}} play kpop')
    if not grouped:
        return header + colorize(
            Colors.RED, 'The genre list is empty. The Radio Browser API may be unavailable. Try again later.\n'
        )
    return header + format_grouped_titles(grouped, app.INDENT, limit=PREVIEW_LIMIT) + footer


class Genres(Command):
    name = 'genres'
    pattern = 'genres [filter]'
    example = (
        'genres',
        'genres hip',
    )
    description = 'List genres, optionally filtered by name.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = ' '.join(args)
        grouped = app.client.genres_titles if app.client else {}
        titles = filter_grouped_titles(grouped, arg)
        header = render(
            '\n'
            + app.INDENT
            + '{{y}}--- GENRES ----------------------------------------------------{{e}}'
            + '\n\n'
            + app.INDENT
        )
        footer = render(
            '\n\n' + app.INDENT + '{{y}}Start listening with{{e}} play [genre]{{y}}. For example:{{e}} play kpop\n'
        )
        if not titles:
            if arg:
                raise CommandError(header + colorize(Colors.RED, 'No genres matching ') + arg + '.\n')
            raise CommandError(
                header
                + colorize(
                    Colors.RED,
                    'The genre list is empty. The Radio Browser API may be unavailable. Try again later.\n',
                )
            )
        return header + format_grouped_titles(titles, app.INDENT) + footer
