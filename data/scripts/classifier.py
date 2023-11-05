import os
import sys
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(f'{os.environ["PROJECT_PATH"]}')
from data.dataSources import ScryFall
from utils.domain import clean_colors,clean_type

source = ScryFall()
possible_classifications = ["removal","ramp","cantrip","counter","burn","draw","discard","tutor","reanimate","manadork"]#"wincondition"]
processed_cards = {}


for classification in possible_classifications:
    raw_cards = source.get_card_by_function(classification)
    clean_cards = []
    for card in raw_cards:
        if "oracle_text" not in card.keys() and "card_faces" in card.keys():
            oracle_text = ""
            for face in card["card_faces"]:
                oracle_text += face["oracle_text"]
        else:
            oracle_text = card["oracle_text"]
        clean_card = {
            "name":card["name"],
            "cmc":card["cmc"],
            "colors":clean_colors(card.get("colors",card["color_identity"])) if clean_colors(card.get("colors",card["color_identity"])) != "" else "colorless",
            "keywords":card["keywords"],
            "text":oracle_text,
            "type":clean_type(card["type_line"])
        }
        clean_cards.append(clean_card)
    processed_cards[classification] = clean_cards
    
classifier = {}
keywords_space = ['Defender', 'Assist', 'Prince of Chaos', 'Gatling Blaster', 'Spore Chimney', 'Psychic Abomination', 'Augment', 'Bestow', 'Desertwalk', 'Wizardcycling', 'Aim for the Wyvern', 'Scry', 'Raid', 'Encore', 'Epic', 'Eminence', 'Daybound', 'Treasure', 'Seek', 'Bloodthirst', 'Double agenda', 'Molting Exoskeleton', "Council's dilemma", 'Psychic Stimulus', 'Infect', 'Morph', 'Transmute', 'Sorcerous Inspiration', 'Multikicker', 'Riot', 'Unquestionable Wisdom', 'Typecycling', 'Addendum', 'Wild Shape', 'Sleight of Hand', 'More Than Meets the Eye', 'Wraith Form', 'Coruscating Flames', 'Investigate', 'Delve', 'Infesting Spores', 'Renown', 'Afterlife', 'Fateseal', 'Lieutenant', 'Offering', 'Overload', 'Hire a Mercenary', 'Mold Earth', 'Annihilator', 'Echo', 'Channel', 'Disturb', 'Enrage', 'Venture into the dungeon', 'Fight', 'Prowl', 'Persist', 'Formidable', 'Forecast', 'Emerge', 'Intimidate', 'Loud Ruckus', 'Hellbent', 'Crown of Madness', 'Ascend', 'Sunburst', 'Tempting offer', 'Open an Attraction', 'Terror from the Deep', 'Extort', 'Exile Cannon', 'Prototype', 'Rites of Banishment', 'Metalcraft', 'Banding', 'Goad', 'Proliferate', "Calim's Breath", 'Dash', 'Devour', 'Assemble', 'Enchant', 'Blitz', 'Living weapon', 'Ravenous', 'First strike', 'Endless Swarm', 'Sweep', 'Scavenge', 'Sigil of Corruption', 'Kicker', 'Ward', 'Improvise', 'Mutate', 'Devoid', 'Genomic Enhancement', 'Unleash', 'Casualty', 'Matter Absorption', 'Squad', 'Warp Vortex', 'Living metal', 'Heavy Power Hammer', 'Heavy Rock Cutter', 'Fateful hour', 'Transform', 'Warp Blast', 'Blood Drain', 'Pray for Protection', 'Keen Sight', 'Islandcycling', 'Vigilance', 'Buy Information', 'Basic landcycling', 'Evolve', 'Delirium', 'Convert', 'Haste', 'Landwalk', 'Transdimensional Scout', 'Pack tactics', 'Ninjutsu', 'Bolster', 'Embalm', 'Grandeur', 'Manifest', 'Hunt for Heresy', 'Provoke', 'Dethrone', 'Chroma', 'Cumulative upkeep', 'Heroic', 'Lord of the Pyrrhian Legions', 'Fire of Tzeentch', 'Islandwalk', 'Weird Insight', 'For Mirrodin!', 'Partner', 'Spell mastery', 'Enlist', 'Indestructible', 'Incubate', 'Monstrosity', 'Strive', 'Myriad', 'Awaken', 'Undaunted', 'Escalate', 'Splice', 'Amass', 'Roll to Visit Your Attractions', 'Prowess', 'Jump-start', 'Domain', 'Transfigure', 'Scorching Ray', 'Madness', 'Populate', 'Architect of Deception', 'Secrets of the Soul', "Bigby's Hand", 'Sell Contraband', 'Evoke', 'Fading', 'Aim for the Cursed Amulet', 'Lord of Torment', 'Strike a Deal', 'Nightbound', 'Compleated', 'Hyperfrag Round', 'The Betrayer', 'Swampwalk', 'Devouring Monster', 'Dynastic Advisor', 'Flanking', 'Shroud', 'Ruinous Ascension', 'Haunt', 'Chapter Master', 'Fuse', 'Menace', 'Escape', 'Spiked Retribution', 'Reconfigure', 'Spiritual Leader', 'Will of the council', 'Specialize', 'Cipher', 'Companion', 'Skulk', 'Grav-cannon', 'Multi-threat Eliminator', 'Spear of the Void Dragon', 'Rebound', 'Threshold', 'Converge', 'Shieldwall', 'Champion', 'Double strike', 'Trample', 'Armour of Shrieking Souls', 'Inspired', 'Soulbond', 'Corrupted', 'Death Ray', 'Modular', 'Fear', 'Intensity', 'Vanguard Species', 'Melee', 'Crew', 'Brood Telepathy', 'Surveil', 'Battalion', 'Cycling', 'Coven', 'Echo of the First Murder', 'Concealed Position', 'Magecraft', 'Surge', 'Command Protocols', 'Foretell', 'Landfall', 'Rapacious Hunger', 'Forestwalk', 'Bio-plasmic Barrage', 'Backup', 'Shadow', 'Clash', 'Plainscycling', 'Cleave', 'Bribe the Guards', 'Project Image', 'Devour Intellect', 'Leading from the Front', 'Rapid-fire Battle Cannon', 'Undying', 'Master Tactician', 'Medicus Ministorum', 'Arcane Life-support', 'Dynastic Codes', 'Constellation', 'Suspend', 'Bushido', 'Entwine', 'Toxic', 'Lifelink', 'Mentor', 'Demonstrate', 'Sonic Blaster', 'Graft', 'Slivercycling', 'Flash', 'Join forces', 'Boast', 'Changeling', 'Reinforce', 'Phalanx Commander', 'Detain', 'Healing Tears', 'Mill', 'Bio-Plasmic Scream', 'Symphony of Pain', 'Affinity', 'Alliance', 'Benediction of the Omnissiah', 'Phasing', 'Imprint', 'Wither', 'Protection', 'Flashback', 'Body Thief', 'Split second', 'Explore', 'Level Up', 'Mantle of Inspiration', 'Conjure', 'Animate Chains', 'Food', 'Secret council', 'Adamant', 'Undergrowth', 'Kinship', 'Disintegration Ray', 'Void Shields', 'Curse of the Walking Pox', 'Exalted', 'Deathtouch', 'Unearth', 'Rapid Regeneration', 'Ferocious', 'Flying', 'Hideaway', 'Morbid', "Hero's Reward", 'Retrace', 'Friends forever', 'Berzerker', 'Cascade', 'Fabricator Claw Array', 'Connive', 'Parley', 'Field Reprogramming', 'Exert', 'Soulshift', 'Plainswalk', 'The Seven-fold Chant', 'Exploit', 'Gust of Wind', 'Threaten the Merchant', 'Replicate', 'Reach', 'Forestcycling', 'Swampcycling', 'Enmitic Exterminator', 'Frenzied Rampage', 'Summary Execution', 'Dredge', 'Buyback', 'Daemon Sword', 'Hidden agenda', 'Three Autostubs', 'Conspire', 'Amplify', 'Support', 'Spectacle', 'Read Ahead', 'Aftermath', 'Convoke', 'Polymorphine', 'Synaptic Disintegrator', 'Xenos Cunning', 'Storm', 'Skilled Outrider', 'Ripple', 'Blood Chalice', 'Radiance', 'Executioner Round', 'Horsemanship', 'Tribute', 'Equip', 'Vanishing', 'Cohort', 'Death Frenzy', 'Atomic Transmutation', 'Rogue Trader', 'Miracle', 'Fire a Warning Shot', 'Training', 'Megamorph', 'Recover', 'Mountaincycling', 'Eternalize', 'Martyrdom', 'Landcycling', 'Ingest', 'Totem armor', 'Afflict', 'A Thousand Souls Die Every Day', 'Adapt', 'Hexproof', 'Repair Barge', 'Hexproof from', 'Revolt', 'Learn', 'Partner with'] 
for classification in possible_classifications:
    aux_names = []
    review_cards =[]
    for card in processed_cards[classification]:
        if card["name"] in aux_names:
            continue
        review_cards.append(card)
        aux_names.append(card["name"])
    classifier[classification] = review_cards


