import shutil, os, requests, sets,time
from unidecode import unidecode

image_path = "E:\\Programming Projects\\Python\\Automatic-Eureka\\Testing Dump\\"

def card_style(card):
    card_style = ""
    variant_foil = False
    # Secret Lair has version checked with collector number, same with some specific cards
    if "sld" in card["set"] or fix_characters(card["name"]) == "Nazgul":
        return str(col_num_prefix(card))
    if card["promo"]:
        if len(card_style := is_set_promo(card)) > 0:
            return card_style
    elif "promo_types" in card:
        if len(card_style := is_variant_foil(card)) > 0:
            variant_foil = True
        elif len(card_style := is_set_foil(card)) > 0:
            return card_style
    if "frame_effects" in card:
        if len(card_style := is_variant(card,variant_foil,card_style)) > 0:
            return card_style
    if len(card_style := is_borderless(card,variant_foil,card_style)) > 0:
        return card_style
    if len(card_style) > 0:
        return card_style
    else:
        return card_style

def is_borderless(card,variant_foil,card_style):
    version = ""
    # Masterpiece sets will all have the same fancy format (everything special == nothing is)
    if card["set_type"] == "masterpiece":
        return card_style
    if "art_series" in card["layout"]:
        return card_style
    if "borderless" in card["border_color"]:
        # Checking specifically for scene cards from ltr, will remove set check if this returns
        if card["set"] == "ltr" and "frame_effects" in card and "inverted" in card["frame_effects"]:
            version = "Scene"            
        else:
            version = "Alt Art"
    if len(version) > 0:
        if variant_foil:
            return card_style + " " + version
        else:
            return version
    elif variant_foil and card["set"] == "unf":
        return card_style + " Foil"
    return card_style
               
def is_variant(card,variant_foil,card_style):
    version = ""
    # everything special == nothing is
    if card["set_type"] == "masterpiece":
        return card_style
    if "extendedart" in card["frame_effects"]:
        version = "Ext Art"
    elif "showcase" in card["frame_effects"]:
        # Checking specifically for the ring showcase cards from ltr
        if card["set"] == "ltr" and "promo_types" in card and "scroll" not in card["promo_types"]:
            version = "Ring"
        else:
            version = "Showcase"
    elif "etched" in card["frame_effects"]:
        version = "Etched"
    if variant_foil:
        # More ltr specific fixes
        if card["set"] == "ltr":
            return card_style
    if len(version) > 0:
        if variant_foil:
            # Magic Album has these backwards for Unfinity
            if card["set"] == "unf":
                return version + " " + card_style
            else:
                return card_style + " " + version
        else:
            return version
    else:
        if card["set"] == "unf" and variant_foil:
            return card_style + " Foil"
        else:
            return card_style

def is_variant_foil(card):
    card_style = ""
    if "surgefoil" in card["promo_types"]:
        card_style = "Surge"
    elif "galaxyfoil" in card["promo_types"]:
        card_style = "Galaxy"
    elif "ripplefoil" in card["promo_types"]:
        card_style = "Ripple"
    return card_style

def is_set_promo(card):
    card_style = ""
    if "promo_types" in card:
        if "prerelease" in card["promo_types"]:
            card_style = "S"
        elif "stamped" in card["promo_types"]:
            card_style = "P"
        elif "promopack" in card["promo_types"] or "bundle" in card["promo_types"] or "playpromo" in card["promo_types"] or "buyabox" in card["promo_types"]:
            card_style = "Promo"
    return card_style
            
def is_set_foil(card):
    if "stepandcompleat" in card["promo_types"]:
        card_style = "Compleat"
    elif "confettifoil" in card["promo_types"]:
        card_style = "Confetti"
    elif "textured" in card["promo_types"]:
        card_style = "Textured"
    elif "invisibleink" in card["promo_types"]:
        card_style = "Invisible Ink"
    elif "dossier" in card["promo_types"]:
        card_style = "Dossier"
    elif "embossed" in card["promo_types"]:
        card_style = "Embossed"
    elif "galaxyfoil" in card["promo_types"]:
        card_style = "Galaxy Foil"
    elif "fracturefoil" in card["promo_types"]:
        card_style = "Fracture"
    elif "gilded" in card["promo_types"]:
        card_style = "Gilded"
    elif "halofoil" in card["promo_types"]:
        card_style = "Halo"
    elif "magnified" in card["promo_types"]:
        card_style = "Magnified"
    elif "oilslick" in card["promo_types"]:
        card_style = "Oil"
    elif "rainbowfoil" in card["promo_types"]:
        card_style = "Rainbow"
    elif "raisedfoil" in card["promo_types"]:
        card_style = "Raised"
    elif "portrait" in card["promo_types"]:
        card_style = "Profile"
    elif "1997" in card["frame"] and "boosterfun" in card["promo_types"]:
        card_style = "Retro"
    else:
        card_style = ""
    return card_style

