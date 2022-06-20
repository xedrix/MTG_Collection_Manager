import sqlite3
import json
import glob
import os
import pandas as pd

conn = sqlite3.connect("../database/scryfall_data.db")
c = conn.cursor()

"""
Kept as an example. Already set up this table.
def create_table():
    c.execute('''CREATE TABLE card_data
    (id integer, name text, foil integer, nonfoil integer, set_abbr text, set_name text)''')
    conn.commit()
    conn.close()
"""


def update_table(table: str, data: list):
    """takes table to update the table you want and the data as a list of tuples
    with id, name, foil, nonfoil, set and set_name"""
    c.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()


def initial_dump():
    with open(file="../scryfall_bulk_imports/scryfall_data.json", mode="r") as file:
        data = json.load(file)
    data_to_upload = [
        (card["id"], card["name"], card["foil"], card["nonfoil"], card["set"], card["set_name"])for card in data
    ]
    update_table(table="card_data", data=data_to_upload)


def weekly_update():
    """Grabs new file from scryfall_bulk_imports folder
    then keeps cards not in sql table, then updates table with new cards."""
    file_list = glob.glob("scryfall_bulk_imports/*")
    latest_file = max(file_list, key=os.path.getctime)
    with open(file=latest_file, mode="r") as file:
        new_cards = pd.read_json(file)
    current_cards = pd.read_sql("select id from card_data", con=conn)
    cards_to_add = new_cards.loc[~new_cards["id"].isin(current_cards.id)]
    if not cards_to_add.empty:
        print(f"The following cards were added: \n {cards_to_add}")
        data_to_upload = [
            (card["id"], card["name"], card["foil"], card["nonfoil"], card["set"],
             card["set_name"]) for card in cards_to_add
        ]
        update_table(table="card_data", data=data_to_upload)
    else:
        print("All cards were already in the database.")


