import sys
from types import SimpleNamespace
from unittest import mock

from onair.player.player import Player


def _player() -> tuple[Player, mock.Mock]:
    backend = mock.Mock()
    backend.audio_get_volume.return_value = 50
    vlc = SimpleNamespace(
        MediaPlayer=mock.Mock(return_value=backend),
        State=SimpleNamespace(Playing='playing', Paused='paused', Stopped='stopped'),
    )
    with mock.patch.dict(sys.modules, {'vlc': vlc}):
        player = Player('http://example.test/stream')
    backend.audio_set_volume.reset_mock()
    return player, backend


def test_mute_and_unmute_restore_volume() -> None:
    player, backend = _player()

    player.mute()
    player.mute()
    player.unmute()

    backend.audio_get_volume.assert_called_once()
    assert backend.audio_set_volume.call_args_list == [mock.call(0), mock.call(0), mock.call(50)]


def test_volume_change_clears_mute_state() -> None:
    player, backend = _player()

    player.unmute()
    player.mute()
    player.set_volume(30)
    player.unmute()

    assert backend.audio_set_volume.call_args_list == [mock.call(0), mock.call(30)]
