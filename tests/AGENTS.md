# Tests

## Layout

- pytest collects from `tests/` and puts both `src` and `tests` on `pythonpath`.
- `mock_client.py` provides `MockClient`, an in-memory `RadioBrowserClient` with fixed genres, countries, languages, and stations.
- `test_commands.py` drives `App` and commands. `test_client.py` covers client state and mapping. `test_player.py` covers the VLC wrapper. `test_utils.py` covers formatting helpers.

## Rules

- Never use the network or real VLC. Use `MockClient` and patch `sys.modules['vlc']` as `test_player.py` does.
- Construct `App` with `test=True` to skip the startup screen, and pass a mock stdout when asserting output.
- Reuse the ANSI-stripping helpers in `test_commands.py` instead of matching escape codes directly.
- Add the smallest test that fails when non-trivial logic breaks. One-liners need no new test.

## Commands

```shell
poe test
uv run pytest tests/test_commands.py
```