def col_num_prefix(card):
    try:
        col_num = int(card["collector_number"])
    except ValueError:
        return card["collector_number"]
    if col_num >= 100:
        return col_num
    elif col_num < 10:
        output = "00" + str(col_num)
    elif col_num < 100:
        output = "0" + str(col_num)
    return output
"""
    elif col_num < 1000:
        output = "0" + str(col_num)
"""

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
    # Magic Album file name fix for Unfinity Name Sticker cards
    if "_____ _____ _____" in current_file:
        return current_file
    elif "_____ _____" in current_file:
        current_file = str(current_file).replace("_____", "______")
    elif "_____" in current_file:
        current_file = str(current_file).replace("_____", "________")
    return current_file

def fix_set_name(name):
    set_name = name
    if ":" in set_name:
        set_name = str(name).replace(":", " -")
    return set_name

def build_folders(path,set_name,langs_nf,langs_f):
    main_path = path + fix_set_name(set_name) + "\\"
    os.makedirs(main_path,511,True)
    os.chdir(main_path)
    for lang in langs_nf:
        lang_path = main_path + lang + "\\"
        os.makedirs(lang_path,511,True)
    for lang in langs_f:
        lang_path = main_path + lang + " FOIL\\"
        os.makedirs(lang_path,511,True)
    return main_path

# Finds if there are multiple cards with the same output name.
# If no return 0, else return which instance this is (second Plains will be 2)
# Ignore Secret Lair (sld) and collector numbers with 'z' (serialized)
def find_dupes(card,card_list):
    card_count = 1
    dup_found = False
    if card["set"] == "sld":
        return 0
    if 'z' in card["collector_number"]:
        return 0
    card_name = fix_characters(card["name"]) + card_style(card)
    for loop_card in card_list:
        if 'z' in loop_card["collector_number"]:
            continue
        loop_name = fix_characters(loop_card["name"]) + card_style(loop_card)
        if card_name == loop_name:
            if is_dupe(card,loop_card):
                card_num = remove_non_num(card["collector_number"])
                loop_num = remove_non_num(loop_card["collector_number"])
                dup_found = True
                if card_num > loop_num:
                    card_count = card_count + 1
    if dup_found:
        return card_count
    else:
        return 0

# The number of things to check against to be sure that it's a 'true' duplicate moved
# it into its own function.
def is_dupe(card,loop_card):
    if card["collector_number"] != loop_card["collector_number"]:
        if card["nonfoil"] == loop_card["nonfoil"]:
            if card["foil"] == loop_card["foil"]:
                if card["lang"] == loop_card["lang"]:
                    return True
    return False
                

# Removes non-numeric characters from collector numbers.  Used to compare the numbers.
def remove_non_num(number):
    output = ''.join(c for c in number if c.isdigit())
    if output == '':
        return number
    else:
        return output

# Checks every card in the set to find the languages for foil or nonfoil cards.
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

# Changes the input from Scryfall data to the expected file path for Magic Album.
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

# Used to find the non-numeric character in collector number variants (RIP Neon Mana Crypt)
def collector_num_variant(card):
    if card["set"] == "sld":
        return ""
    try:
        coll_num = int(card["collector_number"])
        return ""
    except ValueError:
        # planeswalker stamp, date stamp, serialized, foil
        if card["collector_number"][-1] in "psz★":
            return ""
        else:
            return card["collector_number"][-1]

# Let's actually download the image!  This is slowly getting refactored to be less of a clusterfuck.
def download_image(card,dupes,path,size,get_digital,name_check):
    if card["digital"]:
        if not get_digital:
            return
    dupe_string = ""
    os.chdir(path)
    if two_face(card):
        file_names = []
        for i in range(0, 2):
            if card["layout"] == "reversible_card":
                file_name = build_filename_reversible(card,dupes,i)
            else:
                file_name = build_filename_faces(card,dupes,i,name_check)
            file_url = card["card_faces"][i]["image_uris"][size]
            file_name = file_name + '.' + get_ext(size)
            if not os.path.exists(file_name):
                image_data = requests.get(file_url).content
                with open(file_name, 'wb') as handler:
                    handler.write(image_data)
                    handler.close()
            file_names.append(file_name)
        return file_names[0]
    else:
        file_name = build_filename(card,dupes,name_check)
        file_url = card["image_uris"][size]
        file_name = file_name + '.' + get_ext(size)
        if not os.path.exists(file_name):
            image_data = requests.get(file_url).content
            with open(file_name, 'wb') as handler:
                handler.write(image_data)
                handler.close()
        return file_name

