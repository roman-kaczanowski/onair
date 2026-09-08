from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize, render


class Genres(Command):
    name = 'genres'
    pattern = 'genres'
    example = ('genres',)
    description = 'Lists all available genres.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = args[0] if args else ''
        titles = app.client.genres_titles
        titles_keys = sorted(titles.keys())

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

        if arg == 'withintro':
            header = app.intro + header
            footer = (
                render(
                    '\n' + app.INDENT + '{{l}}... {{e-y}}Show more available genres via{{e}} genres {{y}}command{{e}}'
                )
                + footer
            )
            titles_keys = titles_keys[:5]

        if not titles:
            return header + colorize(
                Colors.RED, "Genres list is empty. Seems API isn't available. Please, try again later.\n"
            )

        return (
            header
            + ('\n' + app.INDENT).join(
                colorize(Colors.LIME, k + ' - ') + colorize(Colors.LIME, ', ').join(titles[k]) for k in titles_keys
            )
            + footer
        )
