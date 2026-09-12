from typing import Any

from onair.commands.base import Command, CommandError
from onair.commands.play import now_playing, start_stream
from onair.utils.colorize import Colors, colorize


class Previous(Command):
    name = 'previous'
    pattern = 'previous'
    example = (
        'previous',
        'prev',
        'back',
    )
    description = 'Play the previous station.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if not app.client:
            raise CommandError(app.INDENT + colorize(Colors.RED, 'No previous station.'))

        stream = app.client.previous_station()
        if not stream:
            raise CommandError(app.INDENT + colorize(Colors.RED, 'No previous station.'))
        if start_stream(app, stream):
            return now_playing(app)
        raise CommandError(app.INDENT + colorize(Colors.RED, 'Failed to play the previous station.'))


class Prev(Previous):
    name = 'prev'
    pattern = 'prev'
    example = (
        'prev',
        'previous',
        'back',
    )
    show_in_main_help = False


class Back(Previous):
    name = 'back'
    pattern = 'back'
    example = (
        'back',
        'previous',
        'prev',
    )
    show_in_main_help = False
