import json
import os
import sys
import json
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from databases.cache import cache_db
from utils.domain import clean_colors,clean_types
from databases.SQL import models as SQL_model
from databases import SQL_database


cards = SQL_database.query(SQL_model.Card.scryfall_id,SQL_model.Card.id).all()
CARDS = [(result[0],result[1]) for result in cards]

def insert_card_faces():
    global CARDS
    faces_to_insert = []
    for card in CARDS:
        processed_card = json.loads(cache_db.get(card[0]))
        if processed_card.get("card_faces",False):
            for face in processed_card["card_faces"]:
                face_card_info = {
                    "name":face["name"],
                    "mana_cost":face.get("mana_cost","0"),
                    "colors":clean_colors(face.get("colors",[])),
                    "cmc":face.get("cmc","0"),
                    "color_identity":clean_colors(face.get("color_identity",[])),
                    "type_line":face.get("type_line",""),
                    "power":face.get("power",""),
                    "toughness":face.get("toughness",""),
                    "produced_mana":clean_colors(face.get("produced_mana",[])),
                    "key_words":face.get("keywords",[]),
                    "oracle_text":face.get("oracle_text",""),
                    "card":card[1]
                }
                clean_types(face_card_info)
                faces_to_insert.append(SQL_model.CardFace(**face_card_info))                
        else:
            face_card_info = {
                "name":processed_card["name"],
                "mana_cost":processed_card.get("mana_cost","0"),
                "colors":clean_colors(processed_card.get("colors",[])),
                "cmc":processed_card.get("cmc",""),
                "color_identity":clean_colors(processed_card.get("color_identity")),
                "type_line":processed_card.get("type_line",""),
                "power":processed_card.get("power",""),
                "toughness":processed_card.get("toughness",""),
                "produced_mana":clean_colors(processed_card.get("produced_mana",[])),
                "key_words":processed_card.get("keywords",""),
                "oracle_text":processed_card.get("oracle_text",""),
                "card":card[1]
            }
            clean_types(face_card_info)
            faces_to_insert.append(SQL_model.CardFace(**face_card_info))
    SQL_database.bulk_save_objects(faces_to_insert)
    SQL_database.commit()
    print("final hilo de faces")
insert_card_faces()