import re
import sys
from unittest import mock

import pytest
from mock_client import MockClient

from cmd_fm_python.fm import Fm


def _create() -> tuple[Fm, mock.MagicMock]:
    mock_stdout = mock.create_autospec(sys.stdout)
    cli = Fm(stdin=mock.create_autospec(sys.stdin), stdout=mock_stdout, client=MockClient('test_key'), test=True)
    return cli, mock_stdout


def _clear_coloring(text: str) -> str:
    return re.sub(r'\033\[[0-9]{1,2}m', '', text)


def _cli_response(mock_stdout: mock.MagicMock) -> str:
    return _clear_coloring(mock_stdout.write.call_args_list[0][0][0])


def test_wrong_command() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('wrong_command')
    assert _cli_response(mock_stdout) == '    Unknown command wrong_command\n'


def test_genres() -> None:
    cli, mock_stdout = _create()
    assert not cli.onecmd('genres')
    cli_response = _cli_response(mock_stdout)
    assert '- GENRES -' in cli_response
    assert 'R - Rock' in cli_response
    assert 'play {genre}' in cli_response


def test_quit() -> None:
    cli, _mock_stdout = _create()
    with pytest.raises(SystemExit):
        cli.onecmd('quit')
    with pytest.raises(SystemExit):
        cli.onecmd('q')
