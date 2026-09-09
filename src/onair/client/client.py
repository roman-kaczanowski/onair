import socket
import string
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from random import shuffle
from typing import Any

import requests

try:
    USER_AGENT = f'onair/{version("onair")}'
except PackageNotFoundError:
    USER_AGENT = 'onair/0.1.0'

DNS_NAME = 'all.api.radio-browser.info'
MIN_TAG_STATIONS = 30
REQUEST_TIMEOUT = 10
STATION_LIMIT = '100'
# ponytail: hardcoded hosts if DNS is filtered; drop once discovery is enough.
FALLBACK_HOSTS = (
    'de1.api.radio-browser.info',
    'nl1.api.radio-browser.info',
    'at1.api.radio-browser.info',
)


@dataclass
class Station:
    uuid: str
    name: str
    url: str
    tags: str = ''
    country: str = ''
    countrycode: str = ''
    state: str = ''
    language: str = ''
    codec: str = ''
    bitrate: int = 0
    homepage: str = ''


def discover_servers() -> list[str]:
    hosts: list[str] = []
    try:
        for info in socket.getaddrinfo(DNS_NAME, 443, proto=socket.IPPROTO_TCP):
            ip = info[4][0]
            try:
                host = socket.gethostbyaddr(ip)[0].rstrip('.')
            except socket.herror:
                continue
            if host and host not in hosts:
                hosts.append(host)
    except OSError:
        pass
    if not hosts:
        hosts = list(FALLBACK_HOSTS)
    shuffle(hosts)
    return [f'https://{host}' for host in hosts]


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class RadioBrowserClient:
    def __init__(self, servers: list[str] | None = None) -> None:
        self._servers = list(servers) if servers is not None else discover_servers()
        self.genres: list[dict[str, str]] = self.get_genres()
        self.current_tag: str | None = None
        self.current_stations: list[Station] = []
        self.active_station: Station | None = None
        self.history: list[Station] = []
        self._history_index: int = -1
        self._cursor: int = 0

    def _headers(self) -> dict[str, str]:
        return {'User-Agent': USER_AGENT, 'Accept': 'application/json'}

    def _get(self, path: str, params: dict[str, str] | None = None) -> Any:
        for base in self._servers:
            try:
                response = requests.get(
                    f'{base}{path}',
                    params=params,
                    headers=self._headers(),
                    timeout=REQUEST_TIMEOUT,
                )
                if response.ok:
                    return response.json()
            except (requests.RequestException, ValueError):
                continue
        return None

    def get_genres(self) -> list[dict[str, str]]:
        data = self._get(
            '/json/tags',
            {'hidebroken': 'true', 'order': 'stationcount', 'reverse': 'true'},
        )
        if not isinstance(data, list):
            return []
        genres: list[dict[str, str]] = []
        for tag in data:
            name = str(tag.get('name') or '').strip()
            if name and _int(tag.get('stationcount')) >= MIN_TAG_STATIONS:
                genres.append({'id': name, 'title': name})
        return genres

    def get_languages(self) -> list[dict[str, Any]]:
        data = self._get(
            '/json/languages',
            {'hidebroken': 'true', 'order': 'stationcount', 'reverse': 'true'},
        )
        return data if isinstance(data, list) else []

    def get_countries(self) -> list[dict[str, Any]]:
        data = self._get(
            '/json/countries',
            {'hidebroken': 'true', 'order': 'stationcount', 'reverse': 'true'},
        )
        return data if isinstance(data, list) else []

    @property
    def genres_titles(self) -> dict[str, list[str]]:
        titles: dict[str, list[str]] = {}
        for title in sorted(g.get('title', '') for g in self.genres):
            if not title:
                continue
            first_letter = '#' if title[0] in string.digits else title[0].upper()
            titles[first_letter] = titles.get(first_letter, list()) + [title]
        return titles

    def search_genre(self, genre_name: str) -> dict[str, str] | None:
        needle = genre_name.lower()
        for genre in sorted(self.genres, key=lambda item: (len(item.get('title', '')), item.get('title', ''))):
            if needle in genre.get('title', '').lower():
                return genre
        return None

    def search_stations(
        self,
        *,
        tag: str | None = None,
        language: str | None = None,
        countrycode: str | None = None,
    ) -> list[Station]:
        params: dict[str, str] = {
            'hidebroken': 'true',
            'order': 'votes',
            'reverse': 'true',
            'limit': STATION_LIMIT,
        }
        if tag:
            params['tag'] = tag
            params['tagExact'] = 'true'
        if language:
            params['language'] = language
        if countrycode:
            params['countrycode'] = countrycode
        data = self._get('/json/stations/search', params)
        if not isinstance(data, list):
            return []
        stations: list[Station] = []
        for row in data:
            station = self._station(row)
            if station is not None:
                stations.append(station)
        return stations

    def get_stations(self) -> list[Station]:
        if not self.current_tag:
            return []
        return self.search_stations(tag=self.current_tag)

    def resolve_url(self, station: Station) -> str:
        data = self._get(f'/json/url/{station.uuid}')
        if isinstance(data, dict) and data.get('url'):
            station.url = str(data['url'])
        return station.url

    def update_active_station(self, tag: str) -> Station | None:
        if self.current_tag != tag:
            self.current_tag = tag
            self.current_stations = self.get_stations()
            shuffle(self.current_stations)
            self._cursor = 0
        if not self.current_stations:
            self.active_station = None
            return None
        skip = self.active_station.uuid if self.active_station else None
        count = len(self.current_stations)
        for _ in range(count):
            station = self.current_stations[self._cursor % count]
            self._cursor += 1
            if skip and station.uuid == skip:
                continue
            if self._activate(station):
                return self.active_station
        return None

    @property
    def stream_url(self) -> str:
        return self.active_station.url if self.active_station else ''

    def get_stream(self, tag: str, renew_active_station: bool = False) -> str:
        if not self.active_station or self.current_tag != tag or renew_active_station:
            return self.stream_url if self.update_active_station(tag) else ''
        return self.stream_url

    def next_station(self) -> str:
        if 0 <= self._history_index < len(self.history) - 1:
            self._history_index += 1
            return self._activate(self.history[self._history_index], record_history=False)
        if not self.current_tag:
            return ''
        return self.get_stream(self.current_tag, renew_active_station=True)

    def previous_station(self) -> str:
        if self._history_index <= 0:
            return ''
        self._history_index -= 1
        return self._activate(self.history[self._history_index], record_history=False)

    def _activate(self, station: Station, *, record_history: bool = True) -> str:
        url = self.resolve_url(station)
        if not url:
            return ''
        self.active_station = station
        if record_history:
            self.history = self.history[: self._history_index + 1]
            if not self.history or self.history[-1].uuid != station.uuid:
                self.history.append(station)
            self._history_index = len(self.history) - 1
        return url

    def _station(self, row: dict[str, Any]) -> Station | None:
        uuid = str(row.get('stationuuid') or '').strip()
        url = str(row.get('url_resolved') or row.get('url') or '').strip()
        if not uuid:
            return None
        return Station(
            uuid=uuid,
            name=str(row.get('name') or '').strip() or uuid,
            url=url,
            tags=str(row.get('tags') or ''),
            country=str(row.get('country') or ''),
            countrycode=str(row.get('countrycode') or ''),
            state=str(row.get('state') or ''),
            language=str(row.get('language') or ''),
            codec=str(row.get('codec') or ''),
            bitrate=_int(row.get('bitrate')),
            homepage=str(row.get('homepage') or ''),
        )
