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
def get_sets_filtered(set_list_full):
    set_list_filtered = []
    #set_list_full = get_sets_full()
    set_types = []
    for c_set in set_list_full:
        match c_set["set_type"]:
            case "memorabilia":
                continue
            case "minigame":
                continue
            case "token":
                continue
            case "planechase":
                continue
            case "vanguard":
                continue
            case "archenemy":
                continue
            case _:
                if not c_set["digital"]:
                    set_list_filtered.append(c_set)
    return set_list_filtered

# Used for console output of get_set_cards function.
def cards_remaining(set_size, page_count):
    if set_size > page_count * 175:
        return page_count * 175
    else:
        return set_size

# Check if the card is a style other than the standard printing
def card_style(card):
    card_style = ""
    if "sld" in card["set"]:
        card_style = col_num_prefix(card)
    else:
        try:
            if "surgefoil" in card["promo_types"]:
                card_style = "Surge"
            if "showcase" in card["frame_effects"]:
                card_style = "Showcase"
            if "borderless" in card["border_color"] and "showcase" not in card["frame_effects"]:
                card_style = "Alt Art"
            if "1997" in card["frame"] and "boosterfun" in card["promo_types"]:
                card_style = "Retro"
            if "stepandcompleat" in card["promo_types"]:
                card_style = "Compleat"
            if "confettifoil" in card["promo_types"]:
                card_style = "Confetti"
            if "dossier" in card["promo_types"]:
                card_style = "Dossier"
            if "embossed" in card["promo_types"]:
                card_style = "Embossed"
            if "etched" in card["frame_effects"]:
                card_style = "Etched"
            if "galaxyfoil" in card["promo_types"]:
                card_style = "Galaxy Foil"
            if "gilded" in card["promo_types"]:
                card_style = "Gilded"
            if "halofoil" in card["promo_types"]:
                card_style = "Halo"
            if "invisibleink" in card["promo_types"]:
                card_style = "Invisible Ink"
            if "magnified" in card["promo_types"]:
                card_style = "Magnified"
            if "oilslick" in card["promo_types"]:
                card_style = "Oil"
            if "rainbowfoil" in card["promo_types"]:
                card_style = "Rainbow"
            if "textured" in card["promo_types"]:
                card_style = "Textured"
            if card["promo"]:
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

def is_retro_style(card):
    if "1997" in card["frame"]:
        if "draft_innovation" in card["set_type"] or "masters" in card["set_type"]:
            print("Card Name: " + card["name"] + " Number: " + card["collector_number"])
            return True
        else:
            return False
    else:
        return False

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

# Cleans up set names to replace colon with space+hyphen
def fix_set_name(name):
    set_name = name
    if ":" in set_name:
        set_name = str(name).replace(":", " -")
    return set_name

# Takes in the set / array of cards and returns an array of strings with fixed file names.
# Nested for loops are to find duplicate cards that would have the same file name.  This typically
# happens when there are multiple arts with the same frame (like basic lands).  Each card needs to
# see if there are any other copies in the list, and because that is accounting for different Booster Fun
# treatments its two birds one stone.  This does not account for DFCs.
def build_file_names(card_list):
    card_names = []
    for card in card_list:
        if 'z' in card["collector_number"]:
            continue
        card_name = fix_characters(card) + card_style(card)
        card_dupes = find_dupes(card,card_list)
        #print("Card Name: " + card_name + " Dupes: " + str(card_dupes))
        if card_dupes > 0:
            card_name = card_name + " [" + str(card_dupes) + "]"
        card_names.append(card_name)
    for name in card_names:
        print(name)
    #bad_files = validate_file_names(card_list, card_names)
    return card_names

# Finds 
def find_dupes(card,card_list):
    card_count = 1
    dup_found = False
    if 'z' in card["collector_number"]:
        return 0
    card_name = fix_characters(card) + card_style(card)
    for loop_card in card_list:
        if 'z' in loop_card["collector_number"]:
            continue
        loop_name = fix_characters(loop_card) + card_style(loop_card)
        if card_name == loop_name and card["collector_number"] != loop_card["collector_number"]:
            dup_found = True
            if int(card["collector_number"]) > int(loop_card["collector_number"]):
                card_count = card_count + 1
    if dup_found:
        return card_count
    else:
        return 0
    
            

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

# Creates every folder needed for the set, considering all languages / foil only.
# card_set: set object, contains all set data.
def build_folders(card_set):
    set_name = fix_set_name(card_set.name())
    main_path = image_path + set_name + "\\"
    card_list = get_set_cards(card_set.code())
    langs = get_set_languages(card_list,False)
    langs_foil = get_set_languages(card_list,True)
    os.makedirs(main_path,511,True)
    os.chdir(main_path)
    for lang in langs:
        lang_path = main_path + lang + "\\"
        os.makedirs(lang_path,511,True)
        print("Created " + lang_path)
    for lang in langs_foil:
        lang_path = main_path + lang + " FOIL\\"
        os.makedirs(lang_path,511,True)
        print("Created " + lang_path)

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
        
def get_card_console(card):
    card_name = build_filename(card)
    print("Card Name: " + card_name)

def get_set_console(set_code):
    card_set = scrython.sets.Code(code=set_code)
    print("Set Name: " + card_set.name() + "\nSet Code: " + card_set.code() + "\nRelease Date: " + str(card_set.released_at()) +
          "\nSet Type: " + card_set.set_type() + "\nNumber of Cards: " + str(card_set.card_count()) + "\n")
    card_list = get_set_cards(set_code)
    not_basic = 0

def get_properties_all_cards():
    sets = get_sets_full()
    promo_types = []
    frame_effects = []
    border_color = []
    for c_set in sets:
        if c_set["card_count"] < 1:
            continue
        card_list = get_set_cards(c_set["code"])
        print("Set: " + c_set["code"])
        for card in card_list:
            try:
                for p_type in card["promo_types"]:
                    if p_type not in promo_types:
                        promo_types.append(p_type)
            except KeyError:
                pass
            try:
                for f_effect in card["frame_effects"]:
                    if f_effect not in frame_effects:
                        frame_effects.append(f_effect)
            except KeyError:
                pass
            try:
                for b_color in card["border_color"]:
                    if b_color not in border_color:
                        border_color.append(b_color)
            except KeyError:
                pass
    print("Promo Types: " + str(promo_types) + " Frame Effects: " + str(frame_effects)
          + " Border Colors: " + str(border_color))

        

#get_set_console("h2r")
#build_file_names(get_set_cards("ltr"))
#get_set("snc")
#print(get_languages(get_set_cards("snc"),True))
#download_images(get_set("snc"))
#build_folders(get_set("snc"))
#sets = get_sets_full()
#for c_set in sets:
#    print(c_set)
#get_properties_all_cards()
#get_sets_filtered()
