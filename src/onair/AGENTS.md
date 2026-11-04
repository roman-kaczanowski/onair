# onair package

## Map

- `__main__.py`: module entry point. Calls `app.main`.
- `app.py`: argument parsing, the `App` shell, prompt loop, completion, and status toolbar.
- `client/client.py`: Radio Browser server discovery, HTTP access, the `Station` model, station pools, and play history.
- `commands/`: one class per command family. Aliases subclass the canonical command. See `commands/AGENTS.md`.
- `player/player.py`: thin `python-vlc` wrapper. Imports `vlc` lazily so tests and non-playback code do not need the native library.
- `utils/colorize.py`: ANSI colors and `{{tag}}` template rendering.
- `utils/listing.py`: grouped and filtered list formatting for the home screen and list commands.

## Flow

`__main__.py` -> `app.main` -> `parse_args` -> `RadioBrowserClient` -> `App` -> `Command.handle` -> `Player`.

Startup flags are turned into command lines and run before the REPL starts. `App.run_line` dispatches one command; `App.onecmd` splits on `|` and runs each segment.

## Rules

- Keep rendering in the command layer. Reuse `colorize` and `render`; do not hand-write escape codes.
- Keep stream selection and playback setup in `commands/play.py` helpers (`try_tune`, `start_stream`, `now_playing`) instead of duplicating them.
- Do not do network or VLC work at import time. Constructing `RadioBrowserClient` may fetch genres; keep that inside `main` or an explicit call.
- Keep the client independent of the shell. It exposes data and stream URLs; commands decide what to print.
