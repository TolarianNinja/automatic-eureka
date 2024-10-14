from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
from sys import platform

class HelpWindow(Toplevel):
    def __init__(self,home_directory):
        Toplevel.__init__(self)
        self.title("Settings Information")
        self.geometry('640x320')
        if platform == "win32":
            self.iconbitmap(home_directory + '/images/settings.ico')
        else:
            self.iconbitmap(home_directory + '/images/settings.ico')
        self.image = ImageTk.PhotoImage(Image.open(home_directory + '/images/setting_info.png'))
        self.image_label = Label(self, image=self.image)
        self.image_label.pack()
