from pynput import mouse, keyboard
import time
import json

events = []

def on_click(x, y, button, pressed):
    events.append({
        'type': 'mouse',
        'action': 'press' if pressed else 'release',
        'button': str(button),
        'position': (x, y),
        'timestamp': time.time()
    })

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    events.append({
        'type': 'keyboard',
        'action': 'press',
        'key': k,
        'timestamp': time.time()
    })

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    events.append({
        'type': 'keyboard',
        'action': 'release',
        'key': k,
        'timestamp': time.time()
    })

print("Recording... Press ESC to stop.")
start_time = time.time()

with mouse.Listener(on_click=on_click) as mouse_listener, \
     keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    keyboard_listener.join()

# Normalize timestamps
for event in events:
    event['timestamp'] -= start_time

with open("events.json", "w") as f:
    json.dump(events, f)

print("Recording saved.")
