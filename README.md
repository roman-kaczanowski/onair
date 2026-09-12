# onair

[![CI](https://img.shields.io/github/actions/workflow/status/roman-kaczanowski/onair/quality-checks.yml?branch=main&style=flat-square&label=CI)](https://github.com/roman-kaczanowski/onair/actions/workflows/quality-checks.yml) [![PyPI](https://img.shields.io/pypi/v/onair?style=flat-square)](https://pypi.org/project/onair/) [![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/) [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

Turn your terminal into an internet radio. onair is a small interactive shell for finding and playing stations by genre, country, or language.

## Features

- Browse genres, countries, and languages, optionally filtered by name.
- Play a genre, a country (name or ISO code), a language, or a random genre.
- Jump between stations and return to recently played ones.
- Pause, resume, stop, mute, unmute, and set volume with `n`, `+n`, or `-n`.
- Start with flags such as `--play jazz --volume 30` (or `-p` / `-v`), then continue in the REPL.
- Show the current station with `info`.
- Tab completion, command history, and short aliases (`p`, `c`, `l`, `v`, `m`, and others).
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
onair --language polish
onair -l polish
onair --version
```

Startup flags select a station and set its initial volume before opening the interactive shell. When only a volume flag is given, onair chooses a random genre.

## Common tasks

Start quietly and keep the interactive shell open:

```shell
onair --play jazz --volume 20
```

Browse before choosing a station:

```text
onair> genres chill
onair> countries pol
onair> languages en
onair> play chillout
```

Move between stations and inspect the current one:

```text
onair> next
onair> previous
onair> info
```

## Commands

Run `help` for every command and `help play` for command-specific examples.

Discover:

- `genres [filter]` lists genres.
- `countries [filter]` lists countries.
- `languages [filter]` lists languages.
- `play [genre]` (`p`) plays a genre. With no genre, it resumes paused playback or picks a genre at random.
- `country [name|ISO]` (`c`) plays a station from a country.
- `language [name]` (`lang`, `l`) plays a station in a language.

Playback:

- `next` (`skip`) plays the next station.
- `previous` (`prev`, `back`) plays the previous station.
- `pause` / `resume` / `stop` control playback without leaving the shell.
- `mute` (`m`) and `unmute` (`um`) silence or restore audio.
- `volume [n|+n|-n]` (`v`, `vol`) sets volume, or changes it with `+n` / `-n`.

Session:

- `info` (`i`, `information`) shows the current station.
- `help [command]` lists commands or explains one command.
- `quit` (`q`, `exit`, `e`) stops playback and exits.

## Troubleshooting

- No audio: make sure the VLC application is installed, then restart the terminal.
- A station does not play: try `next` or choose another genre, country, or language.
- Lists are empty: Radio Browser may be unavailable or blocked by the network. Try again later.

## Acknowledgments

Inspired by cmd.fm. onair is an independent project and is not affiliated with or endorsed by cmd.fm.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and release process.

## License

Licensed under the [MIT License](LICENSE).
