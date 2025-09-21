#-------------------------- gui - tkinter --------------------------
import tkinter as tk
from tkinter import LEFT, RIGHT

root = tk.Tk() # create a window
root.title("Clipboard Manager") # set window title
root.geometry("350x620") # set window size
root.minsize(350, 620)

# Let column 0 (where entries will expand) grow with the window.
root.grid_columnconfigure(0, weight=1)

# --------------------------- TITLE ------------------------------------------
title = tk.Label(
    root,
    text="Clipboard-Manager",
    anchor=tk.CENTER,        # text alignment inside the label
    bd=4,
    font=("Bauhaus 93", 28),
    fg="black",
    bg="#cfcfcf",
    justify="center",
    relief=tk.RAISED,
    underline=0,
    padx=25,                 # internal padding
    pady=20
)
title.grid(row=0, column=0, columnspan=3, padx=5, pady=(18, 12), sticky="ew")

# Thin separator under the title
separator = tk.Frame(root, height=2, bg="#737272")
separator.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="ew")

# ------------------------- BODY(THE FORM) ---------------------------------
# ------------------------- LOAD IMAGE ---------------------------

try:
    icon_image = tk.PhotoImage(file="undo-icon-20.png")
except tk.TclError:
    print("Error: 'icon.png' not found or invalid image file. Please provide a valid PNG image.")
    # Create a dummy image if the file is not found to avoid errors
    icon_image = tk.PhotoImage(width=1, height=1) 
    
# ------------------------- FORM STATE (variables) ---------------
invoice_number = tk.StringVar()
invoice_date   = tk.StringVar()
payment_terms  = tk.StringVar()
total_amount   = tk.StringVar()
po_number      = tk.StringVar()
buyer_name     = tk.StringVar()
# ------------------------- CREATE ROWS(Fields) ------------------
fields = ['Invoice Number', 'Invoice Date', 'Payment Terms', 'Total Amount', 'PO Number', 'Buyer Name']
text_vars = [invoice_number, invoice_date, payment_terms, total_amount, po_number, buyer_name]
for i, field in enumerate(fields):
    base = 2 + i*2
    lbl = tk.Label(root, text=field, font=("Aharoni", 13))
    lbl.grid(row=base, column=0, padx=20, pady=(8, 2), sticky="w")

    button = tk.Button(
    root, image=icon_image, width=20, height=20,
    command=None)
    button.grid(row=base, column=2, padx=(0, 20), pady=(8, 2), sticky="e")

    entry = tk.Entry(root, textvariable=text_vars[i], font=("Arial", 12))
    entry.grid(row=base+1, column=0, columnspan=3, padx=20, pady=(0, 8), sticky="ew")
# ------------------------- SEND BUTTON --------------------------
send_btn = tk.Button(
    root, text="SEND", font=("Aharoni", 14, "bold"), pady=8,
    command=None)

send_btn.grid(row=14, column=0, columnspan=3, padx=20, pady=22, sticky="ew")



#-------------------------- core - keyboard, mouse, clipboard --------------------------
import keyboard, mouse, pyperclip, time, threading

# global variables
copy_mode = False
exit_event = threading.Event()
fields_queue = text_vars.copy()[::-1]  # make a reverse copy of the list to use as a queue

# single copy and append to field
def copy_and_append():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)  # slight delay to ensure clipboard is updated
    text = pyperclip.paste()

    fields_queue[0].set(text)
    print(f"{fields_queue[0]}: {text}") # for debug
    fields_queue.pop()

# undo and enqueue the field
def undo_button(field_var):
    field_var.set("")
    fields_queue.append(field_var)


# Mouse thread function
def on_double_click():
    if (copy_mode and not exit_event.is_set()):
        copy_and_append()

def toggle_copy():
    global copy_mode
    copy_mode = not copy_mode
    print("Copy Mode", "ON" if copy_mode else "OFF")

def request_exit():
    exit_event.set()

