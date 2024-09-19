from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import threading
import sets, controller, settingswindow

root = Tk()
root.title('Automatic Eureka')
root.iconbitmap('images/ninja_icon.ico')

# Eris stores all the data and calls all the methods for that data
eris = controller.Controller()

# Used for the stop button
hard_stop = False

splash_path = "E:\\Programming Projects\\Python\\Automatic-Eureka\images\\splash.png"


def donothing():
    return

def window_about():
    about_message = """Automatic Eureka by Tolarian Ninja / Alex Hartshorn-Savage

Magic: The Gathering is property of Wizards of the Coast

Scryfall data is property of Scryfall, LLC

Scrython library by NandaScott
"""
    messagebox.showinfo(title="About Scryfall Image Downloader",
                        message=about_message)
"""    
class SettingsWindow(Toplevel):
    def __init__(self,master_controller):
        Toplevel.__init__(self)
        self.title('Settings')
        self.geometry('465x375')
        self.controller = master_controller

        frame_path = SettingsFramePath(self, self.controller.get_download_path())
        frame_size = SettingsFrameSize(self, self.controller.get_image_size())
        frame_filters = SettingsFrameFilters(self, self.controller.get_set_type_filters())
        frame_other = SettingsFrameOtherSettings(self, self.controller.get_include_digital())
        frame_close = SettingsFrameClose(self)

class SettingsFramePath(LabelFrame):
    def __init__(self, parent, path):
        # Entry for download path
        super().__init__(parent)
        self.settings_frame_path = LabelFrame(parent, bd=2, text="Download Path", width=465, padx=5, pady=5, labelanchor='nw')
        self.settings_frame_path.grid(row=0, column=0, sticky=W)
        self.settings_download_path_string = StringVar()
        self.settings_download_path_string.set(path)
        self.settings_download_path_entry = Entry(self.settings_frame_path, justify=LEFT, width=70, textvariable=self.settings_download_path_string)
        self.settings_download_path_entry.grid(row=0, column=0)
    
        # Folder open for download path with icon
        self.settings_download_directory_image = PhotoImage(file = r"images/selectdir.png")
        self.settings_download_directory_button = Button(self.settings_frame_path, command=donothing, image = self.settings_download_directory_image, width=16, height=16)
        self.settings_download_directory_button.grid(row=0, column=1)

class SettingsFrameSize(LabelFrame):
    def __init__(self, parent, size):
        # Image size radio buttons
        super().__init__(parent)
        self.settings_frame_size = LabelFrame(parent, bd=2, text="Image Size", width=465, padx=5, pady=5)
        self.settings_frame_size.grid(row=1, column=0, sticky=W)
        self.settings_size = StringVar()
        self.settings_size_radio_small = Radiobutton(self.settings_frame_size, text="Small", variable=self.settings_size, value="small", width=6)
        self.settings_size_radio_normal = Radiobutton(self.settings_frame_size, text="Normal", variable=self.settings_size, value="normal", width=6)
        self.settings_size_radio_large = Radiobutton(self.settings_frame_size, text="Large", variable=self.settings_size, value="large", width=6)
        self.settings_size_radio_png = Radiobutton(self.settings_frame_size, text="PNG", variable=self.settings_size, value="png", width=6)
        self.settings_size_radio_art_crop = Radiobutton(self.settings_frame_size, text="Art Crop", variable=self.settings_size, value="art_crop", width=7)
        self.settings_size_radio_border_crop = Radiobutton(self.settings_frame_size, text="Border Crop", variable=self.settings_size, value="border_crop", width=9)
        self.settings_size_radio_small.grid(row=0, column=0, sticky=W)
        self.settings_size_radio_normal.grid(row=0, column=1, sticky=W)
        self.settings_size_radio_large.grid(row=0, column=2, sticky=W)
        self.settings_size_radio_png.grid(row=0, column=3, sticky=W)
        self.settings_size_radio_art_crop.grid(row=0, column=4, sticky=W)
        self.settings_size_radio_border_crop.grid(row=0, column=5, sticky=W)
        self.settings_size.set(size)   

class SettingsFrameFilters(LabelFrame):
    def __init__(self, parent, filters):
        super().__init__(parent)
        filter_names = [ "Core Sets", "Expansions", "Draft Innovation", "Commander",
                         "Masters", "Arsenal", "From the Vault", "Spellbook",
                         "Premium Deck Series", "Duel Decks", "Starter", "Box",
                         "Planechase", "Archenemy", "Vanguard", "Funny",
                         "Promo", "Token", "Memorabilia", "Minigame",
                         "Alchemy", "Treasure Chest" ]
        c_row = 0
        c_col = 0
        filter_buttons = [None] * len(filter_names)
        filter_values = [None] * len(filter_names)
        self.settings_frame_filters = LabelFrame(parent, bd=2, text="Types of Set Listed", width=465, padx=5, pady=5)
        self.settings_frame_filters.grid(row=2, column=0, sticky=W)
        for i in range(0, len(filter_names)):
            filter_values[i] = IntVar()
            filter_buttons[i] = Checkbutton(self.settings_frame_filters, text=filter_names[i], variable=filter_values[i])
            filter_buttons[i].grid(row=c_row, column=c_col, sticky=W)
            filter_values[i].set(filters[i])
            filter_buttons[i].update()
            c_col = c_col + 1
            if c_col >= 4:
                c_row = c_row + 1
                c_col = 0

class SettingsFrameOtherSettings(LabelFrame):
    def __init__(self, parent, get_digital):
        super().__init__(parent)
        self.settings_frame_other_settings = LabelFrame(parent, bd=2, text="Other Settings", width=59, padx=5, pady=5)
        self.settings_frame_other_settings.grid(row=3, column=0, sticky=W)
        self.settings_get_digital_checkbox = Checkbutton(self.settings_frame_other_settings, text="Digital cards in paper sets", width=30, justify="left").grid(row=0, column=0, sticky=W)
        self.settings_button_reset_default = Button(self.settings_frame_other_settings, text="Reset to defaults", width=28).grid(row=0, column=1, sticky=E)

class SettingsFrameClose(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_frame_close = LabelFrame(parent, bd=0, width=465, padx=5, pady=5)
        self.settings_frame_close.grid(row=4, column=0, sticky=E)
        self.settings_button_okay = Button(self.settings_frame_close, command=donothing, text="Okay")
        self.settings_button_cancel = Button(self.settings_frame_close, command=donothing, text="Cancel")
        self.settings_button_okay.grid(row=0, column=0)
        self.settings_button_cancel.grid(row=0, column=1)
"""
def startup():
    load_set_cards()

