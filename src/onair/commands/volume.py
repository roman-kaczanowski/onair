from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


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
    def handle(app: Any, *args: str) -> str:
        if app.player:
            arg = args[0] if args else ''

            if not arg:
                return app.INDENT + colorize(Colors.GREEN, 'Current volume is ') + str(app.player.get_volume())

            try:
                app.player.set_volume(int(arg))
            except ValueError:
                return app.INDENT + colorize(Colors.RED, 'Volume value ') + arg + colorize(Colors.RED, " isn't valid.")
            return app.INDENT + colorize(Colors.GREEN, 'Set volume to ') + arg
        return app.INDENT + colorize(Colors.RED, 'No active players found.')


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
