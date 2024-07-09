import pyautogui
import time
import keyboard
import pygetwindow as gw

# Initialize the loop control and range value
loop_enabled = False    # Whether the autocaster is enabled
range_value = 1         # Number of abilities to cycle through
loop = True             # Determines if the program should continue running or close
cycle_time = 1          # Time to cycle through all abilities (seconds)

# Function definitions

# Toggles the autocaster on or off
def toggle_loop():
    global loop_enabled
    loop_enabled = not loop_enabled
    print(f"Loop enabled: {loop_enabled}")

# Increases the number of abilities to cycle through
def increase_range():
    global range_value
    range_value += 1
    print(f"Range increased to: {range_value}")

# Decreases the number of abilities to cycle through
def decrease_range():
    global range_value
    if range_value > 1:
        range_value -= 1
    print(f"Range decreased to: {range_value}")

# Exits the program
def exit_program():
    print("Exiting program...")
    global loop
    loop = False
    exit()

# Finds the game window
def find_game_window():
    windows = gw.getWindowsWithTitle("BloonsTD6")
    if windows:
        return windows[0]
    else:
        print("Game window not found!")
        return None

# Change hotkeys
def change_hotkey(action, new_key):
    global hotkeys
    # Check if the new key is already in use
    for key in hotkeys:
        if hotkeys[key]['key'] == new_key:
            print(f"Key '{new_key}' is already assigned to another action.")
            return 0
    
    # Remove the old hotkey
    old_key = hotkeys[action]['key']
    keyboard.remove_hotkey(old_key)

    # Set the new hotkey
    hotkeys[action]['key'] = new_key
    keyboard.add_hotkey(new_key, hotkeys[action]['action'], suppress=True)
    
    print(f"Hotkey for {action} changed to '{new_key}'")
    return 1

# Hotkey definitions
hotkeys = {
    "increase_range": {
        "key": 'up',
        "action": increase_range,
        "description": "Increase the number of abilities to cycle through",
        "name": "Increase Abilities"
    },
    "decrease_range": {
        "key": 'down',
        "action": decrease_range,
        "description": "Decrease the number of abilities to cycle through",
        "name": "Decrease Abilities"
    },
    "toggle_loop": {
        "key": 'space',
        "action": toggle_loop,
        "description": "Toggle the autocaster on or off",
        "name": "Toggle Autocaster"
    },
    "exit_program": {
        "key": 'q',
        "action": exit_program,
        "description": "Exit the program",
        "name": "Exit Program"
    }
}

for key in hotkeys:
    keyboard.add_hotkey(hotkeys[key]["key"], hotkeys[key]["action"], suppress=True)   # Set up keyboard hotkeys
    print(f"Press '{hotkeys[key]['key']}' to {hotkeys[key]['description']}")          # Print instructions

# Main loop
while loop:
    if loop_enabled:
        game_window = find_game_window()                        # Find the game window
        x_base = game_window.left + (game_window.width*0.1)     # Base x coordinate for the first ability
        x_offset = game_window.width*0.0525                     # Offset between abilities
        y_base = game_window.top + (game_window.height*0.95)    # Base y coordinate for the first ability
        y_offset = game_window.height*0.08                      # Offset between rows of abilities
        c = 0
        while c < range_value:
            if not loop_enabled:
                break
            x = x_base + ((c-(12*int(c/12))) * x_offset)
            y = y_base-(y_offset*(int(c/12)))
            pyautogui.moveTo(x, y, duration=(cycle_time/(range_value+1)))
            if loop_enabled:
                pyautogui.click()
            c += 1
    time.sleep(0.1)
