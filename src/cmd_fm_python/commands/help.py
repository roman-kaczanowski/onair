from typing import Any

from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import render


class Help(Command):
    name = 'help'
    pattern = 'help {cmd}'
    example = (
        'help',
        'help play',
        'help i',
    )
    description = 'Lists all available commands or shows detailed info about selected command.'

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        arg = args[0] if args else ''

        if arg:
            for command in fm.commands:
                if arg == command.name:
                    return command.help()
            return render(
                fm.INDENT
                + '{{r}}Command{{e-y}} '
                + arg
                + ' {{e-r}}not found. You can use{{e}} help {{r}}command to see all available commands.{{e}}'
            )

        main_help = ''
        for command in fm.commands:
            main_help += command.one_line_help()
        return main_help
