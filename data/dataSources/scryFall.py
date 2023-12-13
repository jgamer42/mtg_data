import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import time
import threading
class ScryFall:
    def __init__(self):
        self.mined_pages = []
        self.url = 'https://api.scryfall.com'
        self.http = requests.Session()
        retries = Retry(
            total=20,
            backoff_factor=2,
        )
        self.http.mount('https://', HTTPAdapter(max_retries=retries))
        self.max_hard_retries = 3 
        self.hard_retries = 0
        
    def list_sets(self) -> dict:
        sets = self.http.get(f'{self.url}/sets')
        return sets.json()['data']

    def get_cards_from_set(self,set_code: str)->list:
        output = []
        self.mined_pages = []
        response = self.http.get(f"{self.url}/cards/search?include_extras=true&include_variations=true&q=set={set_code}")
        if response.status_code == 404:
            print("no encontro el set",set_code)
            raise ValueError
        elif response.status_code != 200:
            print("retry due scryfall, ", response.status_code)
            time.sleep(60)
            return self.get_cards_from_set(set_code)
            # raise ValueError("scrfyall fails")
        cards = response.json()
        output = cards["data"]
        thread_size = int((cards["total_cards"] // len(cards["data"]))//2)
        current_page = 2
        if thread_size > 1:
            threads = []
            url = f"{self.url}/cards/search?include_extras=true&include_variations=true&q=set={set_code}"
            for id in range(2):
                new_thread = threading.Thread(target=self.get_pagination_with_threads,args=(id,url,int(current_page),int(current_page+thread_size),output))
                current_page = current_page + thread_size + 1
                threads.append(new_thread)
                new_thread.start()
            for t in threads:
                t.join()            
        elif cards['has_more']:
            response = self.http.get(f"{self.url}/cards/search?include_extras=true&include_variations=true&q=set={set_code}&page={current_page}")
            cards = response.json()
            output += cards["data"]
            current_page += 1
            while True:
                response = self.http.get(f"{self.url}/cards/search?include_extras=true&include_variations=true&q=set={set_code}&page={current_page}")
                if response.status_code == 422:
                    break
                cards = response.json()
                output += cards["data"]
                current_page += 1
        return output
        

    def get_card_by_name(self, card_name: str):
        card = self.http.get(
            f'{self.url}/cards/search?q=name={card_name}&unique=prints')
        if card.status_code == 404:
            print(card_name,"No encontrada")
            return {}
        elif card.status_code != 200:
            print("fallo la request, hard retry",card.status_code,card_name)
            self.hard_retries += 1
            time.sleep(5)
            if self.hard_retries < self.max_hard_retries:
                return  self.get_card_by_name(card_name)
            else:
                output.close()
                return None
        cards = card.json()
        output = []
        self.hard_retries = 0
        if cards["total_cards"] > 1:
            for card in cards["data"]:
                if card_name.lower().strip() == card["name"].lower().strip():
                    output.append(card)
        else:
            output = cards["data"]
        return output
        
    
    def get_card_by_function(self,function:str):
        cards = self.http.get(
                f'{self.url}/cards/search?q=function={function}')
        if cards.status_code == 404:
            return None
        raw_response = cards.json()
        output = raw_response["data"]
        while raw_response["has_more"]:
            new_cards = requests.get(raw_response["next_page"])
            if new_cards.status_code > 299:
                break
            raw_response = new_cards.json()
            output += raw_response["data"]
        return output
    
    def get_pagination_with_threads(self,id,url:str,start_page:int,end_page:int,output:list):
        current_page = start_page
        response = self.http.get(f"{url}&page={current_page}")
        current_page += 1
        cards = response.json()
        try:
            output += cards["data"]
        except Exception as E:
            print(f"falle pagination",E)
            return ""
        while cards["has_more"] and current_page <= end_page:
            response = self.http.get(f"{url}&page={current_page}")
            cards = response.json()
            output += cards["data"]
            self.mined_pages.append(current_page)
            current_page += 1    