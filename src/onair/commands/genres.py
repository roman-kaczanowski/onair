from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import PREVIEW_LIMIT, filter_grouped_titles, format_grouped_titles


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
        preview = arg == 'withintro'
        grouped = {}
        if app.client:
            grouped = app.client.home_genres_titles if preview else app.client.genres_titles
        titles = grouped if preview else filter_grouped_titles(grouped, arg)

        if preview:
            header = (
                app.intro
                + '\n'
                + app.INDENT
                + render('{{y}}--- GENRES ----------------------------------------------------{{e}}')
                + '\n'
                + app.INDENT
            )
            footer = render(
                '\n' + app.INDENT + '{{l}}... {{e-y}}Run{{e}} genres {{y}}to see more, or try{{e}} play kpop'
            )
        else:
            header = render(
                '\n'
                + app.INDENT
                + '{{y}}--- GENRES ----------------------------------------------------{{e}}'
                + '\n\n'
                + app.INDENT
            )
            footer = render(
                '\n\n' + app.INDENT + '{{y}}Start listening with{{e}} play {genre}{{y}}. For example:{{e}} play kpop\n'
            )

        if not titles:
            if arg and not preview:
                return header + colorize(Colors.RED, 'No genres matching ') + arg + '.\n'
            return header + colorize(
                Colors.RED, 'The genre list is empty. The Radio Browser API may be unavailable. Try again later.\n'
            )

        return header + format_grouped_titles(titles, app.INDENT, limit=PREVIEW_LIMIT if preview else None) + footer
