from typing import Any

from onair.commands.base import Command


class Info(Command):
    name = 'info'
    pattern = 'info'
    example = (
        'info',
        'i',
        'information',
    )
    description = 'Shows more information about current track.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        return 'debug: i/info/information command output'


class InfoI(Info):
    name = 'i'
    pattern = 'i'
    example = (
        'i',
        'info',
        'information',
    )
    show_in_main_help = False


class Information(Info):
    name = 'information'
    pattern = 'information'
    example = (
        'information',
        'i',
        'info',
    )
    show_in_main_help = False
