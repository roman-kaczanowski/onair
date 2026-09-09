import re
import sys
from unittest import mock

import pytest
from mock_client import MockClient

from onair.app import App
from onair.client.client import Station
from onair.commands import commands
from onair.commands.play import start_stream
from onair.commands.volume import parse_volume


def _create() -> tuple[App, mock.MagicMock]:
    mock_stdout = mock.create_autospec(sys.stdout)
    cli = App(stdin=mock.create_autospec(sys.stdin), stdout=mock_stdout, client=MockClient(), test=True)
    return cli, mock_stdout


def _clear_coloring(text: str) -> str:
    return re.sub(r'\033\[[0-9]{1,2}m', '', text)


def _cli_response(mock_stdout: mock.MagicMock) -> str:
    return _clear_coloring(mock_stdout.write.call_args_list[0][0][0])


def _cli_output(mock_stdout: mock.MagicMock) -> str:
    return _clear_coloring(''.join(call[0][0] for call in mock_stdout.write.call_args_list))


def test_wrong_command() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('wrong_command')
    assert _cli_response(mock_stdout) == '    Unknown command: wrong_command\n'


def test_genres() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('genres')
    cli_response = _cli_response(mock_stdout)
    assert '- GENRES -' in cli_response
    assert 'R - rock' in cli_response
    assert 'play {genre}' in cli_response


def test_genres_filter() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('genres dance')
    text = _cli_response(mock_stdout)
    assert 'dance' in text
    assert 'dancehall' in text
    assert 'rock' not in text
    assert 'trance' not in text
    mock_stdout.reset_mock()
    assert not cli.onecmd('genres hip')
    assert 'No genres matching hip' in _cli_response(mock_stdout)


def test_genres_withintro_previews_each_group() -> None:
    from onair.utils.listing import PREVIEW_LIMIT, format_grouped_titles

    names = [f'rock{i}' for i in range(8)]
    preview = _clear_coloring(format_grouped_titles({'R': names}, '    ', limit=PREVIEW_LIMIT))
    full = _clear_coloring(format_grouped_titles({'R': names}, '    '))
    assert 'rock0, rock1, rock2, rock3, rock4' in preview
    assert 'rock5' not in preview
    assert '...' in preview
    assert 'rock5' in full

    cli, mock_stdout = _create()
    assert not cli.onecmd('genres withintro')
    text = _cli_output(mock_stdout)
    assert 'R - rock' in text
    assert 'D - dance' in text
    assert 'Run genres to see more' in text
    assert '\033[91m' in ''.join(call[0][0] for call in mock_stdout.write.call_args_list)


def test_home_screen_fits_default_terminal() -> None:
    import string

    from onair.client.client import RadioBrowserClient
    from onair.utils.listing import DEFAULT_TERMINAL_ROWS

    client = RadioBrowserClient(servers=[])
    client.genres = [
        {'id': f'{letter}{index}', 'title': f'{letter.lower()}{index}', 'stationcount': 50}
        for letter in string.ascii_uppercase
        for index in range(6)
    ]
    mock_stdout = mock.create_autospec(sys.stdout)
    cli = App(stdin=mock.create_autospec(sys.stdin), stdout=mock_stdout, client=client, test=True)
    cli.onecmd('genres withintro')
    assert len(_cli_output(mock_stdout).splitlines()) < DEFAULT_TERMINAL_ROWS


def test_quit() -> None:
    cli, _mock_stdout = _create()
    with pytest.raises(SystemExit):
        cli.onecmd('quit')
    with pytest.raises(SystemExit):
        cli.onecmd('q')
    with pytest.raises(SystemExit):
        cli.onecmd('exit')
    with pytest.raises(SystemExit):
        cli.onecmd('e')


def test_info_without_station() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('info')
    assert 'No station is tuned' in _cli_response(mock_stdout)


def test_info_with_station() -> None:
    cli, mock_stdout = _create()
    cli.client.active_station = Station(
        uuid='1',
        name='Jazz FM',
        url='http://example.test/jazz',
        tags='jazz',
        country='Germany',
        countrycode='DE',
        state='Berlin',
        language='german',
        codec='MP3',
        bitrate=128,
        homepage='https://jazz.fm',
    )
    assert not cli.onecmd('info')
    text = _cli_response(mock_stdout)
    assert 'Jazz FM' in text
    assert 'jazz' in text
    assert 'Berlin, Germany' in text
    assert 'german' in text
    assert 'MP3 128 kbps' in text
    assert 'https://jazz.fm' in text


def test_play_unknown_genre() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('play nosuchgenre')
    assert 'not found' in _cli_response(mock_stdout)


