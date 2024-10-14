from tkinter import *
from tkinter import filedialog
from sys import platform
import controller, helpwindow

changes = False

def donothing():
    return

class SettingsWindow(Toplevel):
    def __init__(self,parent,master_controller):
        Toplevel.__init__(self)
        self.title("Settings")
        self.geometry("465x375")
        self.controller = master_controller
        if platform == "win32":
            self.iconbitmap(self.controller.get_home_directory() + "/images/settings.ico")
        else:
            self.iconbitmap(self.controller.get_home_directory() + "/images/settings.png"
        self.frame_path = SettingsFramePath(self, self.controller)
        self.frame_size = SettingsFrameSize(self, self.controller)
        self.frame_filters = SettingsFrameFilters(self, self.controller)
        self.frame_other = SettingsFrameOtherSettings(self, self.controller)
        self.frame_close = SettingsFrameClose(self)
        self.parent = parent

    def okay_save(self):
        global changes
        self.frame_path.save_info()
        self.frame_size.save_info()
        self.frame_filters.save_info()
        self.frame_other.save_info()
        self.controller.update_filtered_sets()
        if changes:
            self.controller.save_settings_file()
            self.parent.refresh()
        self.destroy()

    def reset_defaults(self):
        self.frame_path.set_default()
        self.frame_size.set_default()
        self.frame_filters.set_default()
        self.frame_other.set_default()

    def change_made(self,parent):
        global changes
        changes = True

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
        self.settings_download_path_entry.bind("<Button-1>", self.change_made)
    
        # Folder open for download path with icon
        self.settings_download_directory_image = PhotoImage(file = self.controller.get_home_directory() + "/images/selectdir.png")
        self.settings_download_directory_button = Button(self.settings_frame_path, command=self.set_path_askdirectory, image = self.settings_download_directory_image, width=16, height=16)
        self.settings_download_directory_button.grid(row=0, column=1)

    def set_path_askdirectory(self):
        new_path = filedialog.askdirectory()
        self.settings_download_path_string.set(new_path + "/")
        self.change_made(self)

    def save_info(self):
        self.controller.set_download_path(self.settings_download_path_string.get())

    def set_default(self):
        self.settings_download_path_string.set(self.controller.get_default_path())

    def change_made(self,parent):
        global changes
        changes = True

class SettingsFrameSize(LabelFrame):
    def __init__(self, parent, controller):
        # Image size radio buttons
        super().__init__(parent)
        self.controller = controller
        self.settings_frame_size = LabelFrame(parent, bd=2, text="Image Size", width=465, padx=5, pady=5)
        self.settings_frame_size.grid(row=1, column=0, sticky=W)
        self.settings_size = StringVar()
        self.settings_size_radio = [None] * 6
        size_text = [ "Small", "Normal", "Large", "PNG", "Art Crop", "Border Crop" ]
        size_values = [ "small", "normal", "large", "png", "art_crop", "border_crop" ]
        for num in range(0, 4):
            self.settings_size_radio[num] = Radiobutton(self.settings_frame_size, text=size_text[num], variable=self.settings_size, value=size_values[num], width=6)
            self.settings_size_radio[num].grid(row=0, column=num, sticky=W)
            self.settings_size_radio[num].bind("<Button-1>", self.change_made)
        # Last two need different widths
        self.settings_size_radio[4] = Radiobutton(self.settings_frame_size, text=size_text[4], variable=self.settings_size, value=size_values[4], width=7)
        self.settings_size_radio[5] = Radiobutton(self.settings_frame_size, text=size_text[5], variable=self.settings_size, value=size_values[5], width=9)
        self.settings_size_radio[4].grid(row=0, column=4, sticky=W)
        self.settings_size_radio[5].grid(row=0, column=5, sticky=W)
        self.settings_size_radio[4].bind("<Button-1>", self.change_made)
        self.settings_size_radio[5].bind("<Button-1>", self.change_made)
        
        self.settings_size.set(controller.get_image_size())

    def save_info(self):
        self.controller.set_image_size(self.settings_size.get())

    def set_default(self):
        self.settings_size.set(self.controller.get_default_size())

    def change_made(self,parent):
        global changes
        changes = True

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
            self.filter_buttons[i].bind("<Button-1>", self.change_made)
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

    def change_made(self,parent):
        global changes
        changes = True

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
        self.settings_get_digital_checkbox.bind("<Button-1>", self.change_made)
        self.settings_button_reset_default = Button(self.settings_frame_other_settings, text="Reset to defaults", command=parent.reset_defaults, width=19)
        self.settings_button_reset_default.grid(row=0, column=2, sticky=E)
        self.settings_button_reset_default.bind("<Button-1>", self.change_made)
        self.settings_info = Button(self.settings_frame_other_settings, text="Settings Info", width=19, command=self.open_help)
        self.settings_info.grid(row=0, column=1)
        self.settings_info.bind("<Button-1>", self.change_made)

    def save_info(self):
        self.controller.set_include_digital(self.get_digital.get())

    def set_default(self):
        self.get_digital.set(self.controller.get_default_digital())

    def change_made(self,parent):
        global changes
        changes = True

    def open_help(self):
        window = helpwindow.HelpWindow(self.controller.get_home_directory())

class SettingsFrameClose(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_frame_close = LabelFrame(parent, bd=0, width=465, padx=5, pady=5)
        self.settings_frame_close.grid(row=4, column=0, sticky=E)
        self.settings_button_okay = Button(self.settings_frame_close, command=parent.okay_save, text="Okay")
        self.settings_button_cancel = Button(self.settings_frame_close, command=parent.destroy, text="Cancel")
        self.settings_button_okay.grid(row=0, column=0)
        self.settings_button_cancel.grid(row=0, column=1)
