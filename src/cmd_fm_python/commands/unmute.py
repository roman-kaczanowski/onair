from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize


class Unmute(Command):
    name = 'unmute'
    pattern = 'unmute'
    example = (
        'unmute',
        'um',
    )
    description = 'Unmute current track.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            fm.player.unmute()
            return fm.INDENT + colorize(Colors.GREEN, 'Track unmuted.')
        return fm.INDENT + colorize(Colors.RED, 'No active players found.')


class Um(Unmute):
    name = 'um'
    pattern = 'um'
    example = (
        'um',
        'unmute',
    )
    show_in_main_help = False
