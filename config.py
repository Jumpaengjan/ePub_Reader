import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.json")

def save_last_folder(path):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"library_folder": path}, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def load_last_folder():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            folder = data.get("library_folder")
            if folder and os.path.isdir(folder):
                return folder
        except Exception as e:
            print(f"Error loading config: {e}")
    return None

def load_progress(book_path):
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        return data.get(book_path, {}).get("page", 0)
    except:
        return 0

def save_progress(book_path, book_type, page):
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}
    data[book_path] = {"type": book_type, "page": page}
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)