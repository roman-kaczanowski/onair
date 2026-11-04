# Commands

## Contract

- Subclass `Command` and set `name`, `pattern`, `example`, and `description`. Set `show_in_main_help = False` for aliases.
- Implement `handle(app, *args) -> str`. Return the text to print or raise `CommandError` with a user-facing message.
- Use `app.stdout_print` for progress messages before slow work, then return the final text.
- Use `app.INDENT` and the helpers in `utils/colorize.py` and `utils/listing.py`.
- Keep help text in the class attributes. It is rendered by `Command.help` and `Command.one_line_help`.

## Registration

- Add every command class to the `commands` list in `commands/__init__.py`.
- Add an alias by subclassing the canonical command and overriding `name`, `pattern`, and `example`.
- Keep the canonical command first in the list so its help entry wins.

## Shared playback

- Use `try_tune`, `start_stream`, and `now_playing` from `commands/play.py` for tuning and playback.
- Use `starting_message` for the `Kind: value  Volume: n` line.
- Do not start a new player without stopping the current one. `start_stream` owns that lifecycle.

## Hidden behavior

- `|` command chaining in `App.onecmd` is an intentional undocumented easter egg. Do not add it to help text, README, or command docs.
