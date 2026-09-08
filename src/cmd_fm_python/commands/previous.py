from typing import Any

from cmd_fm_python.commands.base import Command


class Previous(Command):
    name = 'previous'
    pattern = 'previous'
    example = (
        'previous',
        'prev',
        'back',
    )
    description = 'Skips previous track'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        return 'debug: prev/previous/back command output.'


class Prev(Previous):
    name = 'prev'
    pattern = 'prev'
    example = (
        'prev',
        'previous',
        'back',
    )
    show_in_main_help = False


class Back(Previous):
    name = 'back'
    pattern = 'back'
    example = (
        'back',
        'previous',
        'prev',
    )
    show_in_main_help = False
