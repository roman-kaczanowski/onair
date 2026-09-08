from mock_client import MockClient


def test_get_genres() -> None:
    client = MockClient('test_key')
    assert bool(client.get_genres())
    assert isinstance(client.get_genres(), list)


def test_genres_titles() -> None:
    client = MockClient('test_key')
    assert client.genres_titles == {
        'T': ['Trance'],
        'R': ['Rock'],
        'D': ['Dance', 'Dancehall'],
    }


def test_search_genre() -> None:
    client = MockClient('test_key')
    assert client.search_genre('rock')['id'] == 2
    assert client.search_genre('dancehall')['id'] == 4
    assert client.search_genre('wrong_genre') is None
    assert client.search_genre('ock')['id'] == 2
    assert client.search_genre('ance')['id'] == 3
