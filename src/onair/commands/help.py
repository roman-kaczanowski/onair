from typing import Any

from onair.commands.base import Command, CommandError
from onair.utils.colorize import render


class Help(Command):
    name = 'help'
    pattern = 'help [command]'
    example = (
        'help',
        'help play',
        'help i',
    )
    description = 'List commands or show help for one command.'

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        arg = args[0] if args else ''

        if arg:
            for command in app.commands:
                if arg == command.name:
                    return command.help()
            raise CommandError(
                render(
                    app.INDENT
                    + '{{r}}Command "{{e-y}}'
                    + arg
                    + '{{e-r}}" not found. Run{{e}} help {{r}}to list available commands.{{e}}'
                )
            )

        main_help = ''
        for command in app.commands:
            main_help += command.one_line_help()
        return main_help
