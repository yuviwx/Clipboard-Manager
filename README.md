# 📋 Clipboard Manager (Tkinter GUI)

A user-friendly clipboard automation tool written in Python with a clean **GUI–Core** architecture.  
Designed for quickly copying structured information (like invoice details) into a CSV file using double-click detection and hotkeys.

This is the **latest architecture**, matching your refactored version with OOP, 3-file layout, threading separation, undo, CSV creation, and existing-file selection.

---

## 🚀 Features

### 🖱 Clipboard Automation
- **Double-click to copy**: While in Copy Mode, any double-click anywhere copies the selected text and sends it to the next empty field.
- **Shift + 1** toggles Copy Mode **ON/OFF**.
- **ESC** cleanly exits the application.

### 📝 & 💾 GUI Features
- **Smart Form Filling** - Each field has its own label and undo button. All fields reset after every successful “SEND”.
- **Intelligent CSV Handling** - Automatically creates or opens a CSV on the first “SEND”, with header columns matching your form fields.
- **Menu bar** - Includes options to create/open a CSV file, view instructions, or open the contact dialog.


### 🧵 Multi-Threading Architecture
- Runs in a **multi-threaded environment** with clear separation of concerns:
  - Background threads created by `keyboard` and `mouse` libraries handle system-level hooks.
  - The Tkinter main thread manages all GUI updates.
- A **thread lock** protects the shared field queue.
- Thread communication is done through a `queue`, `shared state`, and a `threading.Event`. 

### 📦 Clean 3-File OOP Structure

```
project/
├── gui.py     → Tkinter GUI (widgets, menu, fields, buttons)
├── core.py    → Logic (copy mode, hooks, queue, CSV I/O)
└── main.py    → Application entry point and wiring
```

---

## 🧩 Future Ideas

- Status bar: show “Copy Mode ON/OFF”
- Track which field is currently active  
- Add theme selection / dark mode  
- Add small pop window for minimize state  
- Add config file for persistent preferences  
