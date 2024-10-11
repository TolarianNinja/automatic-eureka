from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import threading
import controller, settingswindow

running = False

class ControlFrame(LabelFrame):
    def __init__(self, parent, master_controller):
        super().__init__(parent, width=450, height=40, bd=2, text="Set Information")
        self.controller = master_controller
        self.set_code = ""
        self.set_info_text = StringVar(self)
        self.set_info_text.set("Current: ")
        self.sets_box = ttk.Combobox(self, width=50, height=23)
        self.set_info_label = Label(self, textvariable=self.set_info_text, justify="left", anchor="w", width=45)
        self.start_image = PhotoImage(file = r"images/start.png")
        self.start_button = Button(self, command=self.button_click_start, image = self.start_image, width=36, height=36)
        self.stop_image = PhotoImage(file = r"images/stop.png")
        self.stop_button = Button(self, command=self.button_click_stop, image = self.stop_image, width=36, height=36)
        self.settings_image = PhotoImage(file = r"images/settings.png")
        self.settings_button = Button(self, command=self.button_click_settings, image = self.settings_image, width=36, height=36)
        self.sets_box.grid(sticky="W", row=0, column=0)
        self.sets_box['values'] = self.controller.get_sets_filtered_str()
        self.set_info_label.grid(sticky="W", row=1, column=0)
        self.start_button.grid(row=0, column=1, rowspan=2, sticky="W")
        self.stop_button.grid(row=0, column=2, rowspan=2, sticky="W")
        self.settings_button.grid(row=0, column=3, rowspan=2, sticky="W")
        self.sets_box.bind("<<ComboboxSelected>>", self.set_selected)
        self.sets_box.bind("<KeyRelease>", self.set_search)

    def button_click_settings(self):
        window = settingswindow.SettingsWindow(self,self.controller)

    def button_click_stop(self):
        self.controller.set_stop()

    def button_click_start(self):
        self.master.get_images_command()

    def set_selected(self,master):
        global running
        if self.controller.get_running():
            messagebox.showinfo(title="Error",
                        message="There is currently a set loading.")
            return
        self.controller.set_running()
        code_str = self.get_code_selected()
        self.controller.update_set(code_str)
        self.master.load_cards_command(code_str)
        self.controller.get_set_langs()
        set_info = "Current: " + self.controller.get_set_name() + " | " + code_str.upper()
        self.set_info_text.set(set_info)
        self.controller.unset_running()

    def get_code_selected(self):
        selected = self.sets_box.get()
        selected = selected.split(' ')
        set_code = selected[0].lower()
        return set_code

    def set_search(self,direct):
        if len(search_entry := self.sets_box.get()) > 0:
            sets_searched = []
            for c_set in self.sets_box['values']:
                if search_entry.lower() in c_set.lower():
                    sets_searched.append(c_set)
            self.sets_box['values'] = sets_searched
        else:
            self.sets_box['values'] = self.controller.get_sets_filtered_str()

    def refresh(self):
        self.sets_box['values'] = self.controller.get_sets_filtered_str()
