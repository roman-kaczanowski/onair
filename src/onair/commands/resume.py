from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


class Resume(Command):
    name = 'resume'
    pattern = 'resume'
    example = ('resume',)
    description = 'Resume paused playback.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            if app.player.is_playing:
                return app.INDENT + colorize(Colors.RED, 'Track is already playing.')
            elif app.player.is_paused:
                app.player.play()
                return app.INDENT + colorize(Colors.BLUE, '\u25b6 ' + app.client.active_station['name'])
        return app.INDENT + colorize(Colors.RED, 'No active players found.')
