import json
import os

import requests

INFRAS = [
    "advanced_stop_line",
    "crossing",
    "cycle_lane_track",
    "restricted_route",
    "cycle_parking",
    "restricted_point",
    "signage",
    "signal",
    "traffic_calming",
]
BASE_URL = "https://cycling.data.tfl.gov.uk/CyclingInfrastructure/data/lines/"
DATA_DIR = "cycle_data/"


def fetch_json(type: str):
    assert type in INFRAS
    url = BASE_URL + type + ".json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for infra in INFRAS:
        try:
            data = fetch_json(infra)
            with open(DATA_DIR + infra + ".json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Failed to fetch {infra}: {e}")
            continue
