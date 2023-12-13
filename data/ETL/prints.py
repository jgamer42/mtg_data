

import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
import ijson

import requests
from databases.cache import cache_db
import subprocess
from databases.SQL import models as SQL_model
from databases import SQL_database
from constants import BASIC_LANDS

data = requests.get("https://api.scryfall.com/bulk-data/default-cards")
file = data.json()["download_uri"]
logging.basicConfig(filename='sets.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

download = subprocess.Popen(f"wget {file} -O {os.environ['PROJECT_PATH']}/cartas.json",shell=True)
download.wait()


prefix_map = {
    "item.set":"set",
    "item.rarity":"rarity",
    "item.reprint":"reprint",
    "item.card_faces.item.image_uris.small":"small_front_img",
    "item.card_faces.item.image_uris.normal":"normal_front_img",
    "item.image_uris.normal":"normal_front_img",
    "item.image_uris.small":"small_front_img",
    "item.name":"name",
    "item.id":"id",
    "item.oracle_id":"scryfall_id"
}
relevant_prefixes = set(prefix_map.keys())
cards = []
excluded_sets = set()
first = True
with open(f'{os.environ["PROJECT_PATH"]}/cartas.json',"r") as f:
    new_card = {}
    key_count = 0
    for prefix, event, value in ijson.parse(f):
        if prefix in relevant_prefixes:
            key_name = prefix_map[prefix]   
            if key_name in new_card.keys():
                new_card[f"{key_name}_{key_count}"] = value
                key_count += 1
            else:
                new_card[key_name] = value
            if prefix == "item.id" and not first:
                cards.append(new_card)
                new_card = {}
                key_count = 0
            elif prefix == "item.id" and first:
                first = False
    f.close()
prints_to_insert = []
pending_sets = set()
for card in cards:
    if card["name"] in BASIC_LANDS:
        continue
    if "scryfall_id" not in card.keys():
        print(f"Falta ",card["name"],card["set"])
        continue
    card_id = cache_db.get(f'xxx-{card["scryfall_id"]}')
    if card_id is None:
        card_id = SQL_database.query(SQL_model.Card.id).where(SQL_model.Card.scryfall_id == card["scryfall_id"].strip()).all()
        if card_id == []:
            continue
        card_id = card_id[0][0]
        cache_db.set(f'xxx-{card["scryfall_id"]}',card_id)
    set_id = cache_db.get(card["set"])
    if set_id is None:
        set_id = SQL_database.query(SQL_model.Set.id).where(SQL_model.Set.code == card["set"]).all()
        if set_id == []:
            pending_sets.add(f'xxx-{card["set"]}')
            continue
        set_id = set_id[0][0]
        cache_db.set(f'xxx-{card["set"]}',set_id)
    target_print = {
        "card":card_id,
        "set":set_id,
        "small_front_img":card["small_front_img"],
        "normal_front_img":card["normal_front_img"],
        "small_back_img":card.get("small_front_img_1",None),
        "normal_back_img":card.get("normal_front_img_1",None),
        "reprint":bool(card["reprint"]),
        "rarity":card["rarity"]
    }
    prints_to_insert.append(SQL_model.Print(**target_print))
SQL_database.bulk_save_objects(prints_to_insert)
SQL_database.commit()
print(pending_sets)
remove = subprocess.Popen(f"rm {os.environ['PROJECT_PATH']}/cartas.json",shell=True)
remove.wait()