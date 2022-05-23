import requests
import json
import pandas as pd
import datetime as dt

SCRYFALL_ENDPOINT = "https://c2.scryfall.com/file/scryfall-bulk/default-cards/default-cards-20220521090423.json"


def ingest_scryfall_bulk_data(date):
    # TODO: when running this on schedule, add check to only ingest new data since last ingest. Use "released_at" field?
    response = requests.get(url=SCRYFALL_ENDPOINT)
    response.raise_for_status()
    data = response.json()
    with open(file=f"scryfall_bulk_imports/{date}_raw.json", mode="w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=True)


def clean_ingest_bulk_data(date):
    # Takes raw json from Scryfall and drops all un-needed fields and all online-only cards
    with open(file=f"scryfall_bulk_imports/{date}_raw.json", mode="r", encoding="utf8") as f:
        df = pd.read_json(f)  # file is raw from Scryfall and includes many unwanted fields

    slim_dataframe = df.loc[:, ["id", "name", "foil", "nonfoil", "set", "set_name", "collector_number", "digital"]]
    temp_dict = slim_dataframe.to_dict("records")  # converts to dict for efficiency
    digital_cards = [row for row in temp_dict if row["digital"] == False]

    with open(file=f"scryfall_bulk_imports/{dt.date.today()}_clean.json", mode="w", encoding="utf8") as f:
        json.dump(digital_cards, f, ensure_ascii=True)


search = {
    "name": "Fury Sliver",
    "foil": "true",
    "set": "tsp",
    "collector_number": 157
}

with open(file=f"scryfall_bulk_imports/{dt.datetime.today()}_clean.json", mode="r") as file:
    for key, value in search:
        pass

