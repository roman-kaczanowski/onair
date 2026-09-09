from typing import Any

from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize


class Info(Command):
    name = 'info'
    pattern = 'info'
    example = (
        'info',
        'i',
        'information',
    )
    description = 'Show details for the current station.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        station = app.client.active_station if app.client else None
        if not station:
            return app.INDENT + colorize(Colors.RED, 'No station is tuned.')

        location = ', '.join(part for part in (station.state, station.country or station.countrycode) if part)
        codec = station.codec
        if station.bitrate:
            codec = f'{codec} {station.bitrate} kbps'.strip() if codec else f'{station.bitrate} kbps'

        lines = [app.INDENT + colorize(Colors.BLUE, station.name)]
        fields = (
            ('Tags', station.tags),
            ('Location', location),
            ('Language', station.language),
            ('Codec', codec),
            ('Homepage', station.homepage),
        )
        for label, value in fields:
            if value:
                lines.append(app.INDENT + colorize(Colors.GREEN, f'{label}: ') + value)
        return '\n'.join(lines)


class InfoI(Info):
    name = 'i'
    pattern = 'i'
    example = (
        'i',
        'info',
        'information',
    )
    show_in_main_help = False


class Information(Info):
    name = 'information'
    pattern = 'information'
    example = (
        'information',
        'i',
        'info',
    )
    show_in_main_help = False
