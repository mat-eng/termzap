# Termzap

A keyboard-only, always-ready terminal launcher for quick work tasks (screen brightness, opening a dev terminal with a venv, locking the screen, running your own scripts, etc.). Runs in the terminal, works on Linux and Windows, and is fully customized through one YAML file — no code changes needed to add or change menu items.

## Install

```bash
pip install -r requirements.txt
```

On Windows, `windows-curses` (installed automatically by the line above) provides the `curses` module that the app is built on.

## Run

```bash
python main.py
```

Or point it at a different config file (handy if you keep separate configs per project):

```bash
python main.py path/to/other-config.yaml
```

## Keys

| Key             | Action                                   |
|-----------------|-------------------------------------------|
| Up/Down         | move selection                            |
| Enter/right     | run the selected item / open its submenu  |
| Esc/left        | go back one level                         |
| r               | reload config.yaml from disk (no restart) |
| q               | quit                                      |
| any other key   | jumps straight to the item bound to that shortcut |

## Customizing the menu

Everything lives in `config.yaml`. Each item is:

```yaml
- label: "Human-readable name"   # shown in the menu
  key: "b"                       # optional one-key shortcut
  command: "some shell command"  # what to run
  option: "embedded, embedded-blocking, detach-console, detach-no-console" # how the command shall be run
  submenu:                       # optional: nest more items instead of a command
    - ...
```

**Option details**

- `embedded`: the app pauses the curses screen, runs your command in the real terminal, and returns to the menu.
- `embedded-blocking`: the app pauses the curses screen, runs your command in the real terminal so you can see its output, and waits for you to press Enter before returning to the menu.
- `detach-console`: the command is launched in the background in a new terminal window and the menu keeps running immediately.
- `detach-no-console`: the command is launched in the background and the menu keeps running immediately. Use this for anything that opens its own window (a GUI app).

Since `command` is just a shell string, you can point it at **any script in any language** — Python, bash, PowerShell, whatever your project needs. Just make sure it's runnable from wherever you launch `main.py` (use absolute paths if you're not sure).

## Included example scripts

- `scripts/screen.py <percent delta>` — adjusts screen brightness. Uses `brightnessctl` on Linux and the `screen-brightness-control` package on Windows.

Edit these, replace them, or add your own scripts under `scripts/` — then wire them up as `command:` entries in `config.yaml`.

## Notes

- `r` (reload) is handy while you're iterating on `config.yaml` — no need to restart the app.
