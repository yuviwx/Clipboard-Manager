#-------------------------- core - keyboard, mouse, clipboard --------------------------

import keyboard, mouse, pyperclip, time, threading

class ClipboardManagerCore():
    def __init__(self, gui):
        self.gui = gui
        self.copy_mode = False
        self.exit_event = threading.Event()

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
    
    def request_exit(self):
        self.exit_event.set()
        self.gui.root.after(0, self.gui.root.destroy)


