from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import threading
import sets, controller, settingswindow, controlframe, imageframe

# Used for the stop button
hard_stop = False
splash_path = "images\\splash.png"

def donothing():
    return

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.controller = controller.Controller()
        self.title('Automatic Eureka')
        self.iconbitmap('images/ninja_icon.ico')
        self.menu_bar = MenuBar(self, self.controller)
        self.configure(menu=self.menu_bar)
        self.main_frame = MainFrame(self, self.controller)
        self.set_search_font = font.Font(self,family="Courier New",size=8)
        self.option_add("*TCombobox*Listbox*Font", self.set_search_font)
        self.main_frame.grid(row=0, column=0)

class MainFrame(Frame):
    def __init__(self, parent, master_controller):
        super().__init__(parent, height=700, width=500, bd=2)
        self.controller = master_controller
        self.controls = controlframe.ControlFrame(self, self.controller)
        self.images = imageframe.ImageFrame(self, self.controller)
        self.controls.grid(row=0, column=0)
        self.images.grid(row=1, column=0)
        
    # Called by ControlFrame to tell ImageFrame to load the set
    def load_cards_command(self,set_code):
        self.images.load_set_cards(set_code)

    # Called by ControlFrame to tell ImageFrame to start downloading
    def get_images_command(self):
        t = threading.Thread(target=self.images.start_process)
        t.start()

class MenuBar(Menu):
    def __init__(self, parent, master_controller):
        super().__init__(parent)
        self.controller = master_controller
        self.menu_file = Menu(self, tearoff=0)
        self.menu_file.add_command(label="Settings", command=self.open_settings)
        self.menu_file.add_command(label="Exit", command=parent.destroy)
        self.add_cascade(label="File", menu=self.menu_file)
        self.menu_help = Menu(self, tearoff=0)
        self.menu_help.add_command(label="About", command=self.window_about)
        self.menu_help.add_command(label="Info", command=donothing)
        self.add_cascade(label="Help", menu=self.menu_help)

    def open_settings(self):
        window = settingswindow.SettingsWindow(self.controller)

    def window_about(self):
        about_message = """Automatic Eureka by Tolarian Ninja / Alex Hartshorn-Savage

Magic: The Gathering is property of Wizards of the Coast

Scryfall data is property of Scryfall, LLC

Scrython library by NandaScott
"""
        messagebox.showinfo(title="About Scryfall Image Downloader",
                        message=about_message)

root = MainWindow()
root.mainloop()
