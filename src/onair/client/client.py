import socket
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from random import shuffle
from typing import Any

import requests

from onair.utils.listing import HOME_GROUP_KEYS, HOME_GROUP_LIMIT, group_by_letter, letter_key

try:
    USER_AGENT = f'onair/{version("onair")}'
except PackageNotFoundError:
    USER_AGENT = 'onair/0.1.0'

DNS_NAME = 'all.api.radio-browser.info'
MIN_TAG_STATIONS = 30
MIN_COUNTRY_STATIONS = 10
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
        self.genres: list[dict[str, Any]] = self.get_genres()
        self._countries: list[dict[str, Any]] | None = None
        self.current_tag: str | None = None
        self.current_countrycode: str | None = None
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

    def get_genres(self) -> list[dict[str, Any]]:
        data = self._get(
            '/json/tags',
            {'hidebroken': 'true', 'order': 'stationcount', 'reverse': 'true'},
        )
        if not isinstance(data, list):
            return []
        genres: list[dict[str, Any]] = []
        for tag in data:
            name = str(tag.get('name') or '').strip()
            count = _int(tag.get('stationcount'))
            if name and count >= MIN_TAG_STATIONS:
                genres.append({'id': name, 'title': name, 'stationcount': count})
        return genres

    def get_countries(self) -> list[dict[str, Any]]:
        data = self._get(
            '/json/countries',
            {'hidebroken': 'true', 'order': 'stationcount', 'reverse': 'true'},
        )
        return data if isinstance(data, list) else []

    @property
    def genres_titles(self) -> dict[str, list[str]]:
        return group_by_letter(g.get('title', '') for g in self.genres)

    @property
    def home_genres_titles(self) -> dict[str, list[str]]:
        grouped: dict[str, list[tuple[int, str]]] = {}
        for genre in self.genres:
            title = str(genre.get('title') or '')
            if not title:
                continue
            key = letter_key(title)
            if key not in HOME_GROUP_KEYS:
                continue
            grouped.setdefault(key, []).append((_int(genre.get('stationcount')), title))
        ranked = sorted(grouped.items(), key=lambda item: (-sum(count for count, _title in item[1]), item[0]))
        chosen = dict(ranked[:HOME_GROUP_LIMIT])
        return {
            key: [title for _count, title in sorted(items, key=lambda item: (-item[0], item[1]))]
            for key, items in sorted(chosen.items())
        }

    @property
    def countries(self) -> list[dict[str, Any]]:
        if self._countries is None:
            self._countries = []
            for row in self.get_countries():
                name = str(row.get('name') or '').strip()
                iso = str(row.get('iso_3166_1') or '').strip().upper()
                if name and _int(row.get('stationcount')) >= MIN_COUNTRY_STATIONS:
                    self._countries.append({'name': name, 'iso': iso, 'stationcount': _int(row.get('stationcount'))})
        return self._countries

    @property
    def countries_titles(self) -> dict[str, list[str]]:
        labels = [
            f'{country["name"]} ({country["iso"]})' if country.get('iso') else country['name']
            for country in self.countries
        ]
        return group_by_letter(labels)

    def search_genre(self, genre_name: str) -> dict[str, Any] | None:
        needle = genre_name.lower()
        for genre in sorted(self.genres, key=lambda item: (len(item.get('title', '')), item.get('title', ''))):
            if needle in genre.get('title', '').lower():
                return genre
        return None

    def search_country(self, country_name: str) -> dict[str, Any] | None:
        needle = country_name.lower().strip()
        if not needle:
            return None
        for country in self.countries:
            if country.get('iso', '').lower() == needle:
                return country
        for country in sorted(self.countries, key=lambda item: (len(item.get('name', '')), item.get('name', ''))):
            if needle in country.get('name', '').lower() or needle in country.get('iso', '').lower():
                return country
        return None

    @property
    def has_pool(self) -> bool:
        return bool(self.current_tag or self.current_countrycode)

    def search_stations(
        self,
        *,
        tag: str | None = None,
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
        if self.current_tag:
            return self.search_stations(tag=self.current_tag)
        if self.current_countrycode:
            return self.search_stations(countrycode=self.current_countrycode)
        return []

    def resolve_url(self, station: Station) -> str:
        data = self._get(f'/json/url/{station.uuid}')
        if isinstance(data, dict) and data.get('url'):
            station.url = str(data['url'])
        return station.url

    def update_active_station(self, tag: str | None = None, countrycode: str | None = None) -> Station | None:
        if tag is not None:
            countrycode = None
        elif countrycode is not None:
            tag = None
        else:
            tag = self.current_tag
            countrycode = self.current_countrycode
        if self.current_tag != tag or self.current_countrycode != countrycode:
            self.current_tag = tag
            self.current_countrycode = countrycode
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
            if count > 1 and skip and station.uuid == skip:
                continue
            if self._activate(station):
                return self.active_station
        return None

    @property
    def stream_url(self) -> str:
        return self.active_station.url if self.active_station else ''

    def get_stream(
        self,
        tag: str | None = None,
        renew_active_station: bool = False,
        countrycode: str | None = None,
    ) -> str:
        same_pool = self.current_tag == tag and self.current_countrycode == countrycode
        if not self.active_station or not same_pool or renew_active_station:
            return self.stream_url if self.update_active_station(tag=tag, countrycode=countrycode) else ''
        return self.stream_url

    def next_station(self) -> str:
        if 0 <= self._history_index < len(self.history) - 1:
            self._history_index += 1
            return self._activate(self.history[self._history_index], record_history=False)
        if not self.has_pool:
            return ''
        return self.get_stream(self.current_tag, renew_active_station=True, countrycode=self.current_countrycode)

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
