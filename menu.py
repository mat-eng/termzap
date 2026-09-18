
from dataclasses import dataclass
from typing import List, Optional
import yaml
import curses
from run import run_embedded, run_embedded_blocking, run_detach_console, run_detach_no_console


@dataclass
class Item:
    label: str
    key: Optional[str] = None          # single-char shortcut, e.g. "b"
    command: Optional[str] = None      # shell command to run
    option: Optional[str] = None       # embedded, embedded-blocking, detach-console, detach-no-console
    submenu: Optional[List["Item"]] = None


class Menu:
    def __init__(self, stdscr, status):
        self.stdscr = stdscr
        self.item_selected = 0
        self.selection_history = []
        self.current_page = 0
        self.status = status

    @property
    def current_items(self):
        return self.stack[-1][1]

    @property
    def visible_items(self):
        return self.current_items
    
    def load_config(self, path: str):
        self.status.set(" Config reloaded.")
        self.path = path
        self.item_selected = 0
        self.selection_history = []
        self.current_page = 0
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        items = [self._parse_item(x) for x in data.get("items", [])]
        title = data.get("title", "Quick Menu")
        self.stack = [(title, items)]
    
    def get_current_page(self):
        breadcrumb = " → ".join(t for t, _ in self.stack)
        items = self.visible_items
        return breadcrumb, items, self.item_selected

    def handle_key(self, key):
        items = self.visible_items

        if key == curses.KEY_UP:
            self.item_selected = (self.item_selected - 1) % len(items)
        elif key == curses.KEY_DOWN:
            self.item_selected = (self.item_selected + 1) % len(items)
        elif key in (10, 13, curses.KEY_ENTER, curses.KEY_RIGHT):
            self.activate(items[self.item_selected])
        elif key in (27, curses.KEY_LEFT, 8):
            self.go_back()
        elif key in (ord('q'), ord('Q')):
            raise SystemExit
        elif key in (ord('r'), ord('R')):
            self.load_config(self.path)
        else:
            try:
                c = chr(key)
            except ValueError:
                c = None
            if c:
                for i, item in enumerate(items):
                    if item.key and item.key.lower() == c.lower():
                        self.item_selected = i
                        self.activate(item)
                        break

    def activate(self, item: Item):
        if item.submenu:
            self.selection_history.append(self.item_selected)
            self.stack.append((item.label, item.submenu))
            self.item_selected = 0
            return
        self.run_command(item)

    def run_command(self, item: Item):
        self.status.set(f" Launched: {item.label}")
        if item.option == 'embedded':
            curses.def_prog_mode()
            curses.endwin()
            code = run_embedded(item.label, item.command)
            self.status.set(f" '{item.label}' exited with code {code}")
            self.stdscr.clear()
            curses.reset_prog_mode()
            self.stdscr.keypad(True)
            self.stdscr.refresh()
        elif item.option == 'embedded-blocking':
            curses.def_prog_mode()
            curses.endwin()
            code = run_embedded_blocking(item.label, item.command)
            print(f"\n[exit code {code}] Press Enter to return to the menu...")
            input()
            self.status.set(f" '{item.label}' exited with code {code}")
            self.stdscr.clear()
            curses.reset_prog_mode()
            self.stdscr.keypad(True)
            self.stdscr.refresh()
        elif item.option == 'detach-console':
            run_detach_console(item.label, item.command)
        elif item.option == 'detach-no-console':
            run_detach_no_console(item.label, item.command)
        else:
            self.status.set(" Unsupported option defined for this item.")

    def go_back(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.item_selected = self.selection_history[-1]
            self.selection_history.pop()

    def go_home(self):
        while(len(self.stack) > 1):
            self.stack.pop()
            self.item_selected = 0
        self.selection_history = []


    def _parse_item(self, d: dict) -> Item:
        submenu = None
        if d.get("submenu"):
            submenu = [self._parse_item(x) for x in d["submenu"]]
        key = d.get("key")
        return Item(
            label=d.get("label", "?"),
            key=str(key) if key is not None else None,
            command=d.get("command"),
            option=d.get("option"),
            submenu=submenu,
        )
    