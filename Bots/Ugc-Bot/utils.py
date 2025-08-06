import json
import os

SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    return {"reddit": [], "twitter": []}

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f)