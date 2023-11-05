import os
import sys
import json
import multiprocessing
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from constants import BASIC_LANDS
from data.dataSources import ScryFall
from databases.SQL import models as SQL_model
from databases import SQL_database
from databases.cache import cache_db
from utils.domain import clean_legalities
SQL_database.rollback()

def add_to_cache_list(key,value):
    cache_db.set(key, value)
    cache_db.sadd('cards', key)


def get_cards(set_name:str,id:int):
    output = []
    source = ScryFall()
    cards = source.get_cards_from_set(set_name)
    cache_db.set(set_name,id)
    for card in cards:
        processed_card = {}
        try:
            if card["name"].lower() in BASIC_LANDS or cache_db.get(card["oracle_id"]) or card["layout"] in ["token"] or cache_db.get(card["name"]):
                continue
        except KeyError: 
            print("falle por oracle id",card["name"],card.keys(),"\n\n")
            continue
        except TypeError:
            print("falle por tipo",card)
            continue
        add_to_cache_list(card["oracle_id"],json.dumps(card))
        add_to_cache_list(card["name"],card["oracle_id"])
        for relevant_field in ["oracle_id",'name', 'colors', 'mana_cost', 'cmc', 'color_identity', 'type_line', 'edhrec_rank', 'penny_rank', 'power', 'toughness', 'produced_mana',"keywords","legalities","oracle_text","reserved"]:
            processed_card[relevant_field] = card.get(relevant_field,None)
        clean_legalities(processed_card)
        base_card_info = {
            "name":processed_card["name"],
            "scryfall_id":processed_card["oracle_id"],
            "edhc_rank":processed_card['edhrec_rank'],
            "penny_rank":processed_card['penny_rank'],
            "commander_legal":processed_card["commander_legal"] == "legal",
            "standard_legal":processed_card["standard_legal"] == "legal",
            "modern_legal":processed_card["modern_legal"] == "legal",
            "pioneer_legal":processed_card["pioneer_legal"] == "legal",
            "pauper_legal":processed_card["pauper_legal"] == "legal",
            "reserved_list":bool(processed_card["reserved"])
        }
        output.append(SQL_model.Card(**base_card_info))
    return output

sets = SQL_database.query(SQL_model.Set.code,SQL_model.Set.id).all()
sets = [(result[0],result[1]) for result in sets]
pool = multiprocessing.Pool(processes=10)
processed_cards = pool.starmap(get_cards,sets)
cards_to_insert = []
for card in processed_cards:
    cards_to_insert += card
SQL_database.bulk_save_objects(cards_to_insert)
SQL_database.commit()
        