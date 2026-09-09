from typing import Any

from onair.commands.base import Command
from onair.commands.play import now_playing, start_stream
from onair.utils.colorize import Colors, colorize


class Next(Command):
    name = 'next'
    pattern = 'next'
    example = (
        'next',
        'skip',
    )
    description = 'Play the next station in this genre.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if not app.client or not app.client.current_tag:
            return app.INDENT + colorize(Colors.RED, 'No active station. Use play {genre} first.')

        for _ in range(3):
            stream = app.client.next_station()
            if not stream:
                break
            if start_stream(app, stream):
                return now_playing(app)
        return app.INDENT + colorize(Colors.RED, 'No other stations found... Please, try another genre.')


class Skip(Next):
    name = 'skip'
    pattern = 'skip'
    example = (
        'skip',
        'next',
    )
    show_in_main_help = False
