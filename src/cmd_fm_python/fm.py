import cmd
import os
from typing import Any

from cmd_fm_python.client.client import DirbleClient
from cmd_fm_python.commands import commands
from cmd_fm_python.commands.base import Command
from cmd_fm_python.utils.colorize import Colors, colorize, render


class Fm(cmd.Cmd):
    INDENT = ' ' * 4

    prompt = colorize(Colors.LIME, '$ fm ')
    intro = render("""
                 _   ___
     ___ _____ _| | |  _|_____
    |  _|     | . |_|  _|     |
    |___|_|_|_|___|_|_| |_|_|_|
    ---------------------------------------------------------------
    {{y}}Welcome to cmd.fm! Use{{e}} play {{y}}command to begin listening.
    For example:{{e}} play chillout{{y}}, {{e}}play dubstep {{y}}etc...
    {{g}}You can use{{e}} help {{g}}command to see all cmd.fm commands.{{e}}
    """)

    @classmethod
    def _bind_handler(cls, command: type[Command]) -> None:
        def fn(self: Fm, *args: str) -> None:
            self.stdout_print(command.handle(self, *args))

        setattr(cls, f'do_{command.name}', fn)

    @classmethod
    def _bind_help(cls, command: type[Command]) -> None:
        def fn(self: Fm, *args: str) -> None:
            self.stdout_print(command.help())

        setattr(cls, f'help_{command.name}', fn)

    def __init__(
        self,
        client: DirbleClient | None = None,
        test: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        for command in commands:
            Fm._bind_handler(command)
            Fm._bind_help(command)

        self.client = client
        self.player = None
        cmd.Cmd.__init__(self, *args, **kwargs)
        self.commands = commands
        if not test:
            self.intro = self.onecmd('genres withintro')

    def stdout_print(self, text: str, end: str = '\n') -> None:
        self.stdout.write(text + end)

    def default(self, arg: str) -> None:
        self.stdout_print(self.INDENT + colorize(Colors.RED, 'Unknown command ') + arg)

    def emptyline(self) -> None:
        pass


def main() -> None:
    os.environ['VLC_VERBOSE'] = '-1'
    api_key = os.environ.get('DIRBLE_API_KEY')

    if api_key:
        client = DirbleClient(api_key)
        Fm(client=client).cmdloop()
    else:
        print(render('{{r}}Please, specify your{{e}} DIRBLE_API_KEY {{r}}in environment variables.{{e}}'))
