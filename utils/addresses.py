import json
import os

ADDRESS_FILE = "addresses.json"

def _load_all():
    """
    Load full address file.
    """
    if not os.path.exists(ADDRESS_FILE):
        return {}
    with open(ADDRESS_FILE) as f:
        return json.load(f)


def _save_all(data):
    """
    Save entire address structure.
    """
    with open(ADDRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_addresses(A, B, C, script_type):
    """
    Store addresses for a given script type.
    """
    data = _load_all()
    data[script_type] = {
        "A": A,
        "B": B,
        "C": C
    }
    _save_all(data)


def load_addresses(script_type):
    """
    Load addresses for a given script type.
    """
    data = _load_all()
    if script_type not in data:
        raise ValueError(f"No addresses stored for type: {script_type}")
    entry = data[script_type]
    return entry["A"], entry["B"], entry["C"]
