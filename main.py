from pyautogui import *
import pyautogui
import keyboard
import time

from configs.config_reader import Config

point_cords = Config.get_config(0, 'coordinates').coordinates
background_color = Config.get_config(1, 'colors').background
cursor_color = Config.get_config(1, 'colors').cursor
target_color = Config.get_config(1, 'colors').target
print(background_color, cursor_color, target_color)

while 1:
    t = 0
    while keyboard.is_pressed('q'):
        c = 0
        s = 0
        for cord in point_cords:
            pixel = pyautogui.pixel(cord[0], cord[1])
            if pixel != target_color:
                c += 1
            if pixel == background_color:
                s += 1
        if s >= 7:
            if c == 10:
                click(970, 477, button='right')
                time.sleep(0.18)
            t = 0
        elif t == 0:
            click(970, 477, button='right')
            t = 1