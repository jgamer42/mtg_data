import os
import sys
from dotenv import load_dotenv
load_dotenv() 
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from databases import SQL_model_base


class Tournament(SQL_model_base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True)
    format = Column(String(250),nullable=False)
    name = Column(String(250),nullable=False)
    date = Column(DateTime,nullable=False)
    source = Column(String(250),nullable=False)
    link = Column(String(250),nullable=False)
    
class Deck(SQL_model_base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True)
    format = Column(String(250),nullable=False)
    name = Column(String(250),nullable=False)
    player = Column(String(250),nullable=False)
    
    
class DeckCard(SQL_model_base):
    __tablename__ = 'card_deck'
    id = Column(Integer, primary_key=True)
    deck = Column(Integer,ForeignKey("decks.id"))
    card = Column(Integer,ForeignKey("cards.id"))
    quantity = Column(Integer,nullable=False)

class Standings(SQL_model_base):
    __tablename__ = 'standings'
    id = Column(Integer, primary_key=True)
    place = Column(String(10), nullable=False)
    deck = Column(Integer,ForeignKey("decks.id"))
    tournament = Column(Integer,ForeignKey("tournaments.id"))