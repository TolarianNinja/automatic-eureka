import shutil, os, scrython, requests, sets,time
from unidecode import unidecode

image_path = "E:\\Programming Projects\\Python\\Automatic-Eureka\\Testing Dump\\"

def card_style(card):
    card_style = ""
    variant_foil = False
    if "sld" in card["set"]:
        card_style = col_num_prefix(card)
    if "type_line" in card:
        if "Basic" in card["type_line"]:
            return card_style
    if card["promo"]:
        if len(card_style := is_set_promo(card)) > 0:
            return " [" + card_style + "]"
    elif "promo_types" in card:
        if len(card_style := is_variant_foil(card)) > 0:
            variant_foil = True
        elif len(card_style := is_set_foil(card)) > 0:
            return " [" + card_style + "]"
    if "frame_effects" in card:
        if len(card_style := is_variant(card,variant_foil,card_style)) > 0:
            return " [" + card_style + "]"
    if len(card_style := is_borderless(card,variant_foil,card_style)) > 0:
        return " [" + card_style + "]"
    if len(card_style) > 0:
        return " [" + card_style + "]"
    else:
        return card_style

def is_borderless(card,variant_foil,card_style):
    version = ""
    if "borderless" in card["border_color"]:
        version = "Alt Art"
    if len(version) > 0:
        if variant_foil:
            return card_style + " " + version
        else:
            return version
    return card_style
               
def is_variant(card,variant_foil,card_style):
    version = ""
    if "extendedart" in card["frame_effects"]:
        version = "Ext Art"
    elif "showcase" in card["frame_effects"]:
        version = "Showcase"
    elif "etched" in card["frame_effects"]:
        version = "Etched"
    if len(version) > 0:
        if variant_foil:
            return card_style + " " + version
        else:
            return version
    else:
        return card_style

def is_variant_foil(card):
    card_style = ""
    if "surgefoil" in card["promo_types"]:
        card_style = "Surge"
    elif "galaxyfoil" in card["promo_types"]:
        card_style = "Galaxy"
    return card_style

def is_set_promo(card):
    card_style = ""
    if "prerelease" in card["promo_types"]:
        card_style = "S"
    elif "stamped" in card["promo_types"]:
        card_style = "P"
    elif "promopack" in card["promo_types"] or "bundle" in card["promo_types"]:
        card_style = "Promo"
    return card_style
            
def is_set_foil(card):
    if "stepandcompleat" in card["promo_types"]:
        card_style = "Compleat"
    elif "confettifoil" in card["promo_types"]:
        card_style = "Confetti"
    elif "dossier" in card["promo_types"]:
        card_style = "Dossier"
    elif "embossed" in card["promo_types"]:
        card_style = "Embossed"
    elif "galaxyfoil" in card["promo_types"]:
        card_style = "Galaxy Foil"
    elif "gilded" in card["promo_types"]:
        card_style = "Gilded"
    elif "halofoil" in card["promo_types"]:
        card_style = "Halo"
    elif "invisibleink" in card["promo_types"]:
        card_style = "Invisible Ink"
    elif "magnified" in card["promo_types"]:
        card_style = "Magnified"
    elif "oilslick" in card["promo_types"]:
        card_style = "Oil"
    elif "rainbowfoil" in card["promo_types"]:
        card_style = "Rainbow"
    elif "textured" in card["promo_types"]:
        card_style = "Textured"
    elif "1997" in card["frame"] and "boosterfun" in card["promo_types"]:
        card_style = "Retro"
    else:
        card_style = ""
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

def fix_characters(card_name):
    current_file = str(card_name)
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
    set_name = fix_set_name(card_set["name"])
    main_path = image_path + set_name + "\\"
    card_list = sets.get_set_cards(card_set["code"],True)
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
    return main_path

