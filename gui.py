from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import sets, controller

root = Tk()
root.title('Automatic Eureka')
root.iconbitmap('images/ninja_icon.ico')

eris = controller.Controller()


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

def generate_set_menu():
    set_list = sets.get_sets_full()
    set_names = []
    current_output = ""
    for current_set in set_list:
        current_output = str(current_set[1]["code"] + " - " + current_set[1]["name"])
        set_names.append(current_output)
    return set_names

def get_menu_set_code(set_menu):
    selection = set_menu.get()
    selection = selection.split()
    code = selection[0]
    return code

def button_click_start(set_menu):
    set_code = get_menu_set_code(set_menu)
    set_menu
    

menu_bar = Menu(root)
filemenu = Menu(menu_bar, tearoff=0)
filemenu.add_command(label="Config (WIP)", command=donothing)
filemenu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menu_bar, tearoff=0)
helpmenu.add_command(label="Documentation (WIP)", command=donothing)
helpmenu.add_command(label="About", command=window_about)
menu_bar.add_cascade(label="Help", menu=helpmenu)

main_frame = Frame(root, height=700, width=500, bd=2)
main_frame.pack()

frame_top = LabelFrame(main_frame, width=450, bd=2, text="Options")
frame_top.grid(row=0, column=0)

start_image = PhotoImage(file = r"images/start.png")

set_search_font = font.Font(root,family="Courier New",size=8)
root.option_add("*TCombobox*Listbox*Font", set_search_font)

menu_value = StringVar(frame_top)
menu_value.set("Select a set")
sets_list = eris.get_sets_str()
sets_box = ttk.Combobox(frame_top, width = 64, height = 23)
sets_box['values'] = sets_list
sets_box.grid(row=0, column=0, columnspan=3)

get_set_button = Button(frame_top, image = start_image, width=29, height=36, pady=2)
get_set_button.grid(row=0, column=3)

frame_bottom = LabelFrame(main_frame, width=450, height=630, bd=2, text="Downloaded Image")
frame_bottom.grid(row=1, column=0)

side_image = ImageTk.PhotoImage(Image.open("images/splash.png").resize((430,600)))

image_label = Label(frame_bottom, image=side_image, height=615, width=441)
image_text_label = Label(frame_bottom, text="Image downloaded.")

image_label.grid(row=0, column=0)
image_text_label.grid(row=1, column=0)

root.config(menu=menu_bar)
root.mainloop()
