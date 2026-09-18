"""
Provide the UI in strings format
"""

HEADER_H = 3
STATUS_H = 3
FOOTER_H = 3

UI_MARKER_W = 2 # For both of left and right "│"
UI_MARKER_H = 2 # For both of top and bottom "─"

MIN_CONTENT_H = UI_MARKER_H + 3

FOOTER_TEXT = "↑/↓: Move    Enter/→: Select    Esc/←: Back    r: Reload    q: Quit"
FOOTER_TEXT_LEN = len(FOOTER_TEXT)

MIN_REQUIRED_H = HEADER_H + STATUS_H + FOOTER_H + MIN_CONTENT_H
MIN_REQUIRED_W = FOOTER_TEXT_LEN + UI_MARKER_W


class UI:
    def __init__(self):
        pass

    def build_array(self, h, w, header, items, selected, status):
        self.h = h
        self.content_h = h - HEADER_H - STATUS_H - FOOTER_H - UI_MARKER_H
        self.w = w
        self.content_w = w - UI_MARKER_W

        if not self._check_size():
            return self._error_array()

        array = []
        array.extend(self._get_section(header, self._create_line_left))
        array.extend(self._get_content(items, selected))
        array.extend(self._get_section(status, self._create_line_left))
        array.extend(self._get_section(FOOTER_TEXT, self._create_line_center))
        return array


    # ---------- check size ----------

    def _check_size(self):
        if self.h < MIN_REQUIRED_H or self.w < MIN_REQUIRED_W:
            return False
        else:
            return True

    def _error_array(self):
        error = []
        error.append(self._get_top_line())
        for i in range(0, self.h-2):
            error.append(self._get_filled_line())
        error.append(self._get_bottom_line())
        return error


    # ---------- section ----------

    def _get_content(self, items, selected):
        content = []
        content.append(self._get_top_line())

        if len(items) > self.content_h:
            self.content_h -= 2
            if selected == 0:
                content.append(self._get_no_scroll_line())
            else:
                content.append(self._get_scrollup_line())

        if selected >= self.content_h:
            offset = selected - self.content_h + 1
        else:
            offset = 0

        for i in range(0, self.content_h):
            if i >= len(items):
                content.append(self._get_empty_line())
            else:
                marker = ">" if i+offset == selected else " "
                suffix = "→" if items[i+offset].submenu else ""
                content.append(self._create_line_left(f"  {marker} [{items[i+offset].key}] {items[i+offset].label} {suffix}"))

        if len(items) > self.content_h:
            if selected == len(items)-1:
                content.append(self._get_no_scroll_line())
            else:
                content.append(self._get_scrolldown_line())
            
        content.append(self._get_bottom_line())
        return content

    def _get_section(self, text, line):
        section = []
        section.append(self._get_top_line())
        section.append(line(text))
        section.append(self._get_bottom_line())
        return section

    # ---------- lines for ui ----------

    def _get_top_line(self):
        return "╭" + "─" * (self.content_w) + "╮"

    def _get_bottom_line(self):
        return "╰" + "─" * (self.content_w) + "╯"

    def _get_empty_line(self):
        return self._create_line_center(" " * self.content_w)

    def _get_filled_line(self):
        return self._create_line_center("░" * self.content_w)

    def _get_scrollup_line(self):
        return self._create_line_center("--- ↑ ---")
    
    def _get_no_scroll_line(self):
        return self._create_line_center("--- - ---")
    
    def _get_scrolldown_line(self):
        return self._create_line_center("--- ↓ ---")
    

    # ---------- lines with text ----------

    def _create_line_left(self, text):
        s = self._get_spacer(len(text))
        line = "│" + text + " " * s + "│"
        return line

    def _create_line_center(self, text):
        s_a, s_b = self._get_spacers(len(text))
        line = "│" + s_a * " " + text + " " * s_b + "│"
        return line

    # ---------- Helpers ----------

    def _get_spacer(self, used_space):
        spacer = self.content_w - used_space
        return spacer
    
    def _get_spacers(self, used_space):
        spacer_a = int((self.content_w - used_space)/2)        
        spacer_b = spacer_a + ((self.content_w - used_space) % 2)
        return spacer_a, spacer_b
