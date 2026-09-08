from cmd_fm_python.utils.colorize import Colors, colorize, render


def test_colorize() -> None:
    assert colorize(Colors.YELLOW, 'test') == '\033[93mtest\033[0m'
    assert colorize(Colors.GRAY, 'test') == '\033[90mtest\033[0m'
    assert colorize(Colors.PURPLE, 'test') == '\033[95mtest\033[0m'
    assert colorize(Colors.RED, 'test') == '\033[91mtest\033[0m'


def test_render() -> None:
    assert render('test {{r}}test{{e}} test') == 'test \033[91mtest\033[0m test'
    assert render('{{y}}test {{e-r}}test{{e}} test') == '\033[93mtest \033[0m\033[91mtest\033[0m test'
    assert render('{{g}}test{{e}} {{r}}test{{e}} test') == '\033[90mtest\033[0m \033[91mtest\033[0m test'
