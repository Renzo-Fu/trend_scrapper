# utils.py
import json
import os
from config import JSON_FILE


def load_existing_ids():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return []


def save_new_ids(new_ids):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r+') as file:
            data = json.load(file)
            data.extend(new_ids)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        with open(JSON_FILE, 'w') as file:
            json.dump(new_ids, file, indent=4)
