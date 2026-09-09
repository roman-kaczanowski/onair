from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


def parse_volume(current: int, arg: str) -> int | None:
    current = max(0, current)
    try:
        if len(arg) > 1 and arg[0] in '+-' and arg[1:].isdigit():
            value = current + int(arg)
        else:
            value = int(arg)
    except ValueError:
        return None
    return max(0, min(100, value))


class Volume(Command):
    name = 'volume'
    pattern = 'volume {n|+n|-n}'
    example = (
        'volume 45',
        'volume +10',
        'v -5',
    )
    description = 'Set volume, or change it with +n / -n.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            arg = args[0] if args else ''

            if not arg:
                return app.INDENT + colorize(Colors.GREEN, 'Current volume is ') + str(app.player.get_volume())

            value = parse_volume(app.player.get_volume(), arg)
            if value is None:
                return app.INDENT + colorize(Colors.RED, 'Volume value ') + arg + colorize(Colors.RED, " isn't valid.")
            app.player.set_volume(value)
            return app.INDENT + colorize(Colors.GREEN, 'Set volume to ') + str(value)
        return app.INDENT + colorize(Colors.RED, 'No active players found.')


class V(Volume):
    name = 'v'
    pattern = 'v {n|+n|-n}'
    example = (
        'v 45',
        'volume +10',
        'vol -5',
    )
    show_in_main_help = False


class Vol(Volume):
    name = 'vol'
    pattern = 'vol {n|+n|-n}'
    example = (
        'vol 45',
        'v +10',
        'volume 45',
    )
    show_in_main_help = False
