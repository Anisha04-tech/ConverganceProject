import os

def log_event(message):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
