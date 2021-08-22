import json


def get_json(file):
    with open(f"src/data/{file}.json", "r") as f:
        return json.load(f)[file]
