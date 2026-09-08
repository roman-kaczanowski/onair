import re


class Colors:
    ENDC = 0

    LIME = 36
    GRAY = 90
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    PURPLE = 95
    LBLUE = 96
    BLACK = 97

    HMAP = {
        'e': ENDC,
        'l': LIME,
        'g': GRAY,
        'gn': GREEN,
        'r': RED,
        'y': YELLOW,
        'b': BLUE,
        'p': PURPLE,
        'lb': LBLUE,
        'bk': BLACK,
    }


def colorize(color: int, text: str) -> str:
    return f'\033[{color}m{text}\033[{Colors.ENDC}m'


def render(template: str) -> str:
    pattern = r'(?i)({{(e-)?[a-z]{1}}})'
    matches = [m[0].replace('{{', '').replace('}}', '') for m in re.findall(pattern, template)]
    rendered_text = template

    for match in matches:
        if 'e-' in match:
            color = Colors.HMAP.get(match.replace('e-', ''))
        else:
            color = Colors.HMAP.get(match)

        if color is not None:
            if 'e-' in match:
                rendered_color = f'\033[0m\033[{color}m'
            else:
                rendered_color = f'\033[{color}m'

            rendered_text = rendered_text.replace('{{' + match + '}}', rendered_color)
        else:
            raise ValueError('Unexpected tag: {{' + match + '}}')

    return rendered_text
