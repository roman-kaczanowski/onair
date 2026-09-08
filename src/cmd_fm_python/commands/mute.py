from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize


class Mute(Command):
    name = 'mute'
    pattern = 'mute'
    example = (
        'mute',
        'm',
    )
    description = 'Mute current track.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            fm.player.mute()
            return fm.INDENT + colorize(Colors.GREEN, 'Track muted.')
        return fm.INDENT + colorize(Colors.RED, 'No active players found.')


class M(Mute):
    name = 'm'
    pattern = 'm'
    example = (
        'm',
        'mute',
    )
    show_in_main_help = False
