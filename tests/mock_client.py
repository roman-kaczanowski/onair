from typing import Any

from cmd_fm_python.client.client import DirbleClient


class MockClient(DirbleClient):
    def get_genres(self) -> list[dict[str, Any]]:
        return [
            {
                'id': 1,
                'title': 'Trance',
                'description': 'stations that plays commercial and other things in trance-music genre.',
                'slug': 'trance',
                'ancestry': '14',
            },
            {
                'id': 2,
                'title': 'Rock',
                'description': 'simple rock. from elvis to metallica and like hardrock as iron maiden.',
                'slug': 'rock',
                'ancestry': None,
            },
            {
                'id': 3,
                'title': 'Dance',
                'description': "dance music, the new from 80's and 90's, like bubblegum and more.",
                'slug': 'dance',
                'ancestry': '14',
            },
            {
                'id': 4,
                'title': 'Dancehall',
                'description': 'dancehall music.',
                'slug': 'dancehall',
                'ancestry': '14',
            },
        ]

    def get_stations(self) -> list[dict[str, Any]]:
        return []
