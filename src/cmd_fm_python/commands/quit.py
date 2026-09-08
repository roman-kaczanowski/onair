import sys
from typing import Any

from cmd_fm_python.commands.base import Command


class Quit(Command):
    name = 'quit'
    pattern = 'quit'
    example = (
        'quit',
        'q',
    )
    description = 'Close cmd.fm and turn off music.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            fm.player.stop()
        sys.exit()


class Q(Quit):
    name = 'q'
    pattern = 'q'
    example = (
        'q',
        'quit',
    )
    show_in_main_help = False
