import shutil, os, scrython, time, json
from unidecode import unidecode

# Download data
# Get list of cards from set
# Go through list of cards
# Basics, multiple arts
# Booster fun
# Set language, file name, path
# Download images

basics = [ 'Forest', 'Island', 'Mountain', 'Plains', 'Swamp', 'Wastes',
           'Snow-Covered Forest', 'Snow-Covered Island', 'Snow-Covered Mountain',
           'Snow-Covered Plains', 'Snow-Covered Swamp', 'Snow-Covered Wastes' ]
image_path = "E:\\Programming Projects\\Python\\Automatic-Eureka\\Testing Dump\\"


# Get the list of cards in the set from Scryfall
def get_set_cards(set_code,quiet):
    card_list = []
    query = '++e:' + set_code
    page_count = 1;
    card_count = 1;
    set_size = 1
    while(True):
        search = scrython.cards.Search(q=query, page=page_count, order="set")
        time.sleep(0.5)
        for card in search.data():
            card_list.append(card)
            card_count = card_count + 1
        if search.has_more():
            page_count = page_count + 1;
        if not search.has_more():
            print("")
            return card_list

# Used for console output of get_set_cards function.
def cards_remaining(set_size, page_count):
    if set_size > page_count * 175:
        return page_count * 175
    else:
        return set_size


def get_set(set_code):
    card_set = scrython.sets.Code(code=set_code)
    return card_set

# Grabs all the sets from Scrython, splits it into an enumerated list, and
# returns that list.
def get_sets_full():
    set_list = []
    sets = scrython.sets.Sets()
    sets = enumerate(sets.data())
    for c_set in sets:
        set_list.append(c_set[1])
    return set_list

# Filters the full list of sets to remove anything that is not a printed (paper)
# set of legal cards (ie: no tokens, oversized, inserts, etc)
def get_sets_filtered(set_list_full,filters):
    set_list_filtered = []
    set_types = []
    for c_set in set_list_full:
        match c_set["set_type"]:
            case "core":
                if filters[0]:
                    set_list_filtered.append(c_set)
            case "expansion":
                if filters[1]:
                    set_list_filtered.append(c_set)
            case "draft_innovation":
                if filters[2]:
                    set_list_filtered.append(c_set)
            case "commander":
                if filters[3]:
                    set_list_filtered.append(c_set)
            case "masters":
                if filters[4]:
                    set_list_filtered.append(c_set)
            case "arsenal":
                if filters[5]:
                    set_list_filtered.append(c_set)
            case "from_the_vault":
                if filters[6]:
                    set_list_filtered.append(c_set)
            case "spellbook":
                if filters[7]:
                    set_list_filtered.append(c_set)
            case "premium_deck":
                if filters[8]:
                    set_list_filtered.append(c_set)
            case "starter":
                if filters[9]:
                    set_list_filtered.append(c_set)
            case "box":
                if filters[10]:
                    set_list_filtered.append(c_set)
            case "planechase":
                if filters[11]:
                    set_list_filtered.append(c_set)
            case "archenemy":
                if filters[12]:
                    set_list_filtered.append(c_set)
            case "vanguard":
                if filters[13]:
                    set_list_filtered.append(c_set)
            case "funny":
                if filters[14]:
                    set_list_filtered.append(c_set)
            case "promo":
                if filters[15]:
                    set_list_filtered.append(c_set)
            case "token":
                if filters[16]:
                    set_list_filtered.append(c_set)
            case "memorabilia":
                if filters[17]:
                    set_list_filtered.append(c_set)
            case "minigame":
                if filters[18]:
                    set_list_filtered.append(c_set)
            case "alchemy":
                if filters[19]:
                    set_list_filtered.append(c_set)
            case "treasure_chest":
                if filters[20]:
                    set_list_filtered.append(c_set)
            case _:
                if not c_set["digital"]:
                    set_list_filtered.append(c_set)
    return set_list_filtered


def col_num_prefix(card):
    try:
        col_num = int(card["collector_number"])
        if col_num < 10:
            output = "00" + str(col_num)
        if col_num < 100:
            output = "0" + str(col_num)
        return output
    except ValueError:
        return card["collector_number"]

# Finds all languages for cards in the set based on if any card is printed in a language.
# card_list: a list of cards as generated by get_set_cards
# is_foil: boolean that checks for cards printed in a language as foil-only (eg: SNC buy-a-box)
def get_set_languages(card_list,is_foil):
    languages = []
    for card in card_list:
        card_lang = fix_lang(card["lang"])
        if card_lang not in languages:
            if is_foil:
                if not card["nonfoil"]:
                    languages.append(card_lang)
            else:
                if card["nonfoil"]:
                    languages.append(card_lang)
    return languages

# Fixes language string to match what path Magic Album looks for images at
def fix_lang(lang):
    match lang:
        case "en":
            return "ENG"
        case "de":
            return "GER"
        case "fr":
            return "FRA"
        case "it":
            return "ITA"
        case "ja":
            return "JPN"
        case "ko":
            return "KOR"
        case "pt":
            return "POR"
        case "es":
            return "SPA"
        case "ru":
            return "RUS"
        case "zhs":
            return "ZHC"
        case "zht":
            return "ZHT"
        case "ph":
            return "PHY"
        case _:
            return "ENG"
