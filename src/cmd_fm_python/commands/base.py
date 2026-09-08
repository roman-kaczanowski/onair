from typing import Any

from cmd_fm_python.utils.colorize import Colors, colorize


class Command:
    """REPL command bound onto the Fm shell."""

    name = ''
    pattern = ''
    example: tuple[str, ...] = ()
    description = ''
    show_in_main_help = True

    @staticmethod
    def handle(fm: Any, *args: str) -> str:
        """Run the command. `fm` is the Fm shell instance."""
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
            f'    {cls.pattern:<15} - {colorize(Colors.GREEN, cls.description)}'
            f'{colorize(Colors.GRAY, example_label)}{colorize(Colors.GRAY, " | ").join(cls.example)}\n'
        )
