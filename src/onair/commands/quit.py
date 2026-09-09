import sys
from typing import Any, Never

from onair.commands.base import Command


class Quit(Command):
    name = 'quit'
    pattern = 'quit'
    example = (
        'quit',
        'exit',
        'q',
        'e',
    )
    description = 'Quit and stop playback.'

    @staticmethod
    def handle(app: Any, *args: str) -> Never:
        if app.player:
            app.player.stop()
        sys.exit()


class Q(Quit):
    name = 'q'
    pattern = 'q'
    example = (
        'q',
        'quit',
        'exit',
        'e',
    )
    show_in_main_help = False


class Exit(Quit):
    name = 'exit'
    pattern = 'exit'
    example = (
        'exit',
        'quit',
        'q',
        'e',
    )
    show_in_main_help = False


class E(Quit):
    name = 'e'
    pattern = 'e'
    example = (
        'e',
        'quit',
        'exit',
        'q',
    )
    show_in_main_help = False
