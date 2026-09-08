from typing import Any


class Player:
    _volume_state_for_mute = 0

    def __init__(self, stream: str) -> None:
        import vlc

        self._vlc = vlc
        self._player = vlc.MediaPlayer(stream)

    def play(self) -> Any:
        return self._player.play()

    def pause(self) -> Any:
        return self._player.pause()

    def stop(self) -> Any:
        return self._player.stop()

    def get_volume(self) -> int:
        return self._player.audio_get_volume()

    def set_volume(self, value: int) -> int:
        return self._player.audio_set_volume(value)

    def mute(self) -> int:
        self._volume_state_for_mute = self.get_volume()
        return self.set_volume(0)

    def unmute(self) -> int:
        self.set_volume(self._volume_state_for_mute)
        self._volume_state_for_mute = 0
        return 0

    @property
    def state(self) -> Any:
        return self._player.get_state()

    @property
    def is_playing(self) -> bool:
        return self.state == self._vlc.State.Playing

    @property
    def is_paused(self) -> bool:
        return self.state == self._vlc.State.Paused

    @property
    def is_stopped(self) -> bool:
        return self.state == self._vlc.State.Stopped

    @property
    def is_broken(self) -> bool:
        return self.state == self._vlc.State.Error
