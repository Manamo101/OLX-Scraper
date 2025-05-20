import json
from pathlib import Path
from Offer import Offer


def save_offers(offers: set[Offer]):
    """Save offers to a JSON file."""
    try:
        with open('offers.json', 'w') as file:
            data = [item.__dict__ for item in offers]
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving state: {e}")
        raise e


def load_offers() -> set[Offer]:
    """Load offers from a JSON file."""
    try:
        with open('offers.json', 'r') as file:
            data = json.load(file)
            offers = {Offer(**item) for item in data}
            return offers
    except FileNotFoundError:
        return set()