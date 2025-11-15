#-------------------------- GUI - tkinter ------------------------------------------

import tkinter as tk
from tkinter import LEFT, RIGHT

help_text = ("Instructions:\n\n"
             "1. Press Shift + 1 to toggle Copy Mode ON/OFF.\n"
             "2. When Copy Mode is ON, double-clicking the mouse will copy the selected text\n"
             "   and paste it into the next available field in the form.\n"
             "3. To undo the last entry in a field, click the undo button next to it.\n"
             "4. Press send to submit the form and export to cvs file.\n"
             "   each time you press send, a new entry will be appended.\n"
             "5. Press Esc to exit the application.\n")

class ClipboardManagerGUI:
    def __init__(self):
        self.root = self._create_root()
        self._build_menu()
        self._create_title()
        self.icon_image = self._load_icon()

        # list of dicts: {name, var, undo_button}
        self.text_fields = self._create_form_fields()
        self.send_button = self._create_send_button()

        #self.core - None  # to be set later

    def set_core(self, core):
        """Connect core logic after both objects are created"""
        self.core = core

        # wire UNDO buttons
        for field in self.text_fields:
            name  = field["name"]
            var   = field["var"]
            btn   = field["undo_button"]
            btn.config(
                command=lambda field_tuple=(name, var): self.core.undo_button(field_tuple)
            )

        # wire SEND button
        self.send_button.config(command=None)  # to be implemented

    def run(self):
        self.root.mainloop()

    def _create_root(self):
        root = tk.Tk()
        root.title("Clipboard Manager")
        root.geometry("350x620")
        root.minsize(350, 620)
        root.grid_columnconfigure(0, weight=1)
        return root
    
    def _build_menu(self):
        # add a menu bar with an help and Exit options
        menubar = tk.Menu(self.root)

        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='File', menu = file)
        file.add_command(label ='New CVS', command = None)
        file.add_command(label ='Open CVS', command = None)
        file.add_separator()
        file.add_command(label ='Exit', command = None)

        # Adding Help Menu
        help_ = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Help', menu = help_)
        help_.add_command(label ='Instructions', command = self._show_help)
        help_.add_command(label ='Contact Roncha', command = None)

        self.root.config(menu = menubar)
    
    def _show_help(self):
        tk.messagebox.showinfo("Help", help_text)

    def _create_title(self):
        title = tk.Label(
            self.root,
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
        separator = tk.Frame(self.root, height=2, bg="#737272")
        separator.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="ew")

    def _load_icon(self):
        try:
            icon_image = tk.PhotoImage(file="./icons/undo-icon-20.png")
        except tk.TclError:
            print("Error: 'undo-icon-20.png' not found or invalid image file. Please provide a valid PNG image.")
            # Create a dummy image if the file is not found to avoid errors
            icon_image = tk.PhotoImage(width=1, height=1) 
        return icon_image
    
    def _create_form_fields(self):

        invoice_number = tk.StringVar()  
        invoice_date   = tk.StringVar()
        payment_terms  = tk.StringVar()
        total_amount   = tk.StringVar()
        po_number      = tk.StringVar()
        buyer_name     = tk.StringVar()

        text_vars = [
            ("invoice_number",  invoice_number),
            ("invoice_date",    invoice_date),
            ("payment_terms",   payment_terms),
            ("total_amount",    total_amount),
            ("po_number",       po_number),
            ("buyer_name",      buyer_name)
        ]

        fields = []
        for i, (field_name, text_var) in enumerate(text_vars):
            base = 2 + i*2

            lbl = tk.Label(self.root, text=field_name, font=("Aharoni", 13))
            lbl.grid(row=base, column=0, padx=20, pady=(8, 2), sticky="w")

            undo_button = tk.Button(
                self.root, 
                image=self.icon_image, 
                width=20, 
                height=20,
                command= None 
            ) 
            undo_button.grid(row=base, column=2, padx=(0, 20), pady=(8, 2), sticky="e")

            entry = tk.Entry(self.root, textvariable=text_var, font=("Arial", 12))
            entry.grid(
                row=base+1, 
                column=0, 
                columnspan=3, 
                padx=20, 
                pady=(0, 8), 
                sticky="ew"
            )

            fields.append(
                {
                "name": field_name,
                "var": text_var,
                "undo_button": undo_button,
                "label": lbl,
                "entry": entry
                }
            )
        return fields

    def _create_send_button(self):
        send_btn = tk.Button(
            self.root, 
            text="SEND", 
            font=("Aharoni", 14, "bold"), 
            pady=8,
            command=None)   

        send_btn.grid(row=14, column=0, columnspan=3, padx=20, pady=22, sticky="ew")          
        return send_btn
    
# #test
# gui = ClipboardManagerGUI()
# gui.run()