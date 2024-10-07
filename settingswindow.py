from tkinter import *
from tkinter import filedialog
import controller

def donothing():
    return

class SettingsWindow(Toplevel):
    def __init__(self,master_controller):
        Toplevel.__init__(self)
        self.title('Settings')
        self.geometry('465x375')
        self.iconbitmap('images/settings_icon.ico')
        self.controller = master_controller

        self.frame_path = SettingsFramePath(self, self.controller)
        self.frame_size = SettingsFrameSize(self, self.controller)
        self.frame_filters = SettingsFrameFilters(self, self.controller)
        self.frame_other = SettingsFrameOtherSettings(self, self.controller)
        self.frame_close = SettingsFrameClose(self)

    def okay_save(self):
        self.frame_path.save_info()
        self.frame_size.save_info()
        self.frame_filters.save_info()
        self.frame_other.save_info()
        self.controller.update_filtered_sets()
        self.destroy()

    def reset_defaults(self):
        self.frame_path.set_default()
        self.frame_size.set_default()
        self.frame_filters.set_default()
        self.frame_other.set_default()

class SettingsFramePath(LabelFrame):
    def __init__(self, parent, controller):
        # Entry for download path
        super().__init__(parent)
        self.controller = controller
        self.settings_frame_path = LabelFrame(parent, bd=2, text="Download Path", width=465, padx=5, pady=5, labelanchor='nw')
        self.settings_frame_path.grid(row=0, column=0, sticky=W)
        self.settings_download_path_string = StringVar()
        self.settings_download_path_string.set(self.controller.get_download_path())
        self.settings_download_path_entry = Entry(self.settings_frame_path, justify=LEFT, width=70, textvariable=self.settings_download_path_string)
        self.settings_download_path_entry.grid(row=0, column=0)
    
        # Folder open for download path with icon
        self.settings_download_directory_image = PhotoImage(file = r"images/selectdir.png")
        self.settings_download_directory_button = Button(self.settings_frame_path, command=self.set_path_askdirectory, image = self.settings_download_directory_image, width=16, height=16)
        self.settings_download_directory_button.grid(row=0, column=1)

    def set_path_askdirectory(self):
        new_path = filedialog.askdirectory()
        self.settings_download_path_string.set(new_path)

    def save_info(self):
        self.controller.set_download_path(self.settings_download_path_string.get())

    def set_default(self):
        self.settings_download_path_string.set(self.controller.get_default_path())

class SettingsFrameSize(LabelFrame):
    def __init__(self, parent, controller):
        # Image size radio buttons
        super().__init__(parent)
        self.controller = controller
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
        self.settings_size.set(controller.get_image_size())

    def save_info(self):
        self.controller.set_image_size(self.settings_size.get())

    def set_default(self):
        self.settings_size.set(self.controller.get_default_size())

class SettingsFrameFilters(LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        filter_names = [ "Core Sets", "Expansions", "Draft Innovation", "Commander",
                         "Masters", "Arsenal", "From the Vault", "Spellbook",
                         "Premium Deck Series", "Starter", "Box", "Masterpiece",
                         "Duel Decks", "Planechase", "Archenemy", "Vanguard", 
                         "Funny", "Promo", "Token", "Memorabilia", 
                         "Minigame", "Alchemy", "Treasure Chest" ]
        c_row = 0
        c_col = 0
        self.filter_buttons = [None] * len(filter_names)
        self.filter_values = [None] * len(filter_names)
        self.settings_frame_filters = LabelFrame(parent, bd=2, text="Types of Set Listed", width=465, padx=5, pady=5)
        self.settings_frame_filters.grid(row=2, column=0, sticky=W)
        for i in range(0, len(filter_names)):
            self.filter_values[i] = IntVar()
            self.filter_values[i].set(controller.get_set_type_filters()[i])
            self.filter_buttons[i] = Checkbutton(self.settings_frame_filters, text=filter_names[i], variable=self.filter_values[i])
            self.filter_buttons[i].grid(row=c_row, column=c_col, sticky=W)
            self.filter_buttons[i].update()
            c_col = c_col + 1
            if c_col >= 4:
                c_row = c_row + 1
                c_col = 0

    def save_info(self):
        values_return = []
        for num in self.filter_values:
            values_return.append(num.get())
        self.controller.set_set_type_filters(values_return)

    def set_default(self):
        default_filters = self.controller.get_default_filters()
        for i in range(0, len(default_filters)):
            self.filter_values[i].set(default_filters[i])

class SettingsFrameOtherSettings(LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.get_digital = IntVar()
        self.get_digital.set(controller.get_include_digital())
        self.settings_frame_other_settings = LabelFrame(parent, bd=2, text="Other Settings", width=59, padx=5, pady=5)
        self.settings_frame_other_settings.grid(row=3, column=0, sticky=W)
        self.settings_get_digital_checkbox = Checkbutton(self.settings_frame_other_settings, text="Digital cards in paper sets", width=19, justify="left", variable=self.get_digital)
        self.settings_get_digital_checkbox.grid(row=0, column=0, sticky=W)
        self.settings_button_reset_default = Button(self.settings_frame_other_settings, text="Reset to defaults", command=parent.reset_defaults, width=19)
        self.settings_button_reset_default.grid(row=0, column=2, sticky=E)
        self.settings_get_digital_checkbox = Button(self.settings_frame_other_settings, text="Settings Info", width=19)
        self.settings_get_digital_checkbox.grid(row=0, column=1)

    def save_info(self):
        self.controller.set_include_digital(self.get_digital.get())

    def set_default(self):
        self.get_digital.set(self.controller.get_default_digital())

class SettingsFrameClose(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_frame_close = LabelFrame(parent, bd=0, width=465, padx=5, pady=5)
        self.settings_frame_close.grid(row=4, column=0, sticky=E)
        self.settings_button_okay = Button(self.settings_frame_close, command=parent.okay_save, text="Okay")
        self.settings_button_cancel = Button(self.settings_frame_close, command=parent.destroy, text="Cancel")
        self.settings_button_okay.grid(row=0, column=0)
        self.settings_button_cancel.grid(row=0, column=1)
