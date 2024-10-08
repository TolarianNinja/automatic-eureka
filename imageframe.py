from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import threading
import sets, controller

splash_path = "images\\splash.png"
hard_stop = False

class ImageFrame(LabelFrame):
    def __init__(self, parent, master_controller):
        super().__init__(parent, height=630, bd=2, text="Downloaded Image")
        self.controller = master_controller
        self.image = ImageTk.PhotoImage(Image.open(splash_path).resize((430,600)))
        self.image_label = Label(self, image=self.image, height=615, width=440)
        self.image_text_string = StringVar(self)
        self.image_text_string.set("Select a set from the drop down to begin.")
        self.image_text_label = Label(self, textvariable=self.image_text_string)
        self.progress_bar = ttk.Progressbar(self, length=445)
        self.image_label.grid(row=0, column=0)
        self.image_text_label.grid(row=1, column=0)
        self.progress_bar.grid(row=2, column=0)

    def load_set_cards(self,set_code):
        page = 1
        self.progress_bar['maximum'] = self.controller.get_page_count()
        self.image_text_string.set("Loading cards from " + self.controller.get_set_name())
        while len(self.controller.get_card_list()) < self.controller.get_set_size():
            self.controller.get_set_cards(set_code,page)
            self.progress_bar.step(1)
            self.progress_bar.update()
            if (page * 175) < self.controller.get_set_size():
                page = page + 1
            else:
                self.image_text_string.set(self.controller.get_set_name() + " is ready to download.")
                break

    def start_process(self):
        global hard_stop
        card_name = ""
        self.progress_bar['value'] = 0
        if len(self.controller.get_card_list()) == 0:
            messagebox.showinfo(title="Error",
                        message="There are no cards loaded.")
            return
        if not self.controller.get_include_digital() and self.controller.get_current_set()["digital"]:
            messagebox.showinfo(title="Error",
                                message="Digital sets can't be downloaded when downloading digital cards is turned off.  Update your settings to download this set.")
        download_path = self.controller.build_folders()
        self.progress_bar['maximum'] = self.controller.get_set_size()
        for card in self.controller.get_card_list():
            if not self.controller.is_stop():
                if card["digital"] and self.controller.get_include_digital() == 0:
                    continue
                card_name = self.controller.download_image(card,download_path)
                if card_name == "":
                    self.image_text_string.set("Error when downloading (check console)" + card_name)
                    self.image_text_label.update()
                else:
                    card_path = self.controller.get_lang_path(card,download_path) + card_name
                    self.update_image(self.image_label,card_path,self.controller.get_image_size())
                    self.image_text_string.set("Downloaded " + card_name)
                    self.image_text_label.update()
                self.progress_bar.step(1.0)
            else:
                break
        if self.controller.is_stop():
            complete_text = "Download process stopped after " + card_name + "."
            self.controller.unset_stop()
        else:
            complete_text = "Download of " + self.controller.get_set_name() + " completed successfully."
        self.progress_bar['value'] = 0
        self.image_text_string.set(complete_text)
        self.controller.go_home()
        self.update_image(self.image_label,splash_path,"large")
        
    def update_image(self,image_label,path,size):
        if size == "art_crop":
            card_image = Image.open(path).resize((430,314))
        else:
            card_image = Image.open(path).resize((430,600))
        tk_image = ImageTk.PhotoImage(card_image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image
