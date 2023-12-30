import os
import re
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from databases.SQL import models as SQL_model
from databases import SQL_database
from utils.domain import clean_mana_cost,clean_colors


card_face = SQL_database.query(
    SQL_model.CardFace.cmc,SQL_model.CardFace.mana_cost,SQL_model.CardFace.colors,SQL_model.CardFace.color_identity,SQL_model.CardFace.name,SQL_model.CardFace.oracle_text).where(
        SQL_model.CardFace.colors == '' or SQL_model.CardFace.color_identity == ''
    ).all()

for card in card_face:
    
    raw_colors = clean_mana_cost(card[1])
    colors = clean_colors(raw_colors)   
    colors_in_card = re.findall(r'\{[WUBRG]\}',card[5])
    print(''.join(colors_in_card))
    #if colors != card[3] and colors != '':
    #    if card[3] == '':
    #        print("arreglable automaticamente", card[4])

        