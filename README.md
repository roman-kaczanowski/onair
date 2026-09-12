# onair

[![CI](https://img.shields.io/github/actions/workflow/status/roman-kaczanowski/onair/quality-checks.yml?branch=main&style=flat-square&label=CI)](https://github.com/roman-kaczanowski/onair/actions/workflows/quality-checks.yml) [![PyPI](https://img.shields.io/pypi/v/onair?style=flat-square)](https://pypi.org/project/onair/) [![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/) [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

Turn your terminal into an internet radio. onair is a small interactive shell for finding and playing stations by genre or country.

## Features

- Browse genres and countries, optionally filtered by name.
- Play a genre, a country (name or ISO code), or a random genre.
- Jump between stations and return to recently played ones.
- Pause, resume, stop, mute, unmute, and set volume with `n`, `+n`, or `-n`.
- Start with flags such as `--play jazz --volume 30` (or `-p` / `-v`), then continue in the REPL.
- Show the current station with `info`.
- Tab completion, command history, and short aliases (`p`, `c`, `v`, `m`, and others).
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

Start a station from the command line, then keep using the shell:

```shell
onair --play jazz --volume 30
onair -p jazz -v 30
onair --country poland
onair -c poland
onair --version
```

Short flags are `-p` / `--play`, `-c` / `--country`, and `-v` / `--volume`. They run left to right and map to the same commands as the REPL. A failed flag stops the rest of the startup sequence, then the prompt still opens. With flags, startup skips the genre preview and shows the banner, welcome text, then the command output.

## Commands

Run `help` for every command and `help play` for command-specific examples.

Discover:

- `genres [filter]` lists genres.
- `countries [filter]` lists countries.
- `play [genre]` plays a genre. With no genre, it resumes paused playback or picks a genre at random.
- `country [name|ISO]` plays a station from a country.

Playback:

- `next` / `previous` jump to the next or previous station.
- `pause` / `resume` / `stop` control playback without leaving the shell.
- `mute` / `unmute` silence or restore audio.
- `volume [n|+n|-n]` sets volume, or changes it with `+n` / `-n`.

Session:

- `info` shows the current station.
- `help [command]` lists commands or explains one command.
- `quit` stops playback and exits.

```text
onair> help
onair> play chillout
onair> info
onair> next
onair> previous
onair> country poland
onair> volume +10
onair> mute
onair> unmute
onair> pause
onair> resume
onair> stop
```

## Acknowledgments

Inspired by cmd.fm. onair is an independent project and is not affiliated with or endorsed by cmd.fm.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and release process.

## License

Licensed under the [MIT License](LICENSE).
