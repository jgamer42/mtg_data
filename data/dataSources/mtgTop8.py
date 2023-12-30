import scrapy
from lxml import html
import logging
logging.basicConfig(filename="scrapper.log",level=logging.DEBUG)
import requests
class MtgTop8(scrapy.Spider):
    """
    Spider used to retrieve data from mtg top 8 decks tournaments information
    """

    name: str = "mtg_top8_decks_events"
    custom_settings: dict = {"ROBOTSTXT_OBEY": False, "CONCURRENT_REQUESTS": 1000}
    formats_helper: dict = {
        "standard": "ST",
        "pioneer": "PI",
        "modern": "MO",
        "pauper": "PAU",
        "legacy": "LE",
        "vintage": "VI",
        "explorer":"EXP",
        "commander":"cEDH"
    }
    memory: list = []
    aux = ""
    base_url: str = "https://mtgtop8.com"

    def __init__(self, format: str, *args, **kwargs):
        """
        Constructor of the object
        :param format: Is a str with the format to scrape
        """
        super(MtgTop8, self).__init__(*args, **kwargs)
        normalized_format: str = self.formats_helper.get(format, "")
        self.format = format
        self.start_urls: list = [f"{self.base_url}/format?f={normalized_format}"]
        self.data = {}
        self.commander = None

    def parse(self, response):
        """
        Start of the scraper
        """
        tournaments: list = list(
            set(response.xpath("//td[@width='70%']/a").getall())
        )
        for tournament in tournaments:
            tournament_loaded = html.fromstring(tournament)
            url =  tournament_loaded.xpath("@href")[0]
            name = tournament_loaded.xpath("text()")[0]
            tournament_url: str = f"{self.base_url}/{url}"
            self.aux = tournament_url
            tournament_base_info = {
                "link":tournament_url,
                "name":name,
                "format":self.format,
                "decks":[]
            }
            yield response.follow(url=tournament_url, callback=self.tournaments,cb_kwargs={"tournament":tournament_base_info})

    def tournaments(self, response,tournament:dict):
        """
        Function to retrieve a list of tournaments links
        :param response: Response object with the page information
        :return: A generator with the decks information
        """
        decks = response.xpath("//div[@class='hover_tr'] | //div[@class='chosen_tr'] ").getall()
        date = response.xpath('//div[@style="margin-bottom:5px;"]/text()').getall()
        tournament["date"] = date[0]
        tournament["expected_decks"] = len(decks)
        for deck in decks:
            try:
                deck_loaded = html.fromstring(deck)
                deck_link: str = deck_loaded.xpath("div/div[3]/div[1]/a/@href")[0]
                link: str = f"{self.base_url}/event{deck_link}"
                deck_name: str = deck_loaded.xpath("div/div[3]/div[1]/a/text()")[0]
                player_name: str = deck_loaded.xpath("div/div[3]/div[2]/a/text()")[0]
                standings: str = deck_loaded.xpath("div/div[1]/text()")[0]
                self.deck_name = deck_name
                response = requests.get(link)
                deck_response = html.fromstring(response.text)
                if self.format == 'commander':
                    commander = self.get_commander(deck_response)
                    self.commander = commander
                else:
                    commander = None
                    self.commander = None
                card_list = self.decks(deck_response)
                target_deck = {"name":deck_name,"card_list":card_list,"player_name":player_name,"standings":standings,"commander":commander}
                tournament["decks"].append(target_deck)
                yield tournament
            except Exception as e:
                logging.error(f"Toteo {self.base_url}/event{deck_link} , {e}")
                
    def decks(self, response):
        """
        Function to retrieve the decks information
        :param response: Response object with the page information
        :param deck_name: A str with the name of the deck
        :return deck: dict with the deck information
        """
    
        output_cards = []
        cards = response.xpath(
            "//div[position()]/div[@class='deck_line hover_tr']"
        )
        for card in cards:
            aux_card = html.fromstring(html.tostring(card).decode("utf-8"))
            c = self.process_card(aux_card)
            if self.format == 'commander' and c["name"] in self.commander:
                continue
            output_cards.append(c)
        return output_cards

    def get_commander(self,response):
        possible_commander = response.xpath("//div[contains(text(),'COMMANDER')]/following-sibling::div/span/text()")
        if "+" in self.deck_name:
            possible_commander = possible_commander[:2]
        else:
            possible_commander = [possible_commander[0]]
        return possible_commander
    
    def process_card(self, raw_card: str):
        """
        Function to retrieve card information
        :param raw_card: A str with the raw html with the card information
        :return card: dict with the card information
        """
        card_name: str = raw_card.xpath("//span/text()")[0]
        quantity: str = raw_card.xpath("//div/text()")[0]
        card: dict = {"name": str(card_name), "quantity": str(quantity).strip()}
        return card