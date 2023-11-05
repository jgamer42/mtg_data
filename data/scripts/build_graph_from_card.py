import requests
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}/data')
from dataSources import ScryFall


mined_cards = {}
scryfall = ScryFall()

MAP_RELATION_COLORS = {
    "SIMILAR_TO":"blue",
    "WORSE_THAN":"green",
    "BETTER_THAN":"red",
    "MIRRORS":"blue"
}

MAX_DEEP = 2
def get_tag_information(card_set,card_collector_id):
    global scryfall, mined_cards
    url = "https://tagger.scryfall.com/graphql"
    body ={
    "query": "query FetchCard($set:String! $number:String! $back:Boolean=false $moderatorView:Boolean=false){card:cardBySet(set:$set number:$number back:$back){...CardAttrs backside layout scryfallUrl sideNames twoSided rotatedLayout taggings(moderatorView:$moderatorView){...TaggingAttrs tag{...TagAttrs ancestorTags{...TagAttrs}}}relationships(moderatorView:$moderatorView){...RelationshipAttrs}}}fragment CardAttrs on Card{artImageUrl backside cardImageUrl collectorNumber id illustrationId name oracleId printingId set}fragment RelationshipAttrs on Relationship{classifier classifierInverse annotation subjectId subjectName createdAt creatorId foreignKey id name pendingRevisions relatedId relatedName status type}fragment TagAttrs on Tag{category createdAt creatorId id name namespace pendingRevisions slug status type}fragment TaggingAttrs on Tagging{annotation subjectId createdAt creatorId foreignKey id pendingRevisions type status weight}",
    "operationName": "FetchCard",
    "variables": {
        "set": card_set,
        "number": card_collector_id
    }
    }
    headers = {
        "Cookie":"_scryfall_tagger_session=ft9FbKdT%2F%2FKXp8jr6Go7jntXdc%2B%2BLme78yT77Cpkd87fjuYAo7dTOJtmY2ayzaKVkapzSIyI68xksbtXHu3gXRTlcZoy151k1A1rmKgvulTlPrZl4%2B1IsoXDwEsNChHjIvgCNNT5cTPsvJnsVNdmmaB9krniYMVU3MJC9oM9AacNz6xaTcNhZktrPJxhcHRnDGU79Ql1DfXH1chUTLebd6MmBQtwSpalhKouJSWenN6hUSnz9F4fpzkG%2B%2Bf1sTxT%2BlrGCGwvxZEHn9W7pu2N%2F0yCSZT0ISrd5wKIM4W5m%2BY%3D--VUaCLw291WvHbAYO--h8iNZN%2FjYKKL13C2da80jA%3D%3D",
        "X-Csrf-Token":"ovexdyUgo3d1fUs-PHol4JVydRHPCl5B4nGqcH6GDsUvE2R8zNDFeohRggHD1_ijFz-N5Z_5xan7nsQ9VvLXrQ"
    }
    data = requests.post(url,json=body,headers=headers)
    raw_data = data.json()["data"]["card"]
    return raw_data

def add_card_to_graph_dict(card_name:str,target_graph:dict,deep):
    try:
        card_info = scryfall.get_card_by_name(card_name)[0]
    except KeyError:
        return 
    tag_info = get_tag_information(card_info["set"],card_info["collector_number"])
    mined_cards[card_info["name"]] = card_info
    print(f"Mining {card_info['name']}")
    if card_info["name"] not in target_graph["nodes"]:
        target_graph["nodes"].append(card_info["name"])
        target_graph["structure"][card_info["name"]] = []
        target_graph["meta"][card_info["name"]] = []
        
    for related_card in tag_info["relationships"]:
        if related_card["classifier"] in ["DEPICTED_IN","DEPICTS","WITH_BODY","WITHOUT_BODY","COLORSHIFTED","REFERENCES_TO","REFERENCES_BY","RELATED_TO","COMES_BEFORE","COMES_AFTER"]:
            continue
        
        if related_card["subjectName"] not in target_graph["nodes"]:
            target_graph["nodes"].append(related_card["subjectName"])
            target_graph["structure"][related_card["subjectName"]] = []
            target_graph["meta"][related_card["subjectName"]] = []
            
        target_graph["structure"][related_card["subjectName"]].append(related_card["name"])
        target_graph["meta"][related_card["subjectName"]].append({"relation_color":MAP_RELATION_COLORS.get(related_card["classifier"],"gray")})
        if deep <= MAX_DEEP:
            if related_card["subjectName"] not in mined_cards.keys() and related_card["subjectName"] != card_name:
                add_card_to_graph_dict(related_card["subjectName"],target_graph,deep+1)
            if related_card["name"] not in mined_cards.keys() and related_card["name"] != card_name:
                add_card_to_graph_dict(related_card["name"],target_graph,deep+1)
        
            
            
target_graph = {
    "structure":{},
    "meta":{},
    "nodes":[]
}

add_card_to_graph_dict("ponder",target_graph,0)



G = nx.DiGraph()
G.add_nodes_from(target_graph["nodes"])
colors = []
for node in target_graph["structure"].keys():
    for i,edge in enumerate(target_graph["structure"][node]):
        colors.append(target_graph["meta"][node][i]["relation_color"])
        G.add_edge(node,edge)
nx.draw_networkx(G,edge_color=colors)
plt.show()