def button_click_start():
    t = threading.Thread(target=start_process)
    t.start()

def button_click_settings():
    window = settingswindow.SettingsWindow(eris)

def start_process():
    global hard_stop
    card_name = ""
    progress_bar['value'] = 0
    if len(eris.get_card_list()) == 0:
        root.event_generate("<<ComboboxSelected>>")
    download_path = eris.build_folders()
    progress_bar['maximum'] = eris.get_set_size()
    for card in eris.get_card_list():
        if not hard_stop:
            if card["digital"]:
                continue
            card_name = eris.download_image(card,download_path)
            if card_name == "":
                image_text_string.set("Error when downloading (check console)" + card_name)
                image_text_label.update()
            else:
                card_path = eris.get_lang_path(card,download_path) + card_name
                update_image(image_label,card_path,eris.get_image_size())
                image_text_string.set("Downloaded " + card_name)
                image_text_label.update()
            progress_bar.step(1.0)
        else:
            break
    if hard_stop:
        complete_text = "Download process stopped after " + card_name + "."
        hard_stop = False
    else:
        complete_text = "Download of " + eris.get_set_name() + " completed successfully."
    progress_bar['value'] = 0
    image_text_string.set(complete_text)
    update_image(image_label,splash_path,"large")

def button_click_stop():
    global hard_stop
    hard_stop = True

def set_selected(self):
    set_code_text.set(get_code_selected())
    code_str = set_code_text.get()
    eris.update_set(code_str)
    load_set_cards()
    eris.get_set_langs()
    set_info = "Name: " + eris.get_set_name() + " | Set Code: " + code_str.upper()
    set_info_text.set(set_info)

def load_set_cards():
    page = 1
    progress_bar['maximum'] = get_page_count()
    image_text_string.set("Loading cards from " + eris.get_set_name())
    while len(eris.get_card_list()) < eris.get_set_size():
        eris.get_set_cards(get_code_selected(),page)
        progress_bar.step(1)
        progress_bar.update()
        if (page * 175) < eris.get_set_size():
            page = page + 1
        else:
            image_text_string.set(eris.get_set_name() + " is ready to download.")
            break

def get_page_count():
    pages = int(eris.get_set_size() / 175) + 1
    return pages
    
def get_code_selected():
    selected = sets_box.get()
    selected = selected.split(' ')
    set_code = selected[0].lower()
    return set_code

def set_box_select_all():
    sets_box['values'] = sets_list

def set_box_select_filter():
    sets_box['values'] = sets_list_filtered

