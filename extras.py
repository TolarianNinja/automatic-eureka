import sets

def is_retro_style(card):
    if "1997" in card["frame"]:
        if "draft_innovation" in card["set_type"] or "masters" in card["set_type"]:
            print("Card Name: " + card["name"] + " Number: " + card["collector_number"])
            return True
        else:
            return False
    else:
        return False

def get_properties_all_cards():
    card_sets = sets.get_sets_full()
    promo_types = []
    frame_effects = []
    border_color = []
    layouts = []
    for c_set in card_sets:
        if c_set["card_count"] < 1:
            continue
        print("Now checking: " + c_set["name"])
        card_list = sets.get_set_cards(c_set["code"],False)
        for card in card_list:
            """
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
            try:
                for l_type in card["layout"]:
                    if l_type not in layouts:
                        layouts.append(l_type)
                    if l_type == "inverted" and card["set"] != "ltr":
                        print("Set: " + card["set"] + " Card: " + card["name"])
            except KeyError:
                pass
            """
    #print("Promo Types: " + str(promo_types))
    #print("Frame Effects: " + str(frame_effects))
    #print("Border Colors: " + str(border_color)))
    print("Layouts: " + str(layouts))

def get_card_console(card):
    card_name = build_filename(card)
    print("Card Name: " + card_name)

def get_set_console(set_code):
    card_set = scrython.sets.Code(code=set_code)
    print("Set Name: " + card_set.name() + "\nSet Code: " + card_set.code() + "\nRelease Date: " + str(card_set.released_at()) +
          "\nSet Type: " + card_set.set_type() + "\nNumber of Cards: " + str(card_set.card_count()) + "\n")
    card_list = get_set_cards(set_code)
    not_basic = 0

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

get_properties_all_cards()