# Returns the file extension based on image_size (everything except PNG is JPG)
def get_ext(size):
    if "png" in size:
        return "png"
    else:
        return "jpg"

# Builds the filename and appropriately places brackets based on dupes of card styles
def build_filename(card,dupes,name_check):
    if "flavor_name" in card and not card["reprint"]:
        card_name = fix_characters(card["flavor_name"])
    else:
        card_name = fix_characters(card["name"])
    if not name_check:
        return card_name
    c_style = card_style(card)
    coll_variant = collector_num_variant(card)
    # if variant + coll_num variant + dupe
    if dupes > 0 and len(c_style) > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + c_style + " " + coll_variant + " " + str(dupes) + "]"
    # if variant + dupe
    elif dupes > 0 and len(c_style) > 0:
        card_name = card_name + " [" + c_style + " " + str(dupes) + "]"
    # if variant + coll_num variant
    elif len(c_style) > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + c_style + "" + coll_variant + "]"
        print("Card Name: " + card["name"] + " Card Number: \"" + str(card["collector_number"]) + "\"")
    # if dupe + coll_num variant
    elif dupes > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + coll_variant + " " + dupes + "]"
    # if dupe
    elif dupes > 0:
        card_name = card_name + " [" + str(dupes) + "]"
    # if variant
    elif len(c_style) > 0:
        card_name = card_name + " [" + c_style + "]"
    # if coll_num variant
    elif len(coll_variant) > 0:
        card_name = card_name + " [" + coll_variant + "]"
    # if normal card
    else:
        card_name = card_name
    return card_name

# Same function as build_filename but for handling card faces.
def build_filename_faces(card,dupes,face,name_check):
    if "flavor_name" in card and not card["reprint"]:
        card_name = fix_characters(card["card_faces"][face]["flavor_name"])
    else:
        card_name = fix_characters(card["card_faces"][face]["name"])
    if not name_check and not card["promo"]:
        return card_name
    c_style = card_style(card)
    coll_variant = collector_num_variant(card)
    if dupes > 0 and len(c_style) > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + c_style + " " + coll_variant + " " + str(dupes) + "]"
    elif dupes > 0 and len(c_style) > 0:
        card_name = card_name + " [" + c_style + " " + str(dupes) + "]"
    elif dupes > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + c_style + "" + str(coll_variant) + "]"
    elif len(c_style) > 0 and len(coll_variant) > 0:
        card_name = card_name + " [" + c_style + "" + coll_variant + "]"
    elif dupes > 0:
        card_name = card_name + " [" + str(dupes) + "]"
    elif len(c_style) > 0:
        card_name = card_name + " [" + c_style + "]"
    elif len(coll_variant) > 0:
        card_name = card_name + " [" + coll_variant + "]"
    else:
        card_name = card_name
    return card_name

def build_filename_reversible(card,dupes,face):
    card_name = fix_characters(card["card_faces"][face]["name"])
    c_style = card_style(card)
    if face == 0:
        f_name = 'a'
    else:
        f_name = 'b'
    if len(c_style) > 0:
        card_name = card_name + " [" + c_style + f_name + "]"
    else:
        card_name = card_name + " [" + f_name + "]"
    return card_name

# Fighting the urge to call this function some variation of Harvey Dent.
def two_face(card):
    match card["layout"]:
        case "transform" | "modal_dfc" | "reversible_card" | "art_series":
            return True
        case _:
            return False

# Returns the file_name that was downloaded to controller which sends it to GUI
def boot_download(card,card_list,path,set_name,size,get_digital):
    dupes = find_dupes(card,card_list)
    download_path = get_lang_path(path,card)
    n_check = name_check(card,card_list)
    file_name = download_image(card,dupes,download_path,size,get_digital,n_check)
    return file_name

def name_check(card,card_list):
    for loop_card in card_list:
        if card["name"] == loop_card["name"]:
            if card["collector_number"] != loop_card["collector_number"]:
                return True
    return False

def get_lang_path(path,card):
    card_lang = fix_lang(card["lang"])
    if card["nonfoil"]:
        download_path = path + card_lang + "\\"
    else:
        download_path = path + card_lang + " FOIL\\"
    return download_path

"""
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
"""
