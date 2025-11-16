#-------------------------- core - keyboard, mouse, clipboard --------------------------

import keyboard, mouse, pyperclip, time, threading, csv, os
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

class ClipboardManagerCore:
    def __init__(self, gui):
        self.gui = gui
        self.copy_mode = False
        self.exit_event = threading.Event()
        self.csv_path = None

        # queue of (name, StringVar), reversed for easy pop()
        self.fields_queue = [
            (f["name"], f["var"])
            for f in gui.text_fields
        ][::-1]

        self.fields_lock = threading.Lock()
        self._mouse_handler = None
        

    # --- wiring input hooks ---

    def install_hooks(self):
        self._mouse_handler = mouse.on_double_click(self._on_double_click)
        keyboard.add_hotkey('shift+1', self.toggle_copy, suppress=True)
        keyboard.add_hotkey('esc', self.request_exit, suppress=True)

    
    def cleanup(self):
        if self._mouse_handler is not None:
            mouse.unhook(self._mouse_handler)
        keyboard.unhook_all_hotkeys()
        print("Clean exit.")

    # --- mouse / keyboard callbacks ---
    def toggle_copy(self):
        self.copy_mode = not self.copy_mode
        print("Copy Mode", "ON" if self.copy_mode else "OFF")

    def _on_double_click(self):
        """
            Runs in hook thread.
            - chooses the target field (pops queue)
            - does Ctrl+C + sleep + clipboard
            - then schedules var.set(text) on GUI thread
        """

        # Check Conditions
        if not self.copy_mode or self.exit_event.is_set():
            return
        
        with self.fields_lock:
            if not self.fields_queue:
                print("All fields are filled.")
                return
            name, var = self.fields_queue.pop()

        # Perform Copy
        keyboard.press_and_release('ctrl+c') 
        time.sleep(0.05)
        text = pyperclip.paste()

        if not text or text.strip() == "":
            print("No text copied.")
            # put back the field
            with self.fields_lock:
                self.fields_queue.append((name, var))
            return

        # Schedule the GUI update on Tk thread
        self.gui.root.after(0, lambda v=var, t=text: v.set(t))

    def undo_button(self, field_tuple):
        """
        Called from GUI (Tk thread).
        We clear the var and put it back into the queue safely.
        """
        if not field_tuple or field_tuple[1].get() == "":
            return  # nothing to undo
        
        name, var = field_tuple
        var.set("")

        with self.fields_lock:
            self.fields_queue.append((name, var))
    
    def on_send(self):
        """
        Called from the SEND button (Tk thread).
        Validates fields, ensures CSV exists, appends row, clears form.
        """
        missing = self._missing_fields()
        if missing:
            messagebox.showwarning(
                "Incomplete",
                "Please fill in all fields before sending.\nMissing: " + ", ".join(missing)
            )
            return

        # First time: ask user for CSV path (new or existing)
        if not self._ensure_csv_path():
            # user cancelled
            return

        # Make sure file exists / has header
        if not self._ensure_csv_exists():
            return

        self._append_to_csv()

    
    def request_exit(self):
        self.exit_event.set()
        self.gui.root.after(0, self.gui.root.destroy)

#-------------------------------- CSV Handling --------------------------------------
    
    def _missing_fields(self):
        """Return a list of field names that are still empty."""
        return [
            field["name"]
            for field in self.gui.text_fields
            if not field["var"].get().strip()
        ]
    
    def _is_complete(self):
        """Check if all fields are filled."""
        return len(self._missing_fields()) == 0

    def _ensure_csv_path(self):
        """
        Make sure self.csv_path is set.
        On first call, ask the user if they want an existing file or a new one.
        Returns True if a path is available, False if the user cancelled.
        """
        if self.csv_path:
            return True

        use_existing = messagebox.askyesno(
            "CSV file",
            "Do you want to use an existing CSV file?\n\n"
            "Yes  → choose an existing file\n"
            "No   → create a new file"
        )

        if use_existing:
            self.open_csv_file()
        else:
            self.new_csv_file()

        return self.csv_path is not None


    def _ensure_csv_exists(self) -> bool:
        """
        Create the CSV file with headers if it doesn't exist or is empty.
        Returns False if creation failed.
        """
        path = self.csv_path
        try:
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                self._create_csv()
        except OSError as e:
            messagebox.showerror("File error", f"Could not access CSV file:\n{e}")
            return False
        return True

    def _create_csv(self):
        headers = [field["name"] for field in self.gui.text_fields]
        try:
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=headers).writeheader()
        except PermissionError:
            messagebox.showerror(
                "Creation failed",
                "The CSV file is open in another program (e.g., Excel).\n"
                "Close it and try again."
            )
        except Exception as e:
            messagebox.showerror("Creation failed", f"Could not create CSV:\n{e}")

    def _append_to_csv(self):
        """Append a row to CSV with the current entries, then clear and reset queue."""
        headers = [field["name"] for field in self.gui.text_fields]
        row = {field["name"]: field["var"].get() for field in self.gui.text_fields}

        try:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=headers).writerow(row)

        except PermissionError:
            messagebox.showerror(
                "Send failed",
                "The CSV file is open in another program (e.g., Excel).\n"
                "Close it and try again."
            )
            return
        except Exception as e:
            messagebox.showerror("Send failed", f"Could not write CSV:\n{e}")
            return

        # Clear fields
        for field in self.gui.text_fields:
            field["var"].set("")

        # Reset queue (so new copies start at the first field)
        with self.fields_lock:
            self.fields_queue = [
                (field["name"], field["var"])
                for field in self.gui.text_fields
            ][::-1]

        messagebox.showinfo("Saved", f"Row appended to:\n{os.path.realpath(self.csv_path)}")


    def new_csv_file(self):
            """
            Menu action: ask user for a new CSV file path and create it with headers.
            """
            path = filedialog.asksaveasfilename(
                title="Create new CSV file",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if not path:
                # user cancelled
                return

            self.csv_path = path
            # Create (or truncate) the file with headers
            self._create_csv()
            messagebox.showinfo("CSV file", f"New CSV created:\n{os.path.realpath(path)}")

    def open_csv_file(self):
        """
        Menu action: ask user to choose an existing CSV file.
        """
        path = filedialog.askopenfilename(
            title="Select existing CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not path:
            # user cancelled
            return

        self.csv_path = path
        messagebox.showinfo("CSV file", f"Using existing CSV:\n{os.path.realpath(path)}")
