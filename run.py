"""
Handle the execution of commands
"""

import os
import subprocess
import tempfile

def run_embedded(label, command):
    print(f"\n--- Running: {label} ---\n$ {command}\n")
    try:
        result = subprocess.run(command, shell=True)
        code = result.returncode
    except Exception as e:
        code = -1
        print(f"Error: {e}")
    return code

def run_embedded_blocking(label, command):
    code = run_embedded(label, command)
    print(f"\n[exit code {code}] Press Enter to return to the menu...")
    try:
        input()
    except EOFError:
        pass
    return code

def run_detach_console(label, command):
    fd, batch_path = tempfile.mkstemp(suffix=".bat", prefix="quickmenu_")
    with os.fdopen(fd, "w") as f:
        f.write("@echo off\r\n")
        f.write(command + "\r\n")
    subprocess.Popen(["cmd", "/k", batch_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def run_detach_no_console(label, command):
    subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    