from dotenv import load_dotenv
import os
import sys
load_dotenv()
sys.path.append(f'{os.environ["PROJECT_PATH"]}')

from databases.cache import cache_db
from constants import BASIC_LANDS
from data.dataSources import ScryFall
from databases import SQL_database
from databases.SQL import models as SQL_model
import logging
from utils.domain import clean_colors, clean_types,clean_legalities

logging.basicConfig(filename='spoilers.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
sets = SQL_database.query(SQL_model.Set.code, SQL_model.Set.id).where(
    SQL_model.Set.is_spoiler == True).all()
source = ScryFall()
REPRINTS = []


def insert_reprint(card_information, set_id):
    global REPRINTS
    card_id = cache_db.get(card["oracle_id"])
    if card_id is None:
        card_id = SQL_database.query(SQL_model.Card.id).where(
            SQL_model.Card.scryfall_id == card["oracle_id"].strip()).all()
        card_id = card_id[0][0]
        cache_db.set(card["oracle_id"], card_id)
    reprint = SQL_database.query(SQL_model.Print).where(
        SQL_model.Print.set == set_id and SQL_model.Print.card == card_id)
    exists_reprint = SQL_database.query(reprint.exists()).scalar()
    if exists_reprint:
        return None
    if card_information.get("card_faces", []) == []:
        reprint_info = {
            "card": card_id,
            "set": set_id,
            "rarity": card_information["rarity"],
            "reprint": True,
            "small_front_img": card["image_uris"]["small"],
            "normal_front_img": card["image_uris"]["normal"],
        }
    else:
        reprint_info = {
            "card": card_id,
            "set": set_id,
            "rarity": card_information["rarity"],
            "reprint": card_information["reprint"],
            "small_front_img": card["card_faces"][0]["image_uris"]["small"],
            "normal_front_img": card["card_faces"][0]["image_uris"]["normal"],
            "small_back_img": card["card_faces"][1]["image_uris"]["small"],
            "normal_back_img": card["card_faces"][1]["image_uris"]["normal"],
        }
    print(f"nuevo reprint {card['name']} {card['set']}")
    REPRINTS.append(SQL_model.Print(**reprint_info))


def insert_new_card(card_info, set_id):
    faces_to_insert = []
    clean_legalities(card_info)
    new_card_info = {
        "scryfall_id": card_info["oracle_id"],
        "edhc_rank": card_info.get("edhrec_rank",0),
        "penny_rank": card_info.get("penny_rank",0),
        "commander_legal": card_info["commander_legal"],
        "standard_legal": card_info["standard_legal"],
        "modern_legal": card_info["modern_legal"],
        "pioneer_legal": card_info["pioneer_legal"],
        "pauper_legal": card_info["pauper_legal"],
        "name": card_info["name"],
        "reserved_list": card_info["reserved"]
    }
    
    new_card = SQL_model.Card(**new_card_info)
    SQL_database.add(new_card)
    SQL_database.commit()
    if card_info.get("card_faces", []) == []:
        face_card_info = {
            "name": card_info["name"],
            "mana_cost": card_info.get("mana_cost", "0"),
            "colors": clean_colors(card_info.get("colors", [])),
            "cmc": card_info.get("cmc", ""),
            "color_identity": clean_colors(card_info.get("color_identity")),
            "type_line": card_info.get("type_line", ""),
            "power": card_info.get("power", ""),
            "toughness": card_info.get("toughness", ""),
            "produced_mana": clean_colors(card_info.get("produced_mana", [])),
            "key_words": card_info.get("keywords", ""),
            "oracle_text": card_info.get("oracle_text", ""),
            "card": new_card.id
        }
        clean_types(face_card_info)
        new_face = SQL_model.CardFace(**face_card_info)
        SQL_database.add(new_face)
        SQL_database.commit()
    else:
        for face in card_info["card_faces"]:
            face_card_info = {
                "name": face["name"],
                "mana_cost": face.get("mana_cost", "0"),
                "colors": clean_colors(face.get("colors", [])),
                "cmc": face.get("cmc", "0"),
                "color_identity": clean_colors(face.get("color_identity", [])),
                "type_line": face.get("type_line", ""),
                "power": face.get("power", ""),
                "toughness": face.get("toughness", ""),
                "produced_mana": clean_colors(face.get("produced_mana", [])),
                "key_words": face.get("keywords", []),
                "oracle_text": face.get("oracle_text", ""),
                "card": card[1]
            }
            clean_types(face_card_info)
            faces_to_insert.append(SQL_model.CardFace(**face_card_info))
        SQL_database.bulk_save_objects(faces_to_insert)
    insert_reprint(card_info,set_id)



for set in sets:
    cards = source.get_cards_from_set(set[0])
    for card in cards:
        if card["name"].lower().strip() in BASIC_LANDS:
            continue
        if card["layout"] in ["token"]:
            continue
        possible_card = SQL_database.query(SQL_model.Card.id).where(
            SQL_model.Card.scryfall_id == card["oracle_id"].strip())
        exists_card = SQL_database.query(possible_card.exists()).scalar()
        if exists_card:
            insert_reprint(card, set[1])
        else:
            insert_new_card(card,set[1])
            print(card["name"], card["set"], card["layout"], "nueva carta")
SQL_database.bulk_save_objects(REPRINTS)
SQL_database.commit()
