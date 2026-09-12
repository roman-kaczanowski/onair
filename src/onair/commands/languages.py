from typing import Any

from onair.commands.base import Command, CommandError
from onair.commands.play import starting_message, try_tune
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import filter_grouped_titles, format_grouped_titles


class Languages(Command):
    name = 'languages'
    pattern = 'languages [filter]'
    example = (
        'languages',
        'languages pol',
    )
    description = 'List languages, optionally filtered by name or code.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        needle = ' '.join(args)
        titles = filter_grouped_titles(app.client.languages_titles if app.client else {}, needle)
        header = render(
            '\n'
            + app.INDENT
            + '{{y}}--- LANGUAGES -------------------------------------------------{{e}}'
            + '\n\n'
            + app.INDENT
        )
        footer = render(
            '\n\n'
            + app.INDENT
            + '{{y}}Start listening with{{e}} language [name]{{y}}. For example:{{e}} language polish\n'
        )
        if not titles:
            if needle:
                raise CommandError(header + colorize(Colors.RED, 'No languages matching ') + needle + '.\n')
            raise CommandError(
                header
                + colorize(
                    Colors.RED,
                    'The language list is empty. The Radio Browser API may be unavailable. Try again later.\n',
                )
            )
        return header + format_grouped_titles(titles, app.INDENT) + footer


class Language(Command):
    name = 'language'
    pattern = 'language [name]'
    example = (
        'language polish',
        'l en',
    )
    description = 'Play a station in a language.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = ' '.join(args)
        if not arg:
            raise CommandError(app.INDENT + colorize(Colors.RED, 'Specify a language. Example: ') + 'language polish')

        language = app.client.search_language(arg) if app.client else None
        name = language.get('name') if language else None
        if not language or not name:
            raise CommandError(
                app.INDENT + colorize(Colors.RED, 'Language ') + arg + colorize(Colors.RED, ' not found.')
            )

        app.stdout_print(app.INDENT + colorize(Colors.GREEN, 'Tuning in...'))
        app.stdout_print(starting_message(app, 'language', name))
        return try_tune(app, language=name)


class Lang(Language):
    name = 'lang'
    pattern = 'lang [name]'
    example = (
        'lang polish',
        'language en',
    )
    show_in_main_help = False


class L(Language):
    name = 'l'
    pattern = 'l [name]'
    example = (
        'l polish',
        'language en',
    )
    show_in_main_help = False
