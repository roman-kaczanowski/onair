from typing import Any

DEFAULT_VOLUME = 50


class Player:
    def __init__(self, stream: str, volume: int = DEFAULT_VOLUME) -> None:
        import vlc

        self._vlc = vlc
        self._player = vlc.MediaPlayer(stream)
        self._volume_before_mute: int | None = None
        self.set_volume(volume)

    def play(self) -> Any:
        return self._player.play()

    def pause(self) -> Any:
        return self._player.pause()

    def stop(self) -> Any:
        return self._player.stop()

    def get_volume(self) -> int:
        return self._player.audio_get_volume()

    def set_volume(self, value: int) -> int:
        self._volume_before_mute = None
        return self._player.audio_set_volume(value)

    def mute(self) -> int:
        if self._volume_before_mute is None:
            current = self.get_volume()
            if current > 0:
                self._volume_before_mute = current
        return self._player.audio_set_volume(0)

    def unmute(self) -> int:
        if self._volume_before_mute is None:
            return 0
        volume = self._volume_before_mute
        self._volume_before_mute = None
        return self._player.audio_set_volume(volume)

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
