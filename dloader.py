import shutil, os, scrython, requests
from unidecode import unidecode

def card_style(card):
    card_style = ""
    try:
        if "surgefoil" in card["promo_types"]:
            card_style = "Surge"
        if "showcase" in card["frame_effects"]:
            card_style = "Showcase"
        if "borderless" in card["border_color"] and "showcase" not in card["frame_effects"]:
            card_style = "Borderless"
        if "1997" in card["frame"] and "boosterfun" in card["promo_types"]:
            card_style = "Retro"
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

def fix_characters(card_name):
    current_file = card_name
    if "//" in current_file:
        current_file = str(current_file).replace(" // ", "_")
    if "\"" in current_file:
        current_file = str(current_file).replace("\"", "")
    if ":" in current_file:
        current_file = str(current_file).replace(":", "")
    if "?" in current_file:
        current_file = str(current_file).replace("?", "")
    current_file = unidecode(current_file)
    return current_file

def fix_set_name(name):
    set_name = name
    if ":" in set_name:
        set_name = str(name).replace(":", " -")
    return set_name

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

def build_file_names(card_list):
    card_names = []
    for card in card_list:
        if 'z' in card["collector_number"]:
            continue
        card_name = fix_characters(card) + card_style(card)
        card_dupes = find_dupes(card,card_list)
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
            return 0
        loop_name = fix_characters(loop_card) + card_style(loop_card)
        if card_name == loop_name and card["collector_number"] != loop_card["collector_number"]:
            dup_found = True
            if int(card["collector_number"]) > int(loop_card["collector_number"]):
                card_count = card_count + 1
    if dup_found:
        return card_count
    else:
        return 0

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
