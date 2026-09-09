import cmd
import os
from typing import Any

from onair.client.client import RadioBrowserClient
from onair.commands import commands
from onair.commands.base import Command
from onair.utils.colorize import Colors, colorize, render


class App(cmd.Cmd):
    INDENT = ' ' * 4

    prompt = colorize(Colors.LIME, 'onair> ')
    intro = render("""
      ___  _ __   __ _(_)_ __
     / _ \\| '_ \\ / _` | | '__|
    | (_) | | | | (_| | | |
     \\___/|_| |_|\\__,_|_|_|
    ---------------------------------------------------------------
    {{y}}Welcome to onair. Use{{e}} play {{y}}to begin listening.
    For example:{{e}} play chillout{{y}}, {{e}}play dubstep {{y}}etc...
    {{g}}Use{{e}} help {{g}}to see all commands.{{e}}
    """)

    @classmethod
    def _bind_handler(cls, command: type[Command]) -> None:
        def fn(self: App, *args: str) -> None:
            self.stdout_print(command.handle(self, *args))

        setattr(cls, f'do_{command.name}', fn)

    @classmethod
    def _bind_help(cls, command: type[Command]) -> None:
        def fn(self: App, *args: str) -> None:
            self.stdout_print(command.help())

        setattr(cls, f'help_{command.name}', fn)

    def __init__(
        self,
        client: RadioBrowserClient | None = None,
        test: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        for command in commands:
            App._bind_handler(command)
            App._bind_help(command)

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
    App(client=RadioBrowserClient()).cmdloop()
