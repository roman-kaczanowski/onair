import os
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory

from onair.client.client import RadioBrowserClient
from onair.commands import commands
from onair.commands.base import Command
from onair.player.player import DEFAULT_VOLUME
from onair.utils.colorize import Colors, colorize, render

HISTORY_PATH = Path.home() / '.onair_history'


class OnairCompleter(Completer):
    def __init__(self, app: 'App') -> None:
        self._app = app

    def get_completions(self, document: Document, complete_event: Any) -> Iterator[Completion]:
        names = [command.name for command in self._app.commands]
        stripped = document.text_before_cursor.lstrip()
        if not stripped or (' ' not in stripped and not document.text_before_cursor.endswith(' ')):
            for name in names:
                if name.startswith(stripped):
                    yield Completion(name, start_position=-len(stripped))
            return
        command, _, rest = stripped.partition(' ')
        if command in {'play', 'p', 'genres'}:
            options = [genre.get('title', '') for genre in (self._app.client.genres if self._app.client else [])]
        elif command in {'country', 'c', 'countries'}:
            options = []
            for country in self._app.client.countries if self._app.client else []:
                options.append(country.get('name', ''))
                iso = country.get('iso', '')
                if iso:
                    options.append(iso)
        elif command == 'help':
            options = names
        else:
            return
        needle = rest.lower()
        for option in options:
            if option.lower().startswith(needle):
                yield Completion(option, start_position=-len(rest))


class App:
    INDENT = ' ' * 4

    prompt = colorize(Colors.LIME, 'onair> ')
    intro = render("""
      ___  _ __   {{r}}__ _(_)_ __{{e}}
     / _ \\| '_ \\ {{r}}/ _` | | '__|{{e}}
    | (_) | | | | {{r}}(_| | | |{{e}}
     \\___/|_| |_|{{r}}\\__,_|_|_|{{e}}
    ---------------------------------------------------------------
    {{y}}Welcome to onair. Use{{e}} play {{y}}to begin listening.
    For example:{{e}} play chillout{{y}}, {{e}}play dubstep {{y}}etc...
    {{g}}Use{{e}} help {{g}}to see all commands.{{e}}
""").strip('\n')

    def __init__(
        self,
        client: RadioBrowserClient | None = None,
        test: bool = False,
        stdout: Any = None,
        stdin: Any = None,
    ) -> None:
        self.client = client
        self.player = None
        self.volume = DEFAULT_VOLUME
        self.commands = commands
        self._commands_by_name = {command.name: command for command in commands}
        self.stdout = stdout or sys.stdout
        self.stdin = stdin
        if not test:
            self.onecmd('genres withintro')

    def stdout_print(self, text: str, end: str = '\n') -> None:
        self.stdout.write(text + end)

    def onecmd(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return False
        name, *args = line.split()
        command: type[Command] | None = self._commands_by_name.get(name)
        if command is None:
            self.stdout_print(self.INDENT + colorize(Colors.RED, 'Unknown command ') + line)
            return False
        self.stdout_print(command.handle(self, *args))
        return False

    def cmdloop(self) -> None:
        session: PromptSession[str] = PromptSession(
            history=FileHistory(str(HISTORY_PATH)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=OnairCompleter(self),
        )
        while True:
            try:
                line = session.prompt(ANSI(self.prompt))
            except KeyboardInterrupt:
                continue
            except EOFError:
                if self.player:
                    self.player.stop()
                break
            self.onecmd(line)


def main() -> None:
    os.environ['VLC_VERBOSE'] = '-1'
    App(client=RadioBrowserClient()).cmdloop()
