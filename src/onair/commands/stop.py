from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


class Stop(Command):
    name = 'stop'
    pattern = 'stop'
    example = ('stop',)
    description = 'Stop playback without leaving the shell.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            app.player.stop()
            app.player = None
            return app.INDENT + colorize(Colors.GREEN, 'Stopped.')
        return app.INDENT + colorize(Colors.RED, 'Nothing is playing.')
