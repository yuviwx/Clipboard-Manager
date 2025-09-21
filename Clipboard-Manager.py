#-------------------------- GUI - tkinter ------------------------------------------
import tkinter as tk
from tkinter import LEFT, RIGHT

root = tk.Tk() 
root.title("Clipboard Manager") 
root.geometry("350x620") 
root.minsize(350, 620)

# Let column 0 (where entries will expand) grow with the window.
root.grid_columnconfigure(0, weight=1)

# --------------------------- TITLE ----------------------------------------
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
text_vars = [
    ("invoice_number",  invoice_number),
    ("invoice_date",    invoice_date),
    ("payment_terms",   payment_terms),
    ("total_amount",    total_amount),
    ("po_number",       po_number),
    ("buyer_name",      buyer_name)
]
for i, (field_name, text_var) in enumerate(text_vars):
    base = 2 + i*2
    lbl = tk.Label(root, text=field_name, font=("Aharoni", 13))
    lbl.grid(row=base, column=0, padx=20, pady=(8, 2), sticky="w")

    button = tk.Button(
    root, image=icon_image, width=20, height=20,
    command= lambda field_tuple=(field_name, text_var): undo_button(field_tuple))
    button.grid(row=base, column=2, padx=(0, 20), pady=(8, 2), sticky="e")

    entry = tk.Entry(root, textvariable=text_var, font=("Arial", 12))
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
    """Run on Tk thread."""
    global fields_queue
    if not fields_queue:
        print("All fields are filled.")
        return
    
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)  # slight delay to ensure clipboard is updated
    text = pyperclip.paste()
    name, var = fields_queue.pop()
    var.set(text)
    # print(f"{name}: {var.get()}")  # debug

# undo and enqueue the field
def undo_button(field_tuple):
    name, var = field_tuple
    var.set("")
    fields_queue.append((name, var))

# Mouse thread function
def on_double_click():
    if copy_mode and not exit_event.is_set():
        # switch to Tk thread for UI/vars update
        # root.after(0, copy_and_append)
        copy_and_append()

def toggle_copy():
    global copy_mode
    copy_mode = not copy_mode
    print("Copy Mode", "ON" if copy_mode else "OFF")

def request_exit():
    exit_event.set()
    # destroy window from Tk thread
    root.after(0, root.destroy)

def main():
    # main thread install hooks
    handler1 = mouse.on_double_click(on_double_click)
    keyboard.add_hotkey('shift+1', toggle_copy, suppress=True)
    keyboard.add_hotkey('esc', request_exit, suppress=True)
    
    try:
        root.mainloop()  # run the window loop
    finally:
        # cleanup happens in main thread
        mouse.unhook(handler1)
        keyboard.unhook_all_hotkeys()
        print("Clean exit.")

if __name__ == "__main__":
    main()

