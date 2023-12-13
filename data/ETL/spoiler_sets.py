import os
import sys
from dotenv import load_dotenv
import logging
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from databases.SQL import models as SQL_model
from databases import SQL_database
from data.dataSources import ScryFall
from constants import BASIC_LANDS
from databases.cache import cache_db
logging.basicConfig(filename='spoilers.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
sets = SQL_database.query(SQL_model.Set.code,SQL_model.Set.id).where(SQL_model.Set.is_spoiler==True).all()

source = ScryFall()
REPRINTS = []
def insert_reprint(card_information,set_id):
    global REPRINTS
    card_id = cache_db.get(card["oracle_id"])
    if card_id is None:
        card_id = SQL_database.query(SQL_model.Card.id).where(SQL_model.Card.scryfall_id == card["oracle_id"].strip()).all()
        card_id = card_id[0][0]
        cache_db.set(card["oracle_id"],card_id)
    reprint = SQL_database.query(SQL_model.Print).where(SQL_model.Print.set == set_id and SQL_model.Print.card == card_id)
    exists_reprint = SQL_database.query(reprint.exists()).scalar()
    if exists_reprint:
        return None
    reprint_info = {
        "card":card_id,
        "set":set_id,
        "rarity":card_information["rarity"],
        "reprint":True,
    }
    
for set in sets:
    cards = source.get_cards_from_set(set[0])
    for card in cards:
        if card["name"].lower().strip() in BASIC_LANDS:
            continue
        possible_card = SQL_database.query(SQL_model.Card.id).where(SQL_model.Card.scryfall_id == card["oracle_id"].strip())
        exists_card = SQL_database.query(possible_card.exists()).scalar()
        if exists_card:
            insert_reprint(card,set[1])
        else:
            print("nueva carta")