import json
import os

def load_json_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found.")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_items_for_prompt(items):
    return "\n".join([
        f"- {item.get('title', 'Untitled')}: {item.get('description', '')} (Link: {item.get('link', 'N/A')})"
        for item in items
    ])
