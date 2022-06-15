import json
import glob
import os
import pandas as pd
import datetime as dt

SCRYFALL_ENDPOINT = "https://c2.scryfall.com/file/scryfall-bulk/default-cards/default-cards-20220521090423.json"


def ingest_scryfall_bulk_data():
    """Queries Scryfall API for list of cards. Drops un-necessary columns and saves list as new JSON file."""
    df = pd.read_json(SCRYFALL_ENDPOINT)
    slim_dataframe = df.loc[:, ["id", "name", "foil", "nonfoil", "set", "set_name", "collector_number", "digital"]]
    temp_dict = slim_dataframe.to_dict("records")  # converts to dict for efficiency
    digital_cards = [row for row in temp_dict if row["digital"] == False]

    with open(file=f"scryfall_bulk_imports/{dt.date.today()}_clean.json", mode="w", encoding="utf8") as f:
        json.dump(digital_cards, f, ensure_ascii=True)


# example of cards for testing. Includes all fields required to compare with scryfall
list_of_cards = [
    {
        "name": "Fury Sliver",
        "foil": "false",
        "set": "tsp",
        "collector_number": 157
    },
    {
        "name": "Queen Marchesa",
        "foil": "true",
        "set": "cn2",
        "collector_number": 78
    }
]


def clean_list(cards):
    """cleans data by converting foil to boolean and collector_number to string, then returns list as dataframe."""
    for card in cards:
        card["foil"].capitalize()
        card["foil"] = bool(card["foil"])
        card["collector_number"] = str(card["collector_number"])
    clean_list = pd.DataFrame.from_dict(data=cards)
    return validate_cards(clean_list)


def validate_cards(cards):
    """checks list of cards and finds row that contains same name, set, collector number and if the card can be foil
    or non-foil. Returns True or False for each card."""
    file_list = glob.glob("scryfall_bulk_imports/*")
    latest_file = max(file_list, key=os.path.getctime)
    with open(file=latest_file, mode="r") as file:
        df = pd.read_json(file)
    result = []

    standardized_list = cards
    for index, card in standardized_list.iterrows():
        if card.foil:
            card_result = df.loc[(df.name == card["name"]) & (df.foil == True) & (df.set == card["set"])]
            final_result = card_result["collector_number"].item() == card.collector_number
            if not final_result:
                result.append(f"{standardized_list.iloc[index, 0]} from {standardized_list.iloc[index, 2]}"
                              f"was not found in our records.")
        else:
            if df.loc[(df.name == card["name"]) & (df.nonfoil == True) & (df.set == card["set"])
                      & (df.collector_number.isin(card["collector_number"]))]:
                result.append(True)
            else:
                result.append(False)
    if len(result) == 0:
        return True
    else:
        return False


clean_list(list_of_cards)
