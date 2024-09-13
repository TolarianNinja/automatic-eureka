from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from PIL import ImageTk,Image
import sets, controller

root = Tk()
root.title('Automatic Eureka')
root.iconbitmap('images/ninja_icon.ico')

# Eris stores all the data and calls all the methods for that data
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

def button_click_start():
    eris.execute()

def button_click_new():
    

def set_selected(self):
    set_code_text.set(get_code_selected())
    code_str = set_code_text.get()
    eris.update_set(code_str)
    set_info = "Name: " + eris.get_set_name() + " | Set Code: " + code_str.upper() + " | Set Size: " + str(eris.get_set_size())
    set_info_text.set(set_info)
    
def get_code_selected():
    selected = sets_box.get()
    selected = selected.split(' ')
    set_code = selected[0].lower()
    return set_code

def set_box_select_all():
    sets_box['values'] = sets_list

def set_box_select_filter():
    sets_box['values'] = sets_list_filtered


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
frame_top = LabelFrame(main_frame, width=450, bd=2, text="Options")
frame_top.grid(row=0, column=0)

set_code_text = StringVar(frame_top)
#set_size_text = StringVar(frame_top)
#set_name_text = StringVar(frame_top)

set_info_text = StringVar(frame_top)
set_info_text.set("Set Name: " + eris.get_set_name() + " | Set Code: "
                  + eris.get_set_code().upper() + " | Set Size: " + str(eris.get_set_size()))

# Combobox With List of Sets
sets_box = ttk.Combobox(frame_top, width = 64, height = 23)
sets_box['values'] = sets_list
set_search_font = font.Font(root,family="Courier New",size=8)
root.option_add("*TCombobox*Listbox*Font", set_search_font)

# Info Label for Selected Set
set_info_label = Label(frame_top, width=39, textvariable=set_info_text, justify="left", anchor="w")

# RadioButton for selecting filtered or not
radio_all = Radiobutton(frame_top, text = "All Sets", value = "all")
radio_filtered = Radiobutton(frame_top, text = "Filtered", value = "filtered")

# Start Button
start_image = PhotoImage(file = r"images/start.png")
get_set_button = Button(frame_top, command=button_click_start, image = start_image, width=29, height=36, pady=2)

# Events
sets_box.bind("<<ComboboxSelected>>", set_selected)
#radio_all.bind("<<RadiobuttonSelected>>", set_box_select_all)
#radio_filtered.bind("<<RadiobuttonSelected>>", set_box_select_filter)

# Top Frame Grid Sets
sets_box.grid(row=0, column=0, columnspan=4)
set_info_label.grid(sticky = "W", row=1, column=0, columnspan=2)
#radio_all.grid(row=1, column=2)
#radio_filtered.grid(row=1, column=3)
get_set_button.grid(row=0, column=4, rowspan=2)

# Bottom Frame
frame_bottom = LabelFrame(main_frame, width=450, height=630, bd=2, text="Downloaded Image")
frame_bottom.grid(row=1, column=0)

# Image Pane
side_image = ImageTk.PhotoImage(Image.open("images/splash.png").resize((430,600)))
image_label = Label(frame_bottom, image=side_image, height=615, width=441)

# Info Label for Downloaded Image
image_text_label = Label(frame_bottom, text="Image downloaded.")

# Bottom Frame Grid Sets
image_label.grid(row=0, column=0)
image_text_label.grid(row=1, column=0)

root.config(menu=menu_bar)
root.mainloop()
