from PIL import ImageGrab
from pyautogui import rightClick
import keyboard
import time

from configs.config_reader import Config

Active = False
time_wait_minigame = Config.get_config(0, 'settings').time_wait_minigame
point_cords = Config.get_config(1, 'coordinates').coordinates
background_color = Config.get_config(2, 'colors').background
cursor_color = Config.get_config(2, 'colors').cursor
target_color = Config.get_config(2, 'colors').target
print(time_wait_minigame)
print(background_color, cursor_color, target_color)
print(point_cords)


def main():
    t = False
    timer = 0

    while Active:
        c = 0
        s = 0

        px = ImageGrab.grab().load()
        for cord in point_cords:
            pixel = px[cord[0], cord[1]]
            if pixel != target_color:
                c += 1
            if pixel == background_color:
                s += 1

        if s >= 7:
            if c == 10:
                rightClick(point_cords[5])
                time.sleep(0.17)
            if t:
                t = False
                timer = 0
        elif t == False or round(time.time()) - timer >= time_wait_minigame:
            rightClick(point_cords[5])
            t = True
            timer = round(time.time())


def switch_Active(ok):
    global Active
    print(ok)
    if not Active:
        Active = True
        print(Active)
        main()
    else:
        Active = False
        print(Active)


if __name__ == "__main__":
    keyboard.on_release_key("q", switch_Active)
    keyboard.wait()
