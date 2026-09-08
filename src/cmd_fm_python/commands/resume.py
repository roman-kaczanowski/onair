from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize


class Resume(Command):
    name = 'resume'
    pattern = 'resume'
    example = ('resume',)
    description = 'Resume paused playback.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            if fm.player.is_playing:
                return fm.INDENT + colorize(Colors.RED, 'Track is already playing.')
            elif fm.player.is_paused:
                fm.player.play()
                return fm.INDENT + colorize(Colors.BLUE, '\u25b6 ' + fm.client.active_station['name'])
        return fm.INDENT + colorize(Colors.RED, 'No active players found.')
