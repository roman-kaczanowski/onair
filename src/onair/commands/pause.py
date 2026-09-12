from typing import Any

from onair.commands.base import Command, CommandError
from onair.utils.colorize import Colors, colorize


class Pause(Command):
    name = 'pause'
    pattern = 'pause'
    example = ('pause',)
    description = 'Pause playback.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        if app.player:
            if app.player.is_playing:
                app.player.pause()
                return app.INDENT + colorize(Colors.GREEN, 'Playback paused.')
            elif app.player.is_paused:
                raise CommandError(app.INDENT + colorize(Colors.RED, 'Playback is already paused.'))
        raise CommandError(app.INDENT + colorize(Colors.RED, 'Nothing is playing.'))
