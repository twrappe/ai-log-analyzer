import json
from pathlib import Path


def load_json(file_path: Path):
    """Load a JSON file and return its content"""
    with open(file_path, 'r') as f:
        return json.load(f)


def load_log_file(log_file: Path):
    events = []
    with open(log_file, 'r', errors='ignore', newline=None) as f:  # newline=None ensures \r\n handled
        for line in f:
            line = line.strip()
            if line:
                events.append({'raw': line})
    return events