def update_image(image_label,path,size):
    if size == "art_crop":
        card_image = Image.open(path).resize((430,314))
    else:
        card_image = Image.open(path).resize((430,600))
    tk_image = ImageTk.PhotoImage(card_image)
    image_label.configure(image=tk_image)
    image_label.image = tk_image

def on_entry_key(self):
    if len(search_entry := sets_box.get()) > 0:
        sets_searched = []
        for c_set in sets_box['values']:
            if search_entry.lower() in c_set.lower():
                sets_searched.append(c_set)
        sets_box['values'] = sets_searched
    else:
        sets_box['values'] = sets_list

# Controller Actions
sets_list = eris.get_sets_str()                     # Get formatted list of sets for Combobox
sets_list_filtered = eris.get_sets_filtered_str()   # Get formatted list of filtered sets
    
# Building the GUI
# Menu Bar
menu_bar = Menu(root)
filemenu = Menu(menu_bar, tearoff=0)
filemenu.add_command(label="Config (WIP)", command=donothing)
filemenu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menu_bar, tearoff=0)
helpmenu.add_command(label="Documentation (WIP)", command=donothing)
helpmenu.add_command(label="About", command=window_about)
menu_bar.add_cascade(label="Help", menu=helpmenu)

# Main Frame
main_frame = Frame(root, height=700, width=500, bd=2)
main_frame.pack()

# Top Frame
frame_top = LabelFrame(main_frame, width=450, bd=2, text="Set Information")
frame_top.grid(row=0, column=0)

set_code_text = StringVar(frame_top)

set_info_text = StringVar(frame_top)
set_info_text.set("Set Name: " + eris.get_set_name() + " | Set Code: "
                  + eris.get_set_code().upper())

# Combobox With List of Sets
sets_box = ttk.Combobox(frame_top, width = 50, height = 23)
sets_box['values'] = sets_list
set_search_font = font.Font(root,family="Courier New",size=8)
root.option_add("*TCombobox*Listbox*Font", set_search_font)

# Info Label for Selected Set
set_info_label = Label(frame_top, textvariable=set_info_text, justify="left", anchor="w", width=45)
set_info_label.lower()

# RadioButton for selecting filtered or not
#radio_all = Radiobutton(frame_top, text = "All Sets", value = "all")
#radio_filtered = Radiobutton(frame_top, text = "Filtered", value = "filtered")

# Start Button
start_image = PhotoImage(file = r"images/start.png")
start_button = Button(frame_top, command=button_click_start, image = start_image, width=36, height=36)

stop_image = PhotoImage(file = r"images/stop.png")
stop_button = Button(frame_top, command=button_click_stop, image = stop_image, width=36, height=36)

settings_image = PhotoImage(file = r"images/settings.png")
settings_button = Button(frame_top, command=button_click_settings, image = settings_image, width=36, height=36)

# Events
sets_box.bind("<<ComboboxSelected>>", set_selected)
sets_box.bind("<KeyRelease>", on_entry_key)
#radio_all.bind("<<RadiobuttonSelected>>", set_box_select_all)
#radio_filtered.bind("<<RadiobuttonSelected>>", set_box_select_filter)

# Top Frame Grid Sets
sets_box.grid(sticky = "W", row=0, column=0)
set_info_label.grid(sticky = "W", row=1, column=0)
#radio_all.grid(row=1, column=2)
#radio_filtered.grid(row=1, column=3)
start_button.grid(row=0, column=1, rowspan=2, sticky = "W")
stop_button.grid(row=0, column=2, rowspan=2, sticky = "W")
settings_button.grid(row=0, column=3, rowspan=2, sticky = "W")

# Bottom Frame
frame_bottom = LabelFrame(main_frame, width=450, height=630, bd=2, text="Downloaded Image")
frame_bottom.grid(row=1, column=0)

# Image Pane
side_image = ImageTk.PhotoImage(Image.open(splash_path).resize((430,600)))
image_label = Label(frame_bottom, image=side_image, height=615, width=441)

# Info Label for Downloaded Image
image_text_string = StringVar(frame_bottom)
image_text_label = Label(frame_bottom, textvariable=image_text_string)
image_text_string.set("Select a set from the drop down.  Enter text to filter by name or set code.")

# Bottom Frame Grid Sets
image_label.grid(row=0, column=0)
image_text_label.grid(row=1, column=0)

# Progress Bar
progress_bar = ttk.Progressbar(frame_bottom, length=445)
progress_bar.grid(row=2, column=0)

# Startups
startup()
root.config(menu=menu_bar)
root.mainloop()
