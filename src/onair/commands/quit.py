import sys
from typing import Any

from onair.commands.base import Command


class Quit(Command):
    name = 'quit'
    pattern = 'quit'
    example = (
        'quit',
        'q',
    )
    description = 'Quit and turn off music.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            app.player.stop()
        sys.exit()


class Q(Quit):
    name = 'q'
    pattern = 'q'
    example = (
        'q',
        'quit',
    )
    show_in_main_help = False
