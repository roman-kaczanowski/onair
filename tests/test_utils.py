from onair.player.visualizer import Meter, render_histogram
from onair.utils.colorize import Colors, colorize, render
from onair.utils.listing import filter_grouped_titles


def test_colorize() -> None:
    assert colorize(Colors.YELLOW, 'test') == '\033[93mtest\033[0m'
    assert colorize(Colors.GRAY, 'test') == '\033[90mtest\033[0m'
    assert colorize(Colors.PURPLE, 'test') == '\033[95mtest\033[0m'
    assert colorize(Colors.RED, 'test') == '\033[91mtest\033[0m'


def test_render() -> None:
    assert render('test {{r}}test{{e}} test') == 'test \033[91mtest\033[0m test'
    assert render('{{y}}test {{e-r}}test{{e}} test') == '\033[93mtest \033[0m\033[91mtest\033[0m test'
    assert render('{{g}}test{{e}} {{r}}test{{e}} test') == '\033[90mtest\033[0m \033[91mtest\033[0m test'


def test_render_histogram() -> None:
    text = render_histogram([0.0, 0.5, 1.0], indent='    ')
    lines = text.split('\n')
    assert len(lines) == 2
    assert all(line.startswith('    ') for line in lines)
    assert '#' in lines[1]
    assert lines[0].rstrip() == '      #'


def test_meter_idle_decays() -> None:
    meter = Meter()
    meter.levels = [1.0] * 4
    idle = meter.tick(False)
    assert all(level < 1.0 for level in idle)


def test_filter_grouped_titles() -> None:
    titles = {'D': ['dance', 'dancehall'], 'R': ['rock']}
    assert filter_grouped_titles(titles, 'dance') == {'D': ['dance', 'dancehall']}
    assert filter_grouped_titles(titles, 'HIP') == {}
    assert filter_grouped_titles(titles, '') == titles
