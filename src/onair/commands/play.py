import random
import time
from typing import Any

from onair.commands.base import Command
from onair.player.player import Player
from onair.utils.colorize import Colors, colorize


def start_stream(app: Any, stream: str) -> bool:
    if app.player:
        app.player.stop()
    app.player = Player(stream)
    app.player.play()
    for _ in range(5):
        if app.player.is_playing:
            return True
        time.sleep(1)
    return False


def now_playing(app: Any) -> str:
    station = app.client.active_station if app.client else None
    name = station.name if station else ''
    return app.INDENT + colorize(Colors.BLUE, '\u25b6 ' + name)


class Play(Command):
    name = 'play'
    pattern = 'play {genre}'
    example = (
        'play chillout',
        'p jazz',
    )
    description = 'Use this command to play genres and resume paused track.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = args[0] if args else ''

        if not arg:
            if app.player and app.player.is_paused:
                app.player.play()
                return now_playing(app)

            if not app.client or not app.client.genres:
                return app.INDENT + colorize(Colors.RED, 'No genres available. Please, try again later.')

            app.stdout_print(app.INDENT + colorize(Colors.GRAY, 'Pick random genre...'))
            arg = random.choice([genre.get('title', '') for genre in app.client.genres])

        genre = app.client.search_genre(arg) if app.client else None
        tag = genre.get('id') if genre else None

        if not tag:
            return app.INDENT + colorize(Colors.RED, 'Genre ') + arg + colorize(Colors.RED, ' not found.')

        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Starting genre: ') + genre.get('title', ''))

        for _ in range(3):
            stream = app.client.get_stream(tag, renew_active_station=True)
            if not stream:
                return app.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')
            if start_stream(app, stream):
                return now_playing(app)
        return app.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')


class P(Play):
    name = 'p'
    pattern = 'p {genre}'
    example = (
        'p chillout',
        'play jazz',
    )
    show_in_main_help = False
