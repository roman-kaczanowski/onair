from typing import Any

from onair.commands.base import Command, CommandError
from onair.commands.play import starting_message, try_tune
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import filter_grouped_titles, format_grouped_titles


class Countries(Command):
    name = 'countries'
    pattern = 'countries [filter]'
    example = (
        'countries',
        'countries pol',
    )
    description = 'List countries, optionally filtered by name or code.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        needle = ' '.join(args)
        titles = filter_grouped_titles(app.client.countries_titles if app.client else {}, needle)
        header = render(
            '\n'
            + app.INDENT
            + '{{y}}--- COUNTRIES -------------------------------------------------{{e}}'
            + '\n\n'
            + app.INDENT
        )
        footer = render(
            '\n\n'
            + app.INDENT
            + '{{y}}Start listening with{{e}} country [name]{{y}}. For example:{{e}} country poland\n'
        )
        if not titles:
            if needle:
                raise CommandError(header + colorize(Colors.RED, 'No countries matching ') + needle + '.\n')
            raise CommandError(
                header
                + colorize(
                    Colors.RED,
                    'The country list is empty. The Radio Browser API may be unavailable. Try again later.\n',
                )
            )
        return header + format_grouped_titles(titles, app.INDENT) + footer


class Country(Command):
    name = 'country'
    pattern = 'country [name]'
    example = (
        'country poland',
        'c PL',
    )
    description = 'Play a station from a country.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = ' '.join(args)
        if not arg:
            raise CommandError(app.INDENT + colorize(Colors.RED, 'Specify a country. Example: ') + 'country poland')

        country = app.client.search_country(arg) if app.client else None
        code = country.get('iso') if country else None
        if not country or not code:
            raise CommandError(
                app.INDENT + colorize(Colors.RED, 'Country ') + arg + colorize(Colors.RED, ' not found.')
            )

        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        app.stdout_print(starting_message(app, 'country', country.get('name', code)))
        return try_tune(app, countrycode=code)


class C(Country):
    name = 'c'
    pattern = 'c [name]'
    example = (
        'c poland',
        'country PL',
    )
    show_in_main_help = False
