import random
import time
from typing import Any

from onair.commands.base import Command
from onair.player.player import Player
from onair.utils.colorize import Colors, colorize


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
                return app.INDENT + colorize(Colors.BLUE, '\u25b6 ' + app.client.active_station['name'])

            app.stdout_print(app.INDENT + colorize(Colors.GRAY, 'Pick random genre...'))
            arg = random.choice([genre.get('title', '') for genre in app.client.genres])

        genre = app.client.search_genre(arg)
        genre_id = genre.get('id') if genre else None

        if genre_id is None:
            return app.INDENT + colorize(Colors.RED, 'Genre ') + arg + colorize(Colors.RED, ' not found.')

        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Starting genre: ') + genre.get('title', ''))

        num_of_tries = 0
        while num_of_tries < 3:
            num_of_tries += 1
            stream = app.client.get_stream(genre_id, renew_active_station=True)

            if not stream:
                return app.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')

            if app.player:
                app.player.stop()
            app.player = Player(stream)
            app.player.play()

            num_of_checks = 0
            while num_of_checks < 5:
                num_of_checks += 1
                time.sleep(1)
                if app.player.is_playing:
                    return app.INDENT + colorize(Colors.BLUE, '\u25b6 ' + app.client.active_station['name'])
        return app.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')


class P(Play):
    name = 'p'
    pattern = 'p {genre}'
    example = (
        'p chillout',
        'play jazz',
    )
    show_in_main_help = False
