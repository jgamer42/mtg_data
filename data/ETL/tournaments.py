import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from data.dataSources import MtgTop8
import logging
from databases.SQL import models as SQL_model
from databases import SQL_database
from databases.cache import cache_db
import datetime
from constants import BASIC_LANDS
logging.getLogger("scrapy").propagate = False
logging.getLogger("filelock").propagate = False
logging.getLogger("urllib3.connectionpool").propagate = False
logging.getLogger("telethon.extensions.messagepacker").propagate = False
logging.getLogger("telethon.network.mtprotosender").propagate = False

def clean_date(date:str):
    target_date = date
    if "-" in date:
        target_date = date.split("-")[-1].strip()
    return datetime.datetime.strptime(target_date,"%d/%m/%y")
decks_to_insert = []
standings_map = []
cards_to_insert = []
logging.basicConfig(filename="scrapper.log",level=logging.DEBUG)
def handle_data(item:dict):
    global decks_to_insert
    global standings_map
    tournament_information = {
        "source":"mtgTop8",
        "link":item["link"].strip(),
        "date":clean_date(item["date"]),
        "name":item["name"].strip(),
        "format":item["format"]
    }
    if len(item["decks"]) != item["expected_decks"]:
        return 
    possible_tournament = SQL_database.query(SQL_model.Tournament.id).filter(SQL_model.Tournament.link == item["link"])
    if SQL_database.query(possible_tournament.exists()).scalar():
        return 
    target_tournament = SQL_model.Tournament(**tournament_information)
    SQL_database.add(target_tournament)
    SQL_database.commit()
    for deck in item["decks"]:
        deck_base_info = {
            "format":item["format"],
            "player":deck["player_name"].strip(),        
            "name":deck["name"].strip()
        }
        decks_to_insert.append(SQL_model.Deck(**deck_base_info))
        deck_name = f'{deck_base_info["name"]}****{deck_base_info["player"]}'
        standings_map.append({"deck":deck_name,"tournament":target_tournament.id,"place":deck["standings"].strip()})
        for card in deck["card_list"]:
            card_name = " ".join([c.strip()for c in card["name"].strip().split()])
            if card_name.lower() in BASIC_LANDS:
                continue
            card_id = cache_db.get(card_name)
            if card_id is None:
                main_card = SQL_database.query(SQL_model.Card.id).filter(SQL_model.Card.name == card_name)
                if main_card.count() == 0:
                    main_card = SQL_database.query(SQL_model.Card.id).filter(SQL_model.Card.name.like(f"{card_name}%")).all()    
                try:
                    card_id = main_card[0][0]
                except:
                    main_card = SQL_database.query(SQL_model.Card.id).filter(SQL_model.Card.name.like(f"{card_name.split('/')[0]}%{card_name.split('/')[1]}")).all()    
                    card_id = main_card[0][0]
                cache_db.set(card_name,card_id)
            card_information = {
                "deck":deck_name,
                "card":card_id,
                "quantity":card["quantity"]
            }
            cards_to_insert.append(card_information)
                    


                
        
process = CrawlerProcess()
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="standard")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="pioneer")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="modern")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="pauper")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="legacy")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="vintage")
crawler = Crawler(MtgTop8)
crawler.signals.connect(
    handle_data, signal=signals.item_scraped
)
process.crawl(crawler, format="explorer")
process.start()

SQL_database.bulk_save_objects(decks_to_insert)
SQL_database.commit()
clean_cards = []
for card in cards_to_insert:
    deck_id = cache_db.get(card["deck"])
    if deck_id is None:
        name,player = card["deck"].split("****")
        deck_id = SQL_database.query(SQL_model.Deck.id).filter(SQL_model.Deck.name == name and SQL_model.Deck.player == player ).all()
        deck_id = deck_id[0][0]
        cache_db.set(card["deck"],deck_id)
    target_card = {
        "deck":deck_id,
        "quantity":card["quantity"],
        "card":card["card"]
    }
    clean_cards.append(SQL_model.DeckCard(**target_card))
SQL_database.bulk_save_objects(clean_cards)
SQL_database.commit()    
clean_standings = []
for standing in standings_map:
    deck_id = cache_db.get(standing["deck"])
    clean_standings.append(SQL_model.Standings(**{"deck":deck_id,"tournament":standing["tournament"],"place":standing["place"]}))

SQL_database.bulk_save_objects(clean_standings)
SQL_database.commit()