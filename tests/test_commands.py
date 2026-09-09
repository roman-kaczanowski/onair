import re
import sys
from unittest import mock

import pytest
from mock_client import MockClient

from onair.app import App
from onair.client.client import Station
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
    assert _cli_response(mock_stdout) == '    Unknown command wrong_command\n'


def test_genres() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('genres')
    cli_response = _cli_response(mock_stdout)
    assert '- GENRES -' in cli_response
    assert 'R - rock' in cli_response
    assert 'play {genre}' in cli_response


def test_quit() -> None:
    cli, _mock_stdout = _create()
    with pytest.raises(SystemExit):
        cli.onecmd('quit')
    with pytest.raises(SystemExit):
        cli.onecmd('q')


def test_info_without_station() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('info')
    assert 'No active station' in _cli_response(mock_stdout)


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
    assert 'MP3 128kbps' in text
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
    assert f'\u25b6 {first.name}' in _cli_output(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('next')
    second = cli.client.active_station
    assert second is not None
    assert second.uuid != first.uuid
    assert f'\u25b6 {second.name}' in _cli_output(mock_stdout)

    mock_stdout.reset_mock()
    assert not cli.onecmd('previous')
    assert cli.client.active_station is not None
    assert cli.client.active_station.uuid == first.uuid
    assert f'\u25b6 {first.name}' in _cli_output(mock_stdout)


def test_next_without_station() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('next')
    assert 'play {genre}' in _cli_response(mock_stdout)


def test_previous_without_history() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('previous')
    assert 'No previous station' in _cli_response(mock_stdout)


def test_stop_without_player() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('stop')
    assert 'No active players' in _cli_response(mock_stdout)


def test_stop_playback() -> None:
    cli, mock_stdout = _create()
    player = mock.Mock()
    cli.player = player
    assert not cli.onecmd('stop')
    player.stop.assert_called_once()
    assert cli.player is None
    assert 'Stopped' in _cli_response(mock_stdout)


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
