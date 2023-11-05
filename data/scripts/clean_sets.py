import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
import pandas as pd
from constants import ALLOWED_FORMATS,BASIC_LANDS
from utils.domain import clean_colors,clean_type
from data.dataSources import ScryFall
import datetime
import json

mined_cards =[]

def clean_dataset_type(data:pd.DataFrame):
    for index, row in data.iterrows():
        raw_type = row["type_line"]
        principal_type , sub_types = clean_type(raw_type)
        is_legendary = False
        is_snow=False
        if "Legendary" in raw_type:
            is_legendary=True
        if "Snow" in raw_type:
            is_snow=True
        data.at[index,"is_legendary"] = is_legendary
        data.at[index,"is_snow"] = is_snow
        data.at[index,"principal type"] = principal_type
        data.at[index,"sub types"] = sub_types
        
def clean_ruling(data:pd.DataFrame):
    for index, row in data.iterrows():
        clean_str = row['legalities'].replace("'", '"').replace(
            '.', ',').replace('None', '"None"')
        legalities = json.loads(clean_str)
        for legality in legalities.keys():
            if legality in ALLOWED_FORMATS:
                data.at[index, legality] = legalities[legality]
        
def clean_dataset_colors(data: pd.DataFrame):
    for index, row in data.iterrows():
        aux_colors = row['colors']
        aux_identity = row['color_identity']
        aux_mana = row.get("produced_mana","[]")
        if pd.isna(aux_mana):
            aux_mana = "[]"
        if pd.isna(aux_colors):
            aux_colors = aux_identity
        data.at[index, 'colors'] = clean_colors(eval(aux_colors))
        data.at[index, 'color_identity'] = clean_colors(eval(aux_identity))
        data.at[index, 'produced_mana'] = clean_colors(eval(aux_mana))


def clean_price(data: pd.DataFrame):
    for index, row in data.iterrows():
        clean_str = row['prices'].replace("'", '"').replace(
            '.', ',').replace('None', '"None"')
        prices = json.loads(clean_str)
        for price in prices.keys():
            if "foil" in price or "etched" in price:
                continue
            try:
                data.at[index, price] = prices[price]
            except ValueError:
                data.at[index, price] = "0,0"


def get_detail_card(data: pd.DataFrame):
    source = ScryFall()
    target_data = data[data['reprint'] == True]
    for index, row in target_data.iterrows():
        try:
            card = source.get_card_by_name(row['name'])
            cards = sorted(card, key=lambda x: datetime.datetime.strptime(
                x['released_at'], '%Y-%m-%d'))
            data.at[index, 'original_print'] = cards[0]['set_name']
            data.at[index, 'original_print_type'] = cards[0]['set_type']
            mined_cards.append(row["name"])
        except:
            continue
for target in os.listdir(f'{os.environ["PROJECT_PATH"]}/data/mined_data/raw'):
    dataset_to_clean = f'{os.environ["PROJECT_PATH"]}/data/mined_data/raw/{target}'
    if target in os.listdir(f'{os.environ["PROJECT_PATH"]}/data/mined_data/clean'):
        print(f'skipping {target}')
        continue
    dataset = pd.read_csv(dataset_to_clean)
    try:
        relevant_columns = ['name', 'colors', 'mana_cost', 'cmc', 'color_identity', 'type_line', 'reprint', 'rarity', 'edhrec_rank', 'penny_rank', 'prices', 'power', 'toughness', 'produced_mana',"keywords","legalities","reserved","collector_number"]
        clean_data = dataset[relevant_columns]
    except KeyError as e:
        print(f"Fail {target} beacuse {e}")
        continue
    print(target)
    clean_data = clean_data[~clean_data.name.isin(BASIC_LANDS )]
    clean_dataset_colors(clean_data)
    clean_price(clean_data)
    clean_ruling(clean_data)
    clean_dataset_type(clean_data)
    get_detail_card(clean_data)
    del clean_data["prices"]
    del clean_data["legalities"]
    clean_data.drop_duplicates(keep='last')
    target_data_types = {
        "cmc":int
    }
    clean_data = clean_data.astype(target_data_types)
    clean_data.to_csv(f'{os.environ["PROJECT_PATH"]}/data/mined_data/clean/{target}')