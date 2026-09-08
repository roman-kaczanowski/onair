import random
import time
from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.player.player import Player
from cmd_fm_python.utils.colorize import Colors, colorize


class Play(Command):
    name = 'play'
    pattern = 'play {genre}'
    example = (
        'play chillout',
        'p jazz',
    )
    description = 'Use this command to play genres and resume paused track.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        arg = args[0] if args else ''

        if not arg:
            if fm.player and fm.player.is_paused:
                fm.player.play()
                return fm.INDENT + colorize(Colors.BLUE, '\u25b6 ' + fm.client.active_station['name'])

            fm.stdout_print(fm.INDENT + colorize(Colors.GRAY, 'Pick random genre...'))
            arg = random.choice([genre.get('title', '') for genre in fm.client.genres])

        genre = fm.client.search_genre(arg)
        genre_id = genre.get('id') if genre else None

        if genre_id is None:
            return fm.INDENT + colorize(Colors.RED, 'Genre ') + arg + colorize(Colors.RED, ' not found.')

        fm.stdout_print(fm.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        fm.stdout_print(fm.INDENT + colorize(Colors.GREEN, 'Starting genre: ') + genre.get('title', ''))

        num_of_tries = 0
        while num_of_tries < 3:
            num_of_tries += 1
            stream = fm.client.get_stream(genre_id, renew_active_station=True)

            if not stream:
                return fm.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')

            if fm.player:
                fm.player.stop()
            fm.player = Player(stream)
            fm.player.play()

            num_of_checks = 0
            while num_of_checks < 5:
                num_of_checks += 1
                time.sleep(1)
                if fm.player.is_playing:
                    return fm.INDENT + colorize(Colors.BLUE, '\u25b6 ' + fm.client.active_station['name'])
        return fm.INDENT + colorize(Colors.RED, 'No active stations found... Please, try another genre.')


class P(Play):
    name = 'p'
    pattern = 'p {genre}'
    example = (
        'p chillout',
        'play jazz',
    )
    show_in_main_help = False
