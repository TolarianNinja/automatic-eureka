from tkinter import *
import controller

def donothing():
    return

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
