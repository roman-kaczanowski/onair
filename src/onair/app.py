import argparse
import os
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory

from onair import __version__
from onair.client.client import RadioBrowserClient
from onair.commands import commands
from onair.commands.base import Command, CommandError
from onair.commands.genres import home_preview
from onair.player.player import DEFAULT_VOLUME
from onair.utils.colorize import Colors, colorize, render

HISTORY_PATH = Path.home() / '.onair_history'


class StoreOrdered(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        items = list(getattr(namespace, self.dest) or [])
        command = (option_string or self.dest).lstrip('-')
        items.append(f'{command} {values}')
        setattr(namespace, self.dest, items)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='onair', description='Interactive internet radio for the terminal.')
    parser.add_argument('-V', '--version', action='version', version=f'onair {__version__}')
    parser.set_defaults(startup=[])
    parser.add_argument('-p', '--play', dest='startup', metavar='GENRE', action=StoreOrdered, help='Play a genre')
    parser.add_argument(
        '-c', '--country', dest='startup', metavar='COUNTRY', action=StoreOrdered, help='Play a station from a country'
    )
    parser.add_argument(
        '-l',
        '--language',
        dest='startup',
        metavar='LANGUAGE',
        action=StoreOrdered,
        help='Play a station in a language',
    )
    parser.add_argument(
        '-v',
        '--volume',
        dest='startup',
        metavar='LEVEL',
        action=StoreOrdered,
        help='Set volume',
    )
    args = parser.parse_args(argv)
    if args.startup:
        volume = [line for line in args.startup if line.split(maxsplit=1)[0] in {'volume', 'v'}]
        playback = [line for line in args.startup if line not in volume]
        if not playback:
            playback.append('play')
        args.startup = volume + playback
    return args


class OnairCompleter(Completer):
    def __init__(self, app: 'App') -> None:
        self._app = app

    def get_completions(self, document: Document, complete_event: Any) -> Iterator[Completion]:
        names = [command.name for command in self._app.commands]
        segment = document.text_before_cursor.rsplit('|', 1)[-1]
        stripped = segment.lstrip()
        if not stripped or (' ' not in stripped and not segment.endswith(' ')):
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
        elif command in {'language', 'l', 'lang', 'languages'}:
            options = []
            for language in self._app.client.languages if self._app.client else []:
                options.append(language.get('name', ''))
                iso = language.get('iso', '')
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
    banner = render("""
      ___  _ __   {{r}}__ _(_)_ __{{e}}
     / _ \\| '_ \\ {{r}}/ _` | | '__|{{e}}
    | (_) | | | | {{r}}(_| | | |{{e}}
     \\___/|_| |_|{{r}}\\__,_|_|_|{{e}}
""").strip('\n')
    welcome = render("""
    ---------------------------------------------------------------
    {{y}}Welcome to onair. Play a genre to start listening.
    Try:{{e}} play chillout {{y}}or{{e}} play dubstep{{y}}.
    {{g}}Run{{e}} help {{g}}to list all commands.{{e}}
""").strip('\n')

    def __init__(
        self,
        client: RadioBrowserClient | None = None,
        test: bool = False,
        stdout: Any = None,
        stdin: Any = None,
        preview_genres: bool = True,
    ) -> None:
        self.client = client
        self.player = None
        self.volume = DEFAULT_VOLUME
        self.commands = commands
        self._commands_by_name = {command.name: command for command in commands}
        self.stdout = stdout or sys.stdout
        self.stdin = stdin
        if not test:
            self.show_startup(preview_genres=preview_genres)

    def stdout_print(self, text: str, end: str = '\n') -> None:
        self.stdout.write(text + end)

    def show_startup(self, *, preview_genres: bool = True) -> None:
        self.stdout_print(self.banner)
        self.stdout_print(self.welcome)
        if preview_genres:
            self.stdout_print(home_preview(self))
        self.stdout_print('')

    def run_line(self, line: str) -> bool:
        line = line.strip()
        if not line:
            return True
        name, *args = line.split()
        command: type[Command] | None = self._commands_by_name.get(name)
        if command is None:
            self.stdout_print(self.INDENT + colorize(Colors.RED, 'Unknown command: ') + line)
            return False
        try:
            self.stdout_print(command.handle(self, *args))
        except CommandError as exc:
            self.stdout_print(str(exc))
            return False
        return True

    def onecmd(self, line: str) -> bool:
        # Easter egg: `|` chaining is intentional and undocumented. Do not add it to README or help.
        line = line.strip()
        if not line:
            return False
        for segment in line.split('|'):
            segment = segment.strip()
            if not segment:
                continue
            if not self.run_line(segment):
                break
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
                self.onecmd(line)
            except KeyboardInterrupt:
                continue
            except EOFError:
                if self.player:
                    self.player.stop()
                break


def main() -> None:
    os.environ['VLC_VERBOSE'] = '-1'
    args = parse_args()
    app = App(client=RadioBrowserClient(), preview_genres=not args.startup)
    for line in args.startup:
        if not app.run_line(line):
            break
    app.cmdloop()
