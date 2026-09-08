from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


class Unmute(Command):
    name = 'unmute'
    pattern = 'unmute'
    example = (
        'unmute',
        'um',
    )
    description = 'Unmute current track.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            app.player.unmute()
            return app.INDENT + colorize(Colors.GREEN, 'Track unmuted.')
        return app.INDENT + colorize(Colors.RED, 'No active players found.')


class Um(Unmute):
    name = 'um'
    pattern = 'um'
    example = (
        'um',
        'unmute',
    )
    show_in_main_help = False
