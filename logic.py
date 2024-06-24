from PIL import ImageGrab
from pyautogui import rightClick
import keyboard
import time
import os

from configs.config_reader import Config



class OrigonFish:
    def __init__(self):
        print("Загружаем настройки...")
        self.Active = False
        self.time_wait_minigame = Config.get_config(0, 'settings').time_wait_minigame
        print(self.time_wait_minigame)
        self.point_cords = Config.get_config(1, 'coordinates').coordinates
        print(self.point_cords)
        self.background_color = Config.get_config(2, 'colors').background
        self.cursor_color = Config.get_config(2, 'colors').cursor
        self.target_color = Config.get_config(2, 'colors').target
        print(self.background_color, self.cursor_color, self.target_color)
        keyboard.on_release_key("q", self.switch_Active)
        print("Все настройки успешно загружены")
        os.system("clear")
        os.system("cls")
        keyboard.wait()

    def check_screen_process(self):
        t = False
        timer = 0

        while self.Active:
            c = 0
            s = 0

            px = ImageGrab.grab().load()
            for cord in self.point_cords:
                pixel = px[cord[0], cord[1]]
                if pixel != self.target_color:
                    c += 1
                if pixel == self.background_color:
                    s += 1

            if s >= 7:
                if c == 10:
                    rightClick(self.point_cords[5])
                    time.sleep(0.17)
                if t:
                    t = False
                    timer = 0
            elif t == False or round(time.time()) - timer >= self.time_wait_minigame:
                rightClick(self.point_cords[5])
                t = True
                timer = round(time.time())

    def switch_Active(self, ok):
        if not self.Active:
            self.Active = True
            print(self.Active)
            self.check_screen_process()
        else:
            self.Active = False
            print(self.Active)
