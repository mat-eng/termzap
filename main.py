import curses
import sys
import os

from terminal import resize
from ui import UI
from menu import Menu
from status import Status


CONFIG_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config-example.yaml"
)


class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.timeout(100)    # [ms]; time to wait for a key
        self.h = 0
        self.w = 0
        self.ui = UI()
        self.status = Status()
        self.last_status = ""
        self.menu = Menu(stdscr, self.status)
        self.update = True

        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
    def init(self):
        self.menu.load_config(CONFIG_PATH)

    def update_env(self):
        h, w = self.stdscr.getmaxyx()
        if h != self.h or w != self.w:
            self.h = h
            self.w = w
            self.update = True

    def update_input(self):
        key = self.stdscr.getch()
        if key != -1:
            self.menu.handle_key(key)
            self.update = True

    def update_ui(self):
        header, items, selected = self.menu.get_current_page()
        if self.status.get_text() != self.last_status:
            self.last_status = self.status.get_text()
            self.update = True
        if self.update:
            self.ui_array = self.ui.build_array(self.h, self.w, header, items, selected, self.status.get_text())
        
    def draw_ui(self):
        if self.update:
            self.stdscr.erase()
            for i, row in enumerate(self.ui_array):
                try:
                    if ">" in str(row):
                        self.stdscr.addstr(i, 0, str(row), curses.color_pair(1))
                        self.stdscr.addstr(i, 2, str(row[2:]), curses.color_pair(2))
                        self.stdscr.addstr(i, len(row)-2, str(row[-2:]), curses.color_pair(1))
                    else:    
                        self.stdscr.addstr(i, 0, str(row), curses.color_pair(1))
                except curses.error:
                    pass
            self.stdscr.refresh()
        self.update = False

    def loop(self):
        self.init()
        while True:
            self.update_env()
            self.update_input()
            self.status.update()
            self.update_ui()
            self.draw_ui()


###############################################################

def main(stdscr):
    app = App(stdscr)
    app.loop()

if __name__ == "__main__":
    resize()    # resize terminal
    curses.wrapper(main)
