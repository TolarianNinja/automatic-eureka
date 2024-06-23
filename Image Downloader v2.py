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
            print("")
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
        if "extendedart" in card["frame_effects"]:
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

# Takes in the set / array of cards and returns an array of strings with fixed file names.
# Nested for loops are to find duplicate cards that would have the same file name.  This typically
# happens when there are multiple arts with the same frame (like basic lands).  Each card needs to
# see if there are any other copies in the list, and because that is accounting for different Booster Fun
# treatments its two birds one stone.
def build_file_names(card_list):
    card_names = []
    for top_card in card_list:
        top_name = unidecode(fix_characters(top_card) + card_style(top_card))
        card_count = 1
        dup_found = False
        for bottom_card in card_list:
            bottom_name = unidecode(bottom_card["name"] + card_style(bottom_card))
            if top_name == bottom_name and top_card["collector_number"] != bottom_card["collector_number"]:
                dup_found = True
                if top_card["collector_number"] > bottom_card["collector_number"]:
                    card_count = card_count + 1
        if dup_found:
            top_name = top_name + " [" + str(card_count) + "]"
        card_names.append(top_name)
    for name in card_names:
        print(name)
    bad_files = validate_file_names(card_list, card_names)
    return card_names

# Checks that the file names line up with the cards in order
def validate_file_names(card_list, card_names):
    bad_file_names = []
    current_name = ""
    i = 0
    while i < len(card_list):
        current_name = fix_characters(card_list[i]) + card_style(card_list[i])
        if current_name not in card_names[i]:
            bad_file_names.append(card_names[i])
        i = i + 1
    if len(bad_file_names) > 0:
        print("There has been an error!")
    return bad_file_names
        
        
def get_card_console(card):
    card_name = build_filename(card)
    print("Card Name: " + card_name)

def get_set_console(set_code):
    card_set = scrython.sets.Code(code=set_code)
    print("Set Name: " + card_set.name() + "\nSet Code: " + card_set.code() + "\nRelease Date: " + str(card_set.released_at()) +
          "\nNumber of Cards: " + str(card_set.card_count()) + "\n")
    card_list = get_set_cards(set_code)
    not_basic = 0
    for card in card_list:
        dupes = find_dupes(card,card_list)
        if len(dupes) > 0:
            if "Basic" not in card["type_line"]:
                not_basic = not_basic + 1
                print(str(build_filename(card)) + str(find_dupes(card,card_list)))
    if not_basic > 0:
        print("\nThere were " + str(not_basic) + " duplicate card names that were not basic lands.")
    
#get_set_console("woe")
build_file_names(get_set_cards("woe"))
