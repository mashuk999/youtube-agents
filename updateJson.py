import json
from datetime import date

def add_placeholder_entry(video_data, filename='urls.json'):
    """Adds an entry with placeholder URL 'YETTOBEUPLOADED'."""
    try:
        with open(filename, 'r') as f:
            url_entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        url_entries = []

    new_entry = {
        "url": "YETTOBEUPLOADED",
        "date": str(date.today()),
        "title": video_data.get("Video Title", "Untitled"),
        "hashtags": video_data.get("Hashtags", [])
    }

    url_entries.insert(0, new_entry)

    with open(filename, 'w') as f:
        json.dump(url_entries, f, indent=2)

    print(f"Placeholder entry added to {filename}.")

def update_placeholder_url(actual_url, filename='urls.json'):
    """Replaces the first occurrence of placeholder URL with the actual URL."""
    try:
        with open(filename, 'r') as f:
            url_entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing JSON data found.")
        return

    for entry in url_entries:
        if entry["url"] == "YETTOBEUPLOADED":
            entry["url"] = actual_url
            break
    else:
        print("No placeholder entry found.")
        return

    with open(filename, 'w') as f:
        json.dump(url_entries, f, indent=2)

    print(f"Placeholder URL updated to: {actual_url}")

