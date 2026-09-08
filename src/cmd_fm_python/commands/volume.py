from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize


class Volume(Command):
    name = 'volume'
    pattern = 'volume {n}'
    example = (
        'volume 45',
        'v 45',
        'vol 45',
    )
    description = 'Set volume level in percentage.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        if fm.player:
            arg = args[0] if args else ''

            if not arg:
                return fm.INDENT + colorize(Colors.GREEN, 'Current volume is ') + str(fm.player.get_volume())

            try:
                fm.player.set_volume(int(arg))
            except ValueError:
                return fm.INDENT + colorize(Colors.RED, 'Volume value ') + arg + colorize(Colors.RED, " isn't valid.")
            return fm.INDENT + colorize(Colors.GREEN, 'Set volume to ') + arg
        return fm.INDENT + colorize(Colors.RED, 'No active players found.')


class V(Volume):
    name = 'v'
    pattern = 'v {n}'
    example = (
        'v 45',
        'volume 45',
        'vol 45',
    )
    show_in_main_help = False


class Vol(Volume):
    name = 'vol'
    pattern = 'vol {n}'
    example = (
        'vol 45',
        'v 45',
        'volume 45',
    )
    show_in_main_help = False
