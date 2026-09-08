from typing import Any

from onair.commands.base import Command


class Next(Command):
    name = 'next'
    pattern = 'next'
    example = (
        'next',
        'skip',
    )
    description = 'Skips next track.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        return 'debug: next/skip command output'


class Skip(Next):
    name = 'skip'
    pattern = 'skip'
    example = (
        'skip',
        'next',
    )
    show_in_main_help = False