@mock.patch('onair.commands.play.Player')
def test_play_next_and_previous(mock_player_cls: mock.MagicMock) -> None:
    mock_player_cls.return_value.is_playing = True
    mock_player_cls.return_value.is_paused = False
    cli, mock_stdout = _create()

    assert not cli.onecmd('play rock')
    first = cli.client.active_station
    assert first is not None
    output = _cli_output(mock_stdout)
    assert f'Now playing: {first.name}' in output
    assert 'Genre: rock' in output
    assert 'Volume: 50' in output
    mock_player_cls.return_value.set_volume.assert_called_with(50)

    mock_stdout.reset_mock()
    assert not cli.onecmd('next')
    second = cli.client.active_station
    assert second is not None
    assert second.uuid != first.uuid
    assert f'Now playing: {second.name}' in _cli_output(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('previous')
    assert cli.client.active_station is not None
    assert cli.client.active_station.uuid == first.uuid
    assert f'Now playing: {first.name}' in _cli_output(mock_stdout)


def test_next_without_station() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('next')
    assert 'play {genre}' in _cli_response(mock_stdout)


def test_previous_without_history() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('previous')
    assert 'No previous station' in _cli_response(mock_stdout)


def test_countries() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('countries')
    text = _cli_response(mock_stdout)
    assert '- COUNTRIES -' in text
    assert 'Poland (PL)' in text
    assert 'country {name}' in text


def test_countries_filter() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('countries pol')
    text = _cli_response(mock_stdout)
    assert 'Poland (PL)' in text
    assert 'Germany' not in text
    assert 'Portugal' not in text
    mock_stdout.reset_mock()
    assert not cli.onecmd('countries narnia')
    assert 'No countries matching narnia' in _cli_response(mock_stdout)


def test_country_unknown() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('country narnia')
    assert 'not found' in _cli_response(mock_stdout)


@mock.patch('onair.commands.play.Player')
def test_country_play(mock_player_cls: mock.MagicMock) -> None:
    mock_player_cls.return_value.is_playing = True
    cli, mock_stdout = _create()
    assert not cli.onecmd('country PL')
    assert cli.client.current_countrycode == 'PL'
    assert 'Country: Poland' in _cli_output(mock_stdout)
    assert 'Volume: 50' in _cli_output(mock_stdout)
    mock_stdout.reset_mock()
    assert not cli.onecmd('c poland')
    assert cli.client.current_countrycode == 'PL'
    assert 'Country: Poland' in _cli_output(mock_stdout)
    assert 'Now playing:' in _cli_output(mock_stdout)


def test_stop_without_player() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('stop')
    assert 'Nothing is playing' in _cli_response(mock_stdout)


def test_stop_playback() -> None:
    cli, mock_stdout = _create()
    player = mock.Mock()
    cli.player = player
    assert not cli.onecmd('stop')
    player.stop.assert_called_once()
    assert cli.player is None
    assert 'Stopped' in _cli_response(mock_stdout)


def test_playback_controls() -> None:
    cli, mock_stdout = _create()
    player = mock.Mock()
    cli.player = player

    player.is_playing = True
    assert not cli.onecmd('pause')
    player.pause.assert_called_once()
    assert 'Playback paused' in _cli_response(mock_stdout)

    mock_stdout.reset_mock()
    player.is_playing = False
    player.is_paused = True
    assert not cli.onecmd('resume')
    player.play.assert_called_once()
    assert 'Now playing:' in _cli_response(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('mute')
    player.mute.assert_called_once()
    assert 'Muted' in _cli_response(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('unmute')
    player.unmute.assert_called_once()
    assert 'Unmuted' in _cli_response(mock_stdout)


def test_start_stream_cleans_up_failed_player() -> None:
    cli, _mock_stdout = _create()
    with (
        mock.patch('onair.commands.play.Player') as player_cls,
        mock.patch('onair.commands.play.time.sleep') as sleep,
    ):
        player_cls.return_value.is_playing = False
        assert not start_stream(cli, 'http://example.test/broken')

    player_cls.return_value.stop.assert_called_once()
    assert sleep.call_count == 5
    assert cli.player is None


def test_start_stream_cleans_up_when_interrupted() -> None:
    cli, _mock_stdout = _create()
    with (
        mock.patch('onair.commands.play.Player') as player_cls,
        mock.patch('onair.commands.play.time.sleep', side_effect=KeyboardInterrupt),
        pytest.raises(KeyboardInterrupt),
    ):
        player_cls.return_value.is_playing = False
        start_stream(cli, 'http://example.test/slow')

    player_cls.return_value.stop.assert_called_once()
    assert cli.player is None


def test_volume_relative() -> None:
    cli, mock_stdout = _create()
    cli.player = mock.Mock()
    cli.player.get_volume.return_value = 40
    assert not cli.onecmd('volume +10')
    cli.player.set_volume.assert_called_once_with(50)
    assert 'Set volume to 50' in _cli_response(mock_stdout)


def test_parse_volume() -> None:
    assert parse_volume(40, '45') == 45
    assert parse_volume(40, '+10') == 50
    assert parse_volume(40, '-15') == 25
    assert parse_volume(95, '+10') == 100
    assert parse_volume(5, '-10') == 0
    assert parse_volume(40, 'nope') is None


def test_help_and_command_registry() -> None:
    cli, mock_stdout = _create()
    names = [command.name for command in commands]
    assert len(names) == len(set(names))

    assert not cli.onecmd('help')
    lines = [line for line in _cli_response(mock_stdout).splitlines() if line]
    assert len({line.index(' - ') for line in lines}) == 1

    mock_stdout.reset_mock()
    assert not cli.onecmd('help play')
    assert 'Play a genre' in _cli_response(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('help unknown')
    assert 'Command "unknown" not found' in _cli_response(mock_stdout)


def test_genres_without_client() -> None:
    mock_stdout = mock.create_autospec(sys.stdout)
    cli = App(stdout=mock_stdout, client=None, test=True)
    assert not cli.onecmd('genres')
    assert 'Radio Browser API may be unavailable' in _cli_response(mock_stdout)


def test_complete_commands_and_genres() -> None:
    from prompt_toolkit.completion import CompleteEvent
    from prompt_toolkit.document import Document

    from onair.app import OnairCompleter

    cli, _mock_stdout = _create()
    completer = OnairCompleter(cli)

    def texts(line: str) -> list[str]:
        return [item.text for item in completer.get_completions(Document(line, len(line)), CompleteEvent())]

    assert 'play' in texts('pl')
    assert 'rock' in texts('play ro')
    assert 'help' in texts('he')
    assert 'play' in texts('help p')
    assert 'Poland' in texts('country P')
    assert 'Poland' in texts('c P')
    assert 'countries' in texts('co')
    assert 'dance' in texts('genres da')
    assert 'Poland' in texts('countries P')
