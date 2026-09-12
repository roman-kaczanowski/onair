from typing import Any

from onair.commands.base import Command, CommandError
from onair.utils.colorize import Colors, colorize


class Unmute(Command):
    name = 'unmute'
    pattern = 'unmute'
    example = (
        'unmute',
        'um',
    )
    description = 'Unmute playback.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            app.player.unmute()
            return app.INDENT + colorize(Colors.GREEN, 'Unmuted.')
        raise CommandError(app.INDENT + colorize(Colors.RED, 'Nothing is playing.'))


class Um(Unmute):
    name = 'um'
    pattern = 'um'
    example = (
        'um',
        'unmute',
    )
    show_in_main_help = False
