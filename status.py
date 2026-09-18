"""
Handle the status text and timeout
"""

import time

class Status:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.due_time = time.time()
        self.text = ""
        self.elapsed_text = ""

    def set(self, text):
        self.text = text
        self.due_time = time.time() + self.timeout

    def update(self):
        local_time = time.time()
        self.elapsed_text = f"({self.due_time - local_time:.1f})"
        if local_time >= self.due_time:
            self.text = ""
            self.elapsed_text = ""

    def get_text(self):
        if self.text:
            return f"{self.text} --- {self.elapsed_text}"
        else:
            return ""
