import dloader, sets, scrython, time, os, settingsfile

# set_list              The list of sets
# current_set           The current set (JSON) that is loaded
# current_set_name      The name of the loaded set
# current_set_code      The code of the loaded set
# current_set_size      The total number of cards in the set
# card_list             A list containing each individual card (JSON) in the set
# set_languages_nf      The languages of all nonfoil cards in the set
# set_languages_f       The languages of all foil only cards in the set
# file_names            The array of formatted filenames
class Controller:
    def __init__(self):
        # Currently offline.  This should get refactored anyway.
        self.set_list = sets.get_sets_full()
        #self.current_set = self.set_list[0]
        #self.current_set_name = self.current_set["name"]
        #self.current_set_code = self.current_set["code"]
        #self.current_set_size = self.current_set["card_count"]
        self.card_list = [] 
        self.set_languages_nf = []
        self.set_languages_f = []
        self.download_path = ""
        #self.download_path = "E:\Programming Projects\Python\Automatic-Eureka\Testing Dump\\"
        self.include_digital = 0
        self.image_size = "large"
        self.set_type_filters = []
        self.settings_file = settingsfile.SettingsFile(self)
        self.rate_limit = 0.23
        self.set_list_filtered = sets.get_sets_filtered(self.set_list,self.set_type_filters,self.include_digital)
        self.home_directory = os.getcwd()
        self.hard_stop = False

    def __str__(self):
        return str(self.current_set["name"])
    
    def update_set(self, set_code):
        for c_set in self.set_list:
            if set_code == c_set["code"]:
                self.current_set = c_set
        self.current_set_code = set_code
        self.current_set_name = self.current_set["name"]
        self.current_set_size = self.current_set["card_count"]
        self.card_list = []

    def get_set_langs(self):
        self.set_languages_nf = sets.get_set_languages(self.card_list,False)
        self.set_languages_f = sets.get_set_languages(self.card_list,True)
        
    def get_set_code(self):
        return self.current_set_code

    def get_current_set(self):
        return self.current_set

    def get_set_digital(self):
        return self.current_set["digital"]

    def get_set_name(self):
        return self.current_set_name

    def get_set_size(self):
        return self.current_set_size

    def find_set_code(set_code):
        current_set = None
        for c_set in self.set_list:
            if set_code == c_set["code"]:
                return c_set
        print("Could not find set " + set_code)

    def print_set_list(self):
        for c_set in self.set_list:
            print(str(c_set))

    def set_code_str(set_code):
        code_len = len(set_code)
        for i in [code_len, 8]:
            set_code = set_code + " "
        return set_code

    def get_sets_all_str(self):
        set_strings = []
        for c_set in self.set_list:
            set_code = str(c_set["code"]).upper()
            code_len = len(set_code)
            i = code_len
            while i < 5:
                set_code = set_code + " "
                i = i + 1
            entry = set_code + " - " + str(c_set["name"])
            set_strings.append(entry)
        return set_strings

    def get_sets_filtered_str(self):
        set_strings = []
        for c_set in self.set_list_filtered:
            set_code = str(c_set["code"]).upper()
            code_len = len(set_code)
            i = code_len
            while i < 5:
                set_code = set_code + " "
                i = i + 1
            entry = set_code + " - " + str(c_set["name"])
            set_strings.append(entry)
        return set_strings

    def build_folders(self):
        #print(self.download_path + self.ma_set_type())
        main_path = dloader.build_folders(
            self.download_path + self.ma_set_type(),
            self.current_set_name,
            self.set_languages_nf,
            self.set_languages_f)
        return main_path

    def get_download_path(self):
        return self.download_path

    def get_rate_limit(self):
        return self.rate_limit

    def get_card_list(self):
        return self.card_list

    def download_image(self,card,set_download_path):
        file_name = dloader.boot_download(
            card,
            self.card_list,
            set_download_path,
            self.current_set_name,
            self.image_size,
            self.include_digital)
        if len(file_name) == 0:
            print("Error downloading " + card["name"] + " | Set: " + card["set"])
        return file_name

    def get_lang_path(self,card,path):
        return dloader.get_lang_path(path,card)

    def get_image_size(self):
        return self.image_size

    def get_set_cards(self,set_code,page_num):
        query = '++e:' + set_code
        search = scrython.cards.Search(q=query, page=page_num, order="set")
        for card in search.data():
            self.card_list.append(card)
        time.sleep(self.get_rate_limit())
        return self.card_list

    def set_download_path(self, path):
        self.download_path = path

    def set_image_size(self, size):
        self.image_size = size

    def set_set_type_filters(self, filters):
        self.set_type_filters = filters

    def set_include_digital(self, get_digital):
        self.include_digital = get_digital

    def save_settings(path,size,filters,get_digital):
        set_download_path(path)
        set_image_size(size)
        set_set_type_filters(filters)
        set_include_digital(get_digital)
        save_settings_file()

    def save_settings_file(self):
        self.settings_file.save_settings(
            [ self.download_path,
            self.image_size,
            self.set_type_filters,
            self.include_digital ])

    def load_settings(self, settings):
        self.set_download_path(settings[0].strip('\n'))
        self.set_image_size(settings[1])
        self.set_set_type_filters(settings[2])
        self.set_include_digital(settings[3])

    def get_set_type_filters(self):
        return self.set_type_filters

    def get_include_digital(self):
        return self.include_digital

    def get_defaults(self):
        settings = []
        default_path = os.getcwd() + "\\Downloads\\"
        size = "large"
        set_filters = [ 1, 1, 1, 1, 1, 1, 1, 1,
                        1, 1, 1, 1, 1, 0, 0, 0,
                        1, 0, 0, 0, 0, 0, 0 ]
        get_digital = 0
        settings.append(default_path)
        settings.append(size)
        settings.append(set_filters)
        settings.append(get_digital)
        return settings

    def get_default_path(self):
        return os.getcwd() + "\\Downloads\\"

    def get_default_size(self):
        return "large"

    def get_default_filters(self):
        return [ 1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 0, 0,
                1, 0, 0, 0, 0, 0, 0 ]

    def get_default_digital(self):
        return 0

    def get_home_directory(self):
        return self.home_directory

    def go_home(self):
        os.chdir(self.home_directory)

    def get_page_count(self):
        if self.get_set_size() % 175 == 0:
            pages = int(self.get_set_size() / 175)
        else:
            pages = int(self.get_set_size() / 175) + 1
        return pages

    def update_filtered_sets(self):
        self.set_list_filtered = sets.get_sets_filtered(self.set_list,self.set_type_filters,self.include_digital)

    def set_stop(self):
        self.hard_stop = True

    def unset_stop(self):
        self.hard_stop = False

    def is_stop(self):
        return self.hard_stop

    def ma_set_type(self):
        match self.current_set["set_type"]:
            case "core":
                return "Core Sets\\"
            case "expansion":
                return "Expansions\\"
            case "promo":
                return "Promo Cards\\"
            case "token":
                return "Tokens\\"
            case _:
                return "Special Sets\\"
