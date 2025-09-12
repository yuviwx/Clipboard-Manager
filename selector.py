import keyboard, mouse, pyperclip, time, threading

# global variables
text = []
copy_mode = False
exit_event = threading.Event()

# single copy and append to list
def copy_and_append():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)  # slight delay to ensure clipboard is updated
    text.append(pyperclip.paste())
    print(f"copied #{len(text)}") # for debug

# Mouse thread function
def on_mouse(e):
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
    handler = mouse.on_double_click(on_mouse)
    keyboard.add_hotkey('shift+1', toggle_copy, suppress=True)
    keyboard.add_hotkey('esc', request_exit, suppress=True)

    print("Hello Roncha")
    print("Shift+1 = toggle copy mode, ESC = exit")

    try:
        exit_event.wait()  # main thread idles; callbacks still fire
    finally:
        # cleanup happens in main thread
        mouse.unhook(handler)
        keyboard.unhook_all_hotkeys()
        print("Clean exit.")
        print("Copied items:", text)

if __name__ == "__main__":
    main()


    
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

