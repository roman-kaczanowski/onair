from typing import Any
from unittest.mock import MagicMock

from mock_client import MockClient

from onair.client.client import FALLBACK_HOSTS, RadioBrowserClient, Station, discover_servers


def test_get_genres() -> None:
    client = MockClient()
    assert bool(client.get_genres())
    assert isinstance(client.get_genres(), list)


def test_genres_titles() -> None:
    client = MockClient()
    assert client.genres_titles == {
        'T': ['trance'],
        'R': ['rock'],
        'D': ['dance', 'dancehall'],
    }


def test_search_genre() -> None:
    client = MockClient()
    assert client.search_genre('rock') == {'id': 'rock', 'title': 'rock'}
    assert client.search_genre('dancehall') == {'id': 'dancehall', 'title': 'dancehall'}
    assert client.search_genre('wrong_genre') is None
    assert client.search_genre('ock') == {'id': 'rock', 'title': 'rock'}
    assert client.search_genre('ance') == {'id': 'dance', 'title': 'dance'}


def test_get_genres_drops_rare_tags() -> None:
    client = RadioBrowserClient(servers=[])

    def fake_get(path: str, params: dict[str, str] | None = None) -> list[dict[str, Any]]:
        return [
            {'name': 'jazz', 'stationcount': 100},
            {'name': 'tiny', 'stationcount': 2},
            {'name': '  ', 'stationcount': 99},
            {'name': 'rock', 'stationcount': '30'},
        ]

    client._get = fake_get  # type: ignore[method-assign]
    assert {genre['id'] for genre in client.get_genres()} == {'jazz', 'rock'}


def test_search_stations_maps_rows() -> None:
    client = RadioBrowserClient(servers=[])

    def fake_get(path: str, params: dict[str, str] | None = None) -> list[dict[str, Any]]:
        return [
            {
                'stationuuid': 'abc',
                'name': 'Jazz FM',
                'url': 'http://old',
                'url_resolved': 'http://live',
                'tags': 'jazz',
                'country': 'Germany',
                'countrycode': 'DE',
                'state': 'Berlin',
                'language': 'german',
                'codec': 'MP3',
                'bitrate': '128',
                'homepage': 'https://jazz.fm',
            },
            {'name': 'no uuid'},
        ]

    client._get = fake_get  # type: ignore[method-assign]
    stations = client.search_stations(tag='jazz')
    assert len(stations) == 1
    assert stations[0] == Station(
        uuid='abc',
        name='Jazz FM',
        url='http://live',
        tags='jazz',
        country='Germany',
        countrycode='DE',
        state='Berlin',
        language='german',
        codec='MP3',
        bitrate=128,
        homepage='https://jazz.fm',
    )


def test_languages_and_countries() -> None:
    client = RadioBrowserClient(servers=[])
    payload = [{'name': 'english', 'iso_639': 'en', 'stationcount': 3}]
    client._get = MagicMock(return_value=payload)
    assert client.get_languages() == payload
    assert client.get_countries() == payload


def test_play_history_next_and_previous() -> None:
    client = MockClient()
    assert client.get_stream('rock', renew_active_station=True)
    first = client.active_station
    assert first is not None
    assert client.next_station()
    second = client.active_station
    assert second is not None
    assert second.uuid != first.uuid
    assert client.previous_station()
    assert client.active_station is not None
    assert client.active_station.uuid == first.uuid
    assert client.next_station()
    assert client.active_station is not None
    assert client.active_station.uuid == second.uuid
    assert client.previous_station() == first.url
    assert client.previous_station() == ''


def test_discover_servers_fallback(monkeypatch: Any) -> None:
    def fail(*args: Any, **kwargs: Any) -> list[Any]:
        raise OSError('dns down')

    monkeypatch.setattr('onair.client.client.socket.getaddrinfo', fail)
    assert sorted(discover_servers()) == sorted(f'https://{host}' for host in FALLBACK_HOSTS)
