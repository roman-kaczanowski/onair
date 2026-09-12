from typing import Any

from onair.utils.colorize import Colors, colorize


class CommandError(Exception):
    """User-facing command failure. The message is printed as-is."""


class Command:
    """REPL command bound onto the App shell."""

    name = ''
    pattern = ''
    example: tuple[str, ...] = ()
    description = ''
    show_in_main_help = True

    @staticmethod
    def handle(app: Any, *args: str) -> str:
        """Run the command. `app` is the App shell instance."""
        raise NotImplementedError

    @classmethod
    def help(cls) -> str:
        example_label = ' - Example: ' if len(cls.example) == 1 else ' - Examples: '
        examples = colorize(Colors.GRAY, ' | ').join(cls.example)
        return (
            f'    {cls.pattern}{colorize(Colors.GRAY, example_label)}{examples}\n'
            f'    {colorize(Colors.GREEN, cls.description)}'
        )

    @classmethod
    def one_line_help(cls) -> str:
        if not cls.show_in_main_help:
            return ''
        example_label = ' Example: ' if len(cls.example) == 1 else ' Examples: '
        return (
            f'    {cls.pattern:<20} - {colorize(Colors.GREEN, cls.description)}'
            f'{colorize(Colors.GRAY, example_label)}{colorize(Colors.GRAY, " | ").join(cls.example)}\n'
        )
