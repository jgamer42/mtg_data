import os
import sys
from dotenv import load_dotenv
load_dotenv() 
from sqlalchemy import Column, Integer, String,Float,JSON,Boolean,Text,ForeignKey,DateTime
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from databases import SQL_model_base
from datetime import datetime 


class Set(SQL_model_base):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    kind = Column(String(250),nullable=False)
    name = Column(String(250),nullable=False)
    code = Column(String(250),nullable=False)
    scry_fall_id = Column(String(250),nullable=False)
    is_spoiler = Column(Boolean,default=False)


class Card(SQL_model_base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    scryfall_id = Column(String(250),nullable=False)
    edhc_rank = Column(Float,nullable=True)
    penny_rank = Column(Float,nullable=True)
    commander_legal = Column(Boolean)
    standard_legal = Column(Boolean)
    modern_legal = Column(Boolean)
    pioneer_legal = Column(Boolean)
    pauper_legal = Column(Boolean)
    name = Column(String(250),nullable=False)
    reserved_list = Column(Boolean)
    
    
class CardFace(SQL_model_base):
    __tablename__ = 'card_faces'
    id = Column(Integer, primary_key=True)
    name = Column(String(250),nullable=False)
    mana_cost = Column(String(250),nullable=True)
    colors = Column(String(250),nullable=True)
    cmc = Column(String(250),nullable=True)
    color_identity = Column(String(250),nullable=True)
    type_line = Column(String(250),nullable=True)
    is_legendary = Column(Boolean)
    is_snow = Column(Boolean)
    main_type = Column(String(250),nullable=False)
    sub_type = Column(String(250),nullable=False)
    power = Column(String(250),nullable=True)
    toughness = Column(String(250),nullable=True)
    produced_mana = Column(String(250),nullable=True)
    key_words = Column(JSON,nullable=True)
    oracle_text = Column(Text)
    card =  Column(Integer,ForeignKey("cards.id"))
    

class Print(SQL_model_base):
    __tablename__ = 'prints'
    id = Column(Integer, primary_key=True)
    card = Column(Integer,ForeignKey("cards.id"))
    set = Column(Integer,ForeignKey("sets.id"))
    small_front_img = Column(String(250),nullable=True)
    normal_front_img = Column(String(250),nullable=True)
    small_back_img = Column(String(250),nullable=True)
    normal_back_img = Column(String(250),nullable=True)
    rarity = Column(String(50),nullable=True)
    reprint = Column(Boolean,nullable=False)

class SuggestedPrice(SQL_model_base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    print =  Column(Integer,ForeignKey("prints.id"))
    usd = Column(Float,nullable=True)
    eur = Column(Float,nullable=True)
    source = Column(String(250))
    is_foil = Column(Boolean)
    date = Column(DateTime,nullable=False,default=datetime.now())