# Finds if there are multiple cards with the same output name.
# If no return 0, else return which instance this is (second Plains will be 2)
def find_dupes(card,card_list):
    card_count = 1
    dup_found = False
    if 'z' in card["collector_number"]:
        return 0
    card_name = fix_characters(card["name"]) + card_style(card)
    card_num = remove_non_num(card["collector_number"])
    for loop_card in card_list:
        if 'z' in loop_card["collector_number"]:
            return 0
        loop_name = fix_characters(loop_card["name"]) + card_style(loop_card)
        loop_num = remove_non_num(loop_card["collector_number"])
        if card_name == loop_name and card_num != loop_num and card["lang"] == loop_card["lang"]:# and card["finishes"] == loop_card["finishes"]:
            dup_found = True
            if card_num > loop_num:
                card_count = card_count + 1
    if dup_found:
        return card_count
    else:
        return 0

# Removes non-numeric characters from collector numbers.  Used to compare the numbers.
def remove_non_num(number):
    output = ''.join(c for c in number if c.isdigit())
    return output

# Checks the set 
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

def collector_num_variant(card):
    try:
        coll_num = int(card["collector_number"])
        return ""
    except ValueError:
        return card["collector_number"][-1]

def download_image(card,dupes,path,size,get_digital):
    if card["digital"]:
        if not get_digital:
            return
    if "png" in size:
        ext = "png"
    else:
        ext = "jpg"
    dupe_string = ""
    os.chdir(path)
    if dupes > 0:
        dupe_string = " [" + str(dupes) + "]"
    if len(coll_num := collector_num_variant(card)) > 0:
        dupe_string = " [" + coll_num + "]"
    if card["layout"] == "transform" or card["layout"] == "modal_dfc":
        file_names = []
        for i in range(0, 2):
            file_name = fix_characters(card["card_faces"][i]["name"]) + card_style(card) + dupe_string
            file_url = card["card_faces"][i]["image_uris"][size]
            file_name = file_name + '.' + ext
            image_data = requests.get(file_url).content
            with open(file_name, 'wb') as handler:
                handler.write(image_data)
                handler.close()
            file_names.append(file_name)
        return file_names[0]
    else:
        file_name = fix_characters(card["name"]) + card_style(card) + dupe_string
        file_url = card["image_uris"][size]
        file_name = file_name + '.' + ext
        image_data = requests.get(file_url).content
        with open(file_name, 'wb') as handler:
            handler.write(image_data)
            handler.close()
        return file_name
            
def get_image_size(size):
    if "small" in size:
        return "small"
    elif "normal" in size:
        return "normal"
    elif "large" in size:
        return "large"
    elif "png" in size:
        return "png"
    elif "art_crop" in size:
        return "art_crop"
    elif "border_crop" in size:
        return "border_crop"

def get_lang_path(path,card):
    card_lang = fix_lang(card["lang"])
    if card["nonfoil"]:
        download_path = path + card_lang + "\\"
    else:
        download_path = path + card_lang + " FOIL\\"
    return download_path

def download_set_images(card_set):
    path = build_folders(card_set)
    card_list = sets.get_set_cards(card_set["code"],False)
    for card in card_list:
        time.sleep(0.23)            # Rate limit
        download_path = get_lang_path(path,card)
        dupes = find_dupes(card,card_list)
        downloaded_filename = download_image(card,dupes,download_path,"large",False)
        print("Downloaded: " + str(downloaded_filename))
    print("Work complete.")
    

#download_set_images(sets.get_set("pip"))
"""
set_cards = sets.get_set_cards("unf",False)
for card in set_cards:
    dupes = find_dupes(card,set_cards)
    card_path = get_lang_path(image_path,card)
    dupe_string = ""
    if dupes > 0:
        dupe_string = " [" + str(dupes) + "]"
    elif len(coll_num := collector_num_variant(card)) > 0:
        dupe_string = " [" + coll_num + "]"
    print(str(card["collector_number"]) + ", " + card["name"] + card_style(card) + dupe_string)
"""
