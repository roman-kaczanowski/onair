import random
import time
from typing import Any

from onair.commands.base import Command, CommandError
from onair.player.player import DEFAULT_VOLUME, Player
from onair.utils.colorize import Colors, colorize


def session_volume(app: Any) -> int:
    value = getattr(app, 'volume', DEFAULT_VOLUME)
    if app.player:
        current = app.player.get_volume()
        if isinstance(current, int) and current >= 0:
            value = current
    return max(0, min(100, value))


def start_stream(app: Any, stream: str) -> bool:
    volume = session_volume(app)
    if app.player:
        app.player.stop()
    app.player = None
    player = None
    try:
        player = Player(stream, volume=volume)
        app.player = player
        player.play()
        player.set_volume(volume)
        app.volume = volume
        for _ in range(5):
            if player.is_playing:
                player.set_volume(volume)
                return True
            time.sleep(1)
    except BaseException:
        if player:
            player.stop()
        app.player = None
        raise
    player.stop()
    app.player = None
    return False


def now_playing(app: Any) -> str:
    station = app.client.active_station if app.client else None
    name = station.name if station else ''
    return app.INDENT + colorize(Colors.BLUE, f'Now playing: {name}')


def starting_message(app: Any, kind: str, name: str) -> str:
    return (
        app.INDENT
        + colorize(Colors.GREEN, f'{kind.capitalize()}: ')
        + name
        + colorize(Colors.GREEN, '  Volume: ')
        + str(session_volume(app))
    )


def try_tune(app: Any, *, tag: str | None = None, countrycode: str | None = None, language: str | None = None) -> str:
    missing = app.INDENT + colorize(Colors.RED, 'No working stations found. Try another genre, country, or language.')
    if not app.client:
        raise CommandError(missing)
    for _ in range(3):
        stream = app.client.get_stream(tag, renew_active_station=True, countrycode=countrycode, language=language)
        if not stream:
            raise CommandError(missing)
        if start_stream(app, stream):
            return now_playing(app)
    raise CommandError(missing)


class Play(Command):
    name = 'play'
    pattern = 'play [genre]'
    example = (
        'play chillout',
        'p jazz',
    )
    description = 'Play a genre, resume playback, or pick a genre at random.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = ' '.join(args)

        if not arg:
            if app.player and app.player.is_paused:
                app.player.play()
                return now_playing(app)

            if not app.client or not app.client.genres:
                raise CommandError(app.INDENT + colorize(Colors.RED, 'No genres available. Try again later.'))

            app.stdout_print(app.INDENT + colorize(Colors.GRAY, 'Picking a random genre...'))
            arg = random.choice([genre.get('title', '') for genre in app.client.genres])

        genre = app.client.search_genre(arg) if app.client else None
        tag = genre.get('id') if genre else None

        if not tag:
            raise CommandError(app.INDENT + colorize(Colors.RED, 'Genre ') + arg + colorize(Colors.RED, ' not found.'))

        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        app.stdout_print(starting_message(app, 'genre', genre.get('title', '')))
        return try_tune(app, tag=tag)


class P(Play):
    name = 'p'
    pattern = 'p [genre]'
    example = (
        'p chillout',
        'play jazz',
    )
    show_in_main_help = False
