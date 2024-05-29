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

duplicate_counts = []

# Get the list of cards in the set from Scryfall
def get_set_cards(set_code):
    card_list = []
    query = '++e:' + set_code
    page_count = 1;
    card_count = 1;
    set_size = 1
    while(True):
        search = scrython.cards.Search(q=query, page=page_count, order="set")
        print("Processing cards " + str(card_count) + " to " + str(cards_remaining(search.total_cards(), page_count)) + "...")
        time.sleep(0.5)
        for card in search.data():
            card_list.append(card)
            card_count = card_count + 1
        if search.has_more():
            page_count = page_count + 1;
        if not search.has_more():
            return card_list

# Used for console output of get_set_cards function.
def cards_remaining(set_size, page_count):
    if set_size > page_count * 175:
        return page_count * 175
    else:
        return set_size

# Check if the card is a style other than the standard printing
def card_style(card):
    card_style = ""
    try:
        if "surgefoil" in card["promo_types"]:
            card_style = "Surge"
        if "showcase" in card["frame_effects"]:
            card_style = "Showcase"
        if "borderless" in card["border_color"] and "showcase" not in card["frame_effects"]:
            card_style = "Borderless"
        if card["promo"]:
            #print("This is a promo of " + str(card["promo_types"]) + " types.")
            if "prerelease" in card["promo_types"]:
                card_style = "S"
            elif "stamped" in card["promo_types"]:
                card_style = "P"
            elif "promopack" in card["promo_types"] or "bundle" in card["promo_types"]:
                card_style = "Promo"
        elif "extendedart" in card["frame_effects"]:
            card_style = "Ext Art"
        if len(card_style) > 0:
            card_style = " [" + card_style + "]"
        return card_style
    except KeyError:
        return card_style

# Cleans up characters that would cause an issue as a file name
def fix_characters(card):
    current_file = card["name"]
    if "//" in current_file:
        current_file = str(card["name"]).replace(" // ", "_")
    if "\"" in current_file:
        current_file = str(card["name"]).replace("\"", "")
    if ":" in current_file:
        current_file = str(card["name"]).replace(":", "")
    if "?" in current_file:
        current_file = str(card["name"]).replace("?", "")
    current_file = unidecode(current_file)
    return current_file

# 
def build_filename(card):
    c_name = fix_characters(card)
    dup_count = 0 #basic_check(card)
    c_style = card_style(card)
    return c_name + c_style
"""
    if dup_count > 0:
        return c_name + " [" + str(dup_count) + "]"
    if len(c_style) != 0:
        return c_name + " [" + c_style + "]"
    return c_name
"""

def find_duplicates(card_list):
    for top_card in card_list:
        top_name = unidecode(top_card["name"] + card_style(top_card))
        card_count = 1
        for bottom_card in card_list:
            bottom_name = unidecode(bottom_card["name"] + card_style(bottom_card))
            if top_name == bottom_name and top_card["collector_number"] > bottom_card["collector_number"]:
                card_count = card_count + 1
                print("Top Name: " + top_name + " Top Num: " + str(top_card["collector_number"]) +
                      " Bottom Name: " + bottom_name + " Bottom Num: " + str(bottom_card["collector_number"]) + "Count: " + str(card_count))

"""
#
def basic_check(card):
    dup_count = 0
    for name, count in duplicate_counts:
        if name in card["name"]:
            duplicate_counts.update(name,count = count + 1)
            return count
    return dup_count

#
def build_dupes():
    for name in basics:
        duplicate_counts.append((name,0))
    print(duplicate_counts)
"""

def get_card_console(card):
    card_name = build_filename(card)
    print("Card Name: " + card_name)

def get_set_console(set_code):
    card_set = scrython.sets.Code(code=set_code)
    print("Set Name: " + card_set.name() + "\nSet Code: " + card_set.code() + "\nRelease Date: " + str(card_set.released_at()) +
          "\nNumber of Cards: " + str(card_set.card_count()) + "\n")
    card_list = get_set_cards(set_code)
    for card in card_list:
        get_card_console(card)

#get_set_console("pwoe")
find_duplicates(get_set_cards("woe"))
