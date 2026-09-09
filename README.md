# onair

[![CI](https://img.shields.io/github/actions/workflow/status/roman-kaczanowski/onair/quality-checks.yml?branch=main&style=flat-square&label=CI)](https://github.com/roman-kaczanowski/onair/actions/workflows/quality-checks.yml) [![PyPI](https://img.shields.io/pypi/v/onair?style=flat-square)](https://pypi.org/project/onair/) [![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/) [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

Turn your terminal into an internet radio. onair is a small interactive shell for finding and playing stations by genre or country.

## Features

- Browse popular genres and countries.
- Jump between stations and return to recently played ones.
- Pause, resume, mute, and adjust volume without leaving the prompt.
- Use tab completion, command history, and short aliases.
- Discover stations through [Radio Browser](https://www.radio-browser.info/) without an API key.

## Requirements

- Python 3.12 or newer.
- [VLC](https://www.videolan.org/vlc/) installed on your system. The `python-vlc` binding is installed with onair, but playback still requires the VLC application and its native library.

## Quick start

Install the release from PyPI:

```shell
python -m pip install onair
onair
```

Or run it without installing by using [uv](https://docs.astral.sh/uv/):

```shell
uvx onair
```

To run the source:

```shell
uv sync
uv run onair
```

Then choose a genre or country and start exploring:

```text
onair> help
onair> play chillout
onair> info
onair> next
onair> previous
onair> country poland
onair> volume +10
onair> pause
onair> resume
onair> stop
```

Run `help` for every command and `help play` for command-specific examples. Running `play` without a genre resumes paused playback or chooses a genre at random.

## Acknowledgments

Inspired by cmd.fm. onair is an independent project and is not affiliated with or endorsed by cmd.fm.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and release process.

## License

Licensed under the [MIT License](LICENSE).
