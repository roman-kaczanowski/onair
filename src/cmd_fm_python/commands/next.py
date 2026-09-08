from typing import Any

from cmd_fm_python.commands.base import Command


class Next(Command):
    name = 'next'
    pattern = 'next'
    example = (
        'next',
        'skip',
    )
    description = 'Skips next track.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        return 'debug: next/skip command output'


class Skip(Next):
    name = 'skip'
    pattern = 'skip'
    example = (
        'skip',
        'next',
    )
    show_in_main_help = False
