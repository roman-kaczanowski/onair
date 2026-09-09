# onair

[![CI](https://img.shields.io/github/actions/workflow/status/roman-kaczanowski/onair/quality-checks.yml?branch=main&style=flat-square&label=CI)](https://github.com/roman-kaczanowski/onair/actions/workflows/quality-checks.yml) [![PyPI](https://img.shields.io/pypi/v/onair?style=flat-square)](https://pypi.org/project/onair/) [![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/) [![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

Interactive REPL shell radio. Stations come from [Radio Browser](https://www.radio-browser.info/) (no API key). VLC is required for playback (`python-vlc`).

```shell
uv sync
uv run onair
```

```text
onair> play chillout
onair> genres
onair> info
onair> next
onair> previous
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and releases.

MIT. Replace `LICENSE` if you need a different license.
