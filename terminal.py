"""
Handle the resizing and positioning of the terminal window
"""

import win32gui
import win32con
import ctypes

def resize():
    # Screen dimensions
    user32 = ctypes.windll.user32
    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)

    # Find the terminal window
    hwnd = win32gui.GetForegroundWindow()

    # Move and resize it to the top-left quarter
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.MoveWindow(
        hwnd,
        screen_w // 3,  # X
        screen_h // 3,  # Y
        screen_w // 3,  # Width
        screen_h // 3,  # Height
        True
    )
    