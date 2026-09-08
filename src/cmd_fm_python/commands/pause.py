from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize


class Pause(Command):
    name = 'pause'
    pattern = 'pause'
    example = ('pause',)
    description = 'Pause playback.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            if fm.player.is_playing:
                fm.player.pause()
                return fm.INDENT + colorize(Colors.GREEN, 'Track paused.')
            elif fm.player.is_paused:
                return fm.INDENT + colorize(Colors.RED, 'Track already paused.')
        return fm.INDENT + colorize(Colors.RED, 'No active players found.')
