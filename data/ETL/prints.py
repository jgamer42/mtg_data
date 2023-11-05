

import os
import sys

from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
import ijson
import requests
from databases.cache import cache_db
import subprocess
from databases.SQL import models as SQL_model
from databases import SQL_database

data = requests.get("https://api.scryfall.com/bulk-data/default-cards")
file = data.json()["download_uri"]
#print("Descargando")
download = subprocess.Popen(f"wget {file} -O {os.environ['PROJECT_PATH']}/cartas.json",shell=True)
download.wait()
#print("Procesando")
relevant_prefixes = ["item.set","item.rarity","item.reprint","item.card_faces.image_uris.small","item.card_faces.image_uris.normal","item.image_uris.normal","item.image_uris.small","item.name"]
prefix_map = {
    "item.set":"set",
    "item.rarity":"rarity",
    "item.reprint":"reprint",
    "item.card_faces.image_uris.small":"small_front_img",
    "item.card_faces.image_uris.normal":"normal_front_img",
    "item.image_uris.normal":"normal_front_img",
    "item.image_uris.small":"small_front_img",
    "item.name":"name"
}
cards = []
i = 0

prints_card = {}

with open(f'{os.environ["PROJECT_PATH"]}/cartas.json',"r") as f:
    data = {}
    for prefix, event, value in ijson.parse(f):
        if i == len(relevant_prefixes):
            oracle_id = cache_db.get(data["name"])
            del data["name"]
            if oracle_id in prints_card.keys():
                prints_card[oracle_id].append(data)
            else:
                prints_card[oracle_id] = [data]
            data = {}
            i = 0
            
        if prefix in relevant_prefixes:
            key_name = prefix_map[prefix]
            if prefix in ["item.card_faces.image_uris.small","item.card_faces.image_uris.normal"] and key_name in data.keys():
                key_name = key_name.replace("front","back")
                i =- 1
            data[key_name] = value
            i += 1
    f.close()
remove = subprocess.Popen(f"rm {os.environ['PROJECT_PATH']}/cartas.json",shell=True)
remove.wait()
print_to_create = []
for card in prints_card.keys():
    main_card = SQL_database.query(SQL_model.Card.id).filter(SQL_model.Card.scryfall_id==card).all()
    
    #print(main_card)
    if main_card is []:
        print(f"No existe {card}")
        continue
    for p in prints_card[card]:
        try:
            p["card"] = main_card[0][0]
        except:
            print(f"No existe {card}")
            break
        if cache_db.get(p["set"]):
            p["set"] = cache_db.get(p["set"])
        else:
            try:
                set_id = SQL_database.query(SQL_model.Set.id).filter(SQL_model.Set.code==p["set"]).all()
                cache_db.set(p["set"], set_id[0])
                p["set"] = set_id[0]
            except:
                print(f"No existe el set {p['set']}")
                continue
        print_to_create.append(SQL_model.Print(**p))
SQL_database.bulk_save_objects(print_to_create)
SQL_database.commit()