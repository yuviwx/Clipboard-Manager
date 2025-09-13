# Clipboard Manager

A simple Python script that allows you to capture and store and export(Future) text copied to the clipboard.

## Features

- **Toggle Copy Mode**: Easily switch between capturing and normal mode.
- **Capture on Double-Click**: When in copy mode, double-clicking the mouse automatically copies the selected text and appends it to a list.
- **Non-blocking Operation**: The script uses multithreading to listen for mouse and keyboard events without blocking the main program flow.
- **Easy Exit**: Press `ESC` to gracefully exit the application.

## How it Works

The application uses a multithreaded approach to handle user input. The `main` function sets up global keyboard and mouse hooks to listen for specific events.

- A keyboard hotkey (`Shift+1`) is configured to toggle the `copy_mode`.
- Another hotkey (`ESC`) is used to set an `exit_event`, signaling the main thread to terminate.
- A double-click mouse event is hooked to the `on_mouse` function, which, when `copy_mode` is active, triggers a copy operation and appends the content to a list.

### Multithreading and Thread Communication

This script leverages Python's `threading` module to achieve its non-blocking behavior.

- The `keyboard` and `mouse` libraries internally create separate threads to monitor input events. This allows the main program to "idle" (`exit_event.wait()`) while the event-driven callbacks (like `on_mouse` and `toggle_copy`) are executed on these background threads.
- **Thread Communication** is managed through global variables and a `threading.Event` object.
    - The `copy_mode` global variable acts as a flag that is toggled by the `toggle_copy` function and read by the `on_mouse` function.
    - The `exit_event` is a thread-safe way to signal from the keyboard thread (via `request_exit`) to the main thread that the program should terminate. This is a clean method for thread synchronization, ensuring a proper cleanup.

## Requirements

The following Python libraries are required to run this script:

- `keyboard`: For listening to and handling global keyboard events.
- `mouse`: For listening to and handling global mouse events.
- `pyperclip`: For interacting with the system clipboard.
- `threading`: A built-in Python library used for creating and managing threads.
- `time`: A built-in Python library for time-related functions, used here to introduce a small delay.

You can install the required external libraries using `pip`:

```bash
pip install keyboard mouse pyperclip
