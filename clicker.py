from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import sys
import time
import json

with open(sys.argv[1]) as f:
    events = json.load(f)

mouse = MouseController()
keyboard = KeyboardController()

start_time = time.time()

for j in range(int(sys.argv[2])):
    for i, event in enumerate(events):
        delay = event['timestamp'] - (events[i - 1]['timestamp'] if i > 0 else 0)
        time.sleep(delay)

        if event['type'] == 'mouse':
            x, y = event['position']
            mouse.position = (x, y)
            btn = Button.left if 'left' in event['button'] else Button.right
            if event['action'] == 'press':
                mouse.press(btn)
                print(event)
            else:
                mouse.release(btn)

        elif event['type'] == 'keyboard':
            k = event['key']
            try:
                key = getattr(Key, k.replace('Key.', '')) if k.startswith('Key.') else k
            except AttributeError:
                key = k
            if event['action'] == 'press':
                keyboard.press(key)
            else:
                keyboard.release(key)
