from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize, render


class Genres(Command):
    name = 'genres'
    pattern = 'genres'
    example = ('genres',)
    description = 'Lists all available genres.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        arg = args[0] if args else ''
        titles = fm.client.genres_titles
        titles_keys = sorted(titles.keys())

        header = render(
            '\n'
            + fm.INDENT
            + '{{y}}--- GENRES ----------------------------------------------------{{e}}'
            + '\n\n'
            + fm.INDENT
        )

        footer = render(
            '\n\n' + fm.INDENT + '{{y}}Start listening by typing{{e}} play {genre} {{y}}command: {{e}}play kpop\n'
        )

        if arg == 'withintro':
            header = fm.intro + header
            footer = (
                render(
                    '\n' + fm.INDENT + '{{l}}... {{e-y}}Show more available genres via{{e}} genres {{y}}command{{e}}'
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
            + ('\n' + fm.INDENT).join(
                colorize(Colors.LIME, k + ' - ') + colorize(Colors.LIME, ', ').join(titles[k]) for k in titles_keys
            )
            + footer
        )
