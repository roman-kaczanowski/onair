from typing import Any

from onair.commands.base import Command
from onair.commands.play import now_playing
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
                return app.INDENT + colorize(Colors.RED, 'Playback is already running.')
            elif app.player.is_paused:
                app.player.play()
                return now_playing(app)
        return app.INDENT + colorize(Colors.RED, 'Nothing is playing.')
