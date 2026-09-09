from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import PREVIEW_LIMIT, filter_grouped_titles, format_grouped_titles


class Genres(Command):
    name = 'genres'
    pattern = 'genres {filter}'
    example = (
        'genres',
        'genres hip',
    )
    description = 'Lists genres, optionally filtered by name.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = ' '.join(args)
        preview = arg == 'withintro'
        titles = app.client.home_genres_titles if preview else filter_grouped_titles(app.client.genres_titles, arg)

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
                '\n' + app.INDENT + '{{l}}... {{e-y}}Show more via{{e}} genres {{y}}or play a genre:{{e}} play kpop'
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
                '\n\n' + app.INDENT + '{{y}}Start listening by typing{{e}} play {genre} {{y}}command: {{e}}play kpop\n'
            )

        if not titles:
            if arg and not preview:
                return header + colorize(Colors.RED, 'No genres matching ') + arg + '.\n'
            return header + colorize(
                Colors.RED, "Genres list is empty. Seems API isn't available. Please, try again later.\n"
            )

        return header + format_grouped_titles(titles, app.INDENT, limit=PREVIEW_LIMIT if preview else None) + footer
