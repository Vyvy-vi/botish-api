import json

import toml


def get_json(file):
    with open(f"src/data/{file}.json", "r") as f:
        return json.load(f)[file]


def get_meta():
    with open("pyproject.toml", "r") as f:
        f = toml.load(f)["tool"]["poetry"]
        return {
            "name": f["name"],
            "version": "v" + f["version"],
            "description": f["description"],
            "license": {
                "name": f["license"],
                "url": "https://github.com/Heptagram-Bot/api/blob/master/LICENSE.md",
            },
            "repo": f["repository"],
            "author": {"name": "Vyvy-vi", "url": "https://github.com/Vyvy-vi"},
        }
