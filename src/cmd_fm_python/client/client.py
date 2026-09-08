import string
from contextlib import closing
from random import shuffle
from typing import Any

import requests


class DirbleClient:
    DOMAIN = 'http://api.dirble.com/v2'
    GENRES = '/categories/{}'
    STATIONS = '/category/{}/stations'

    genres: list[dict[str, Any]] | None = None
    current_category_id: Any = None
    current_stations: list[dict[str, Any]] | None = None
    active_station: dict[str, Any] | None = None

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.genres = self.get_genres()

    @property
    def _uri_token(self) -> str:
        return f'?token={self.api_key}'

    def build_request_uri(self, endpoint: str, arg: str | int = '') -> str:
        return self.DOMAIN + endpoint.format(arg) + self._uri_token

    def get_genres(self) -> list[dict[str, Any]]:
        response = requests.get(self.build_request_uri(self.GENRES))

        if response.ok:
            return response.json()
        return []

    @property
    def genres_titles(self) -> dict[str, list[str]]:
        titles: dict[str, list[str]] = {}

        for title in sorted([g.get('title', '') for g in self.genres or []]):
            first_letter = title[0].upper()
            if title[0] in string.digits:
                first_letter = '#'
            titles[first_letter] = titles.get(first_letter, list()) + [title]

        return titles

    def get_stations(self) -> list[dict[str, Any]]:
        response = requests.get(self.build_request_uri(self.STATIONS, self.current_category_id))

        if response.ok:
            return response.json()
        return []

    def search_genre(self, genre_name: str) -> dict[str, Any] | None:
        for genre in sorted(self.genres or [], key=lambda x: (len(x.get('title', '')), x.get('title', ''))):
            if genre_name.lower() in genre.get('title', '').lower():
                return genre
        return None

    def update_active_station(self, category_id: Any) -> dict[str, Any] | None:
        self.active_station = None
        self.current_category_id = category_id

        if not self.current_stations:
            self.current_stations = self.get_stations()

        if not self.current_stations:
            return None

        shuffle(self.current_stations)

        for station in self.current_stations:
            stream_url = station['streams'][0].get('stream', '') if len(station.get('streams', [])) else ''
            if not stream_url:
                continue

            try:
                with closing(requests.get(stream_url, stream=True)) as r:
                    if r.ok:
                        self.active_station = station
                        break
            except requests.exceptions.ConnectionError:
                continue

        return self.active_station

    @property
    def stream_url(self) -> str:
        if self.active_station and len(self.active_station.get('streams', [])):
            return self.active_station['streams'][0].get('stream', '')
        return ''

    def get_stream(self, category_id: Any, renew_active_station: bool = False) -> str:
        if not self.active_station or self.current_category_id != category_id or renew_active_station:
            return self.stream_url if self.update_active_station(category_id) else ''
        return self.stream_url
