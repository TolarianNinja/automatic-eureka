from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

root = Tk()
root.title('Scryfall Image Downloader')
root.iconbitmap('images/ninja_icon.ico')

def donothing():
    return

def window_about():
    messagebox.showinfo(title="About Scryfall Image Downloader", message="Programmed by TolarianNinja / Alex Hartshorn-Savage")

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

menu_value = StringVar(frame_top)
menu_value.set("Select a set")
sets_list = ["Arabian Nights", "Antiquities", "Legends", "The Dark", "Fallen Empires"]
sets_menu = OptionMenu(frame_top, menu_value, *sets_list)
sets_menu.config(width=14)
sets_menu.grid(row=0, column=0)

get_set_button = Button(frame_top, text="Set Information", width=14, pady=2)
get_set_button.grid(row=0, column=1)

button_configure_boosterfun = Button(frame_top, text="Booster Fun", width=14, pady=2)
button_configure_boosterfun.grid(row=0, column=2)

button_configure_multiples = Button(frame_top, text="Multiple Arts", width=14, pady=2)
button_configure_multiples.grid(row=0, column=3)

frame_bottom = LabelFrame(main_frame, width=450, height=630, bd=2, text="Downloaded Image")
frame_bottom.grid(row=1, column=0)

side_image = ImageTk.PhotoImage(Image.open("images/Nightmare.jpg").resize((430,600)))

image_label = Label(frame_bottom, image=side_image, height=615, width=441)
image_text_label = Label(frame_bottom, text="Image downloaded.")

image_label.grid(row=0, column=0)
image_text_label.grid(row=1, column=0)

root.config(menu=menu_bar)
root.mainloop()
