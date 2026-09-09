import re
import sys
from unittest import mock

import pytest
from mock_client import MockClient

from onair.app import App
from onair.client.client import Station


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