def main():
    # main thread install hooks
    handler1 = mouse.on_double_click(on_double_click)
    keyboard.add_hotkey('shift+1', toggle_copy, suppress=True)
    keyboard.add_hotkey('esc', request_exit, suppress=True)

    print("Hello Roncha")
    print("Shift+1 = toggle copy mode, ESC = exit")

    try:
        exit_event.wait()  # main thread idles; callbacks still fire
    finally:
        # cleanup happens in main thread
        mouse.unhook(handler1)
        keyboard.unhook_all_hotkeys()
        print("Clean exit.")
        # print("Copied items:", text)

# main()
# root.mainloop() # run the window loop



#-------------------------- old version --------------------------




# import tkinter
# from tkinter import Scrollbar, Listbox, RIGHT, Y, END, LEFT, BOTH , TOP
# root = tkinter.Tk() # create a window
# root.title("Clipboard Manager") # set window title
# root.geometry("500x700") # set window size
# root.label = tkinter.Label(root, text="Hello Roncha\nShift+1 = toggle copy mode\nESC = exit", font=("David", 20), justify='left')
# root.label.pack()
# scrollbar = Scrollbar(root) # create a scrollbar widget for the listbox
# scrollbar.pack(side=TOP, fill=tkinter.X) # side - position the scrollbar in the window, fill - how to fill the scrollbar, using axis - X or Y or BOTH
# #why in scrollbar.pack there is no parent? because scrollbar is already a child of root,
# # can scrollbar be a child of mylist? no, because scrollbar is not a container widget
# mylist = Listbox(root, yscrollcommand=scrollbar.set) # create a listbox widget with the scrollbar attached using yscrollcommand, whenever the listbox’s visible region changes (you scroll, resize, select, etc.), Tkinter calls scrollbar.set(lo, hi) so the thumb position updates.
# # mylist.insert(END, "Copied items will appear here")
# mylist.pack(side=LEFT, fill=BOTH) #pack with no parent is default to root
# scrollbar.config(command=mylist.yview) # configure the scrollbar to call mylist.yview when the scrollbar is moved, so the listbox scrolls accordingly
# root.button1 = tkinter.Button(root, text="add", font=("David", 20), command=lambda: mylist.insert(END, "NEW ITEM"))
# root.button2 = tkinter.Button(root, text="add", font=("David", 20), command=lambda: mylist.insert(END, "NEW ITEM"))
# root.button3 = tkinter.Button(root, text="add", font=("David", 20), command=lambda: mylist.insert(END, "NEW ITEM"))

# root.button1.pack(side=LEFT)
# root.button2.pack(side=RIGHT)
# root.button3.pack(side=TOP)

# root.mainloop() # run the window loop

''' - old version -
# power - מפעיל ואז מתחיל רצף של פעולות עכבר
# copy_and_append - הפונקציה שpower ישתמש
text = []
power = True
copy_mode = False
fields = ['Invoice Number', 'Invoice Date', 'Payment Terms', 'Total Amount', 'PO Number', 'Currency', 'Buyer Name']
pointer = 0

# wait for the starting cue - Shift+1
def start():
    print("Hello Roncha")
    print("press Shift+1 to start")
    keyboard.wait('shift+1')
    print("press Esc to stop")

# toggle power state and hook/unhook mouse events
def power_toggle():
    global power
    power = not power
    if power:
        print("Power ON")
    else:
        print("Power OFF")
        print(text)

# toggle copy mode state
def copy_mode_toggle():
    global copy_mode
    copy_mode = not copy_mode
    print("Copy Mode " + ("ON" if copy_mode else "OFF"))

# single copy and append to list
def copy_and_append():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)  # slight delay to ensure clipboard is updated
    text.append(pyperclip.paste())
    print(f"copied #{len(text)}") # for debug

def runAll():
    global power, copy_mode
    keyboard.add_hotkey('shift+1', lambda: copy_mode_toggle())
    keyboard.add_hotkey('esc', lambda: power_toggle())

    start()
    while power:
        while copy_mode:
            mouse.wait('left','double')
            copy_and_append()
        print("press Shift+1 to start again or Esc to exit")
        keyboard.wait('shift+1' or 'esc')

runAll()
'''

