from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


class Mute(Command):
    name = 'mute'
    pattern = 'mute'
    example = (
        'mute',
        'm',
    )
    description = 'Mute playback.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            app.player.mute()
            return app.INDENT + colorize(Colors.GREEN, 'Muted.')
        return app.INDENT + colorize(Colors.RED, 'Nothing is playing.')


class M(Mute):
    name = 'm'
    pattern = 'm'
    example = (
        'm',
        'mute',
    )
    show_in_main_help = False
