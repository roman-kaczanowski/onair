from typing import Any

from onair.client.client import RadioBrowserClient, Station


class MockClient(RadioBrowserClient):
    def __init__(self) -> None:
        super().__init__(servers=[])

    def get_genres(self) -> list[dict[str, Any]]:
        return [
            {'id': 'trance', 'title': 'trance'},
            {'id': 'rock', 'title': 'rock'},
            {'id': 'dance', 'title': 'dance'},
            {'id': 'dancehall', 'title': 'dancehall'},
        ]

    def search_stations(
        self,
        *,
        tag: str | None = None,
        language: str | None = None,
        countrycode: str | None = None,
    ) -> list[Station]:
        return [
            Station(uuid='rock-1', name='Rock FM', url='http://example.test/rock-1', tags='rock'),
            Station(uuid='rock-2', name='Rock Live', url='http://example.test/rock-2', tags='rock'),
        ]

    def resolve_url(self, station: Station) -> str:
        return station.url

    def get_countries(self) -> list[dict[str, Any]]:
        return [
            {'name': 'Poland', 'iso_3166_1': 'PL', 'stationcount': 50},
            {'name': 'Germany', 'iso_3166_1': 'DE', 'stationcount': 80},
            {'name': 'Portugal', 'iso_3166_1': 'PT', 'stationcount': 20},
        ]
