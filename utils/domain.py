import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from constants import COLORS_IDENTITY,ALLOWED_FORMATS

def clean_colors(colors:list):
    try:
        processed = ''.join(sorted(list(set(colors))))
        return COLORS_IDENTITY.get(processed,"")
    except TypeError:
        return ""
    
def clean_mana_cost(mana_cost:str)->list:
    possible_colors = ["W","U","R","B","G"]
    present_colors = []
    for color in possible_colors:
        if color in mana_cost:
            present_colors.append(color)
    return present_colors

def clean_type(raw_type):
    principal_type = raw_type.split("—")[0].strip()
    principal_type = principal_type.replace("Legendary","").replace("Snow","").replace("Tribal","").replace("World","").replace("Token","").replace("Elemental","").strip().lower()
    sub_types = " ".join(raw_type.split("—")[1:]).strip()
    if "summon" in principal_type:
        principal_type = "creature"
    return (principal_type,sub_types)

def clean_prices(prices:dict)->dict:
    return {
        "usd":prices["usd"],
        "eur":prices["eur"],
        "usd_foil":prices["usd_foil"],
        "eur_foil":prices["usd_foil"]
    }


def clean_types(card):
    raw_type = card["type_line"]
    principal_type , sub_types = clean_type(raw_type)
    is_legendary = False
    is_snow=False
    if "legendary" in raw_type.lower():
        is_legendary=True
    if "snow" in raw_type:
        is_snow=True
    card["is_legendary"] = is_legendary
    card["is_snow"] = is_snow
    card["main_type"] = principal_type
    card["sub_type"] = sub_types
    
def clean_legalities(card):
    for format in ALLOWED_FORMATS:
        if card["legalities"][format].lower() == "not legal":
            target = False
        else:
            target = True 
        card[f"{format}_legal"] = target
    del card["legalities"]
    