from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

class HelpWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Settings Information")
        self.geometry('640x320')
        self.iconbitmap('images/settings.ico')
        self.image = ImageTk.PhotoImage(Image.open('images/setting_info.png'))
        self.image_label = Label(self, image=self.image)
        self.image_label.pack()
