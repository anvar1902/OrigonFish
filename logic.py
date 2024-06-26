from PIL import ImageGrab
from pyautogui import rightClick
import keyboard
import logging
import time
import os

from configs.config_reader import Config

if not os.path.isdir("logs"): os.mkdir("logs")
logic_logger = logging.getLogger(__name__.split('.')[-1])
logic_logger.setLevel(logging.DEBUG)

log_handler = logging.FileHandler("logs/" + __name__.split('.')[-1] + ".log", mode='w')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
logic_logger.addHandler(log_handler)

conf = Config()

class OrigonFish:
    def __init__(self):
        print("Загружаем настройки...")
        logic_logger.info("Загружаем настройки...")

        try:
            self.Active = False
            self.time_wait_minigame = conf.get_config('settings', 'time_wait_minigame')
            print(self.time_wait_minigame)
            logic_logger.info("Настройки регулирования успешно загружены")
            logic_logger.debug(self.time_wait_minigame)

            self.point_cords = conf.get_config('coordinates', 'coordinates')
            print(self.point_cords)
            logic_logger.info("Координаты успешно загружены")
            logic_logger.debug(self.point_cords)

            self.background_color = conf.get_config('colors', 'background')
            self.cursor_color = conf.get_config('colors', 'cursor')
            self.target_color = conf.get_config('colors', 'target')
            print(self.background_color, self.cursor_color, self.target_color)
            logic_logger.info("Цвета успешно загружены")
            logic_logger.debug((self.background_color, self.cursor_color, self.target_color))

            keyboard.on_release_key('q', self.switch_Active)
            logic_logger.debug("Клавиша q успешно привязана к функции switch_Active")

        except Exception as Error:
            print("Ошибка при загрузки настроек: \n", Error)
            print("Обратитесь за помощью к разработчику")
            logic_logger.critical("Критическая ошибка при загрузке настроек", exc_info=True)
            time.sleep(5)
            exit()

        else:
            print("Все настройки успешно загружены")
            logic_logger.info("Все настройки успешно загружены")

        time.sleep(1)
        os.system("clear")
        os.system("cls")
        self.check_screen_process()

    def check_screen_process(self):
        t = False
        timer = 0
        logic_logger.debug("Запуск основной части программы")

        while 1:
            while self.Active:
                c = 0
                s = 0

                try:
                    logic_logger.debug("Началась проверки пикселей")
                    px = ImageGrab.grab().load()
                    logic_logger.debug("Изображение успешно получено")
                    for cord in self.point_cords:
                        pixel = px[cord[0], cord[1]]
                        if pixel != self.target_color:
                            c += 1
                        if pixel == self.background_color:
                            s += 1
                except Exception as Error:
                    print(f"Критическая ошибка при проверки пикселей: \n{Error}")
                    print("Обратитесь за помощью к разработчику")
                    logic_logger.error("Критическая ошибка при проверке пикселей", exc_info=True)
                    time.sleep(5)
                    exit()
                else:
                    logic_logger.debug("Успешно закончилась проверка пикселей")


                try:
                    logic_logger.debug("Начата проверка полученных данных")
                    if s >= 7:
                        logic_logger.debug("Найдена мини игра")
                        if c == 10:
                            rightClick(self.point_cords[5])
                            logic_logger.debug(f"Был сделан правый клик на: {self.point_cords[5]}")
                            logic_logger.debug("Нажатие по цели")
                            time.sleep(0.17)
                        if t:
                            t = False
                            timer = 0
                            logic_logger.debug(f"Сброшен t и timer")
                    elif t == False or round(time.time()) - timer >= self.time_wait_minigame:
                        logic_logger.debug(f"Был сделан правый клик на: {self.point_cords[5]}")
                        logic_logger.debug("Кидание удочки")
                        rightClick(self.point_cords[5])
                        t = True
                        timer = round(time.time())
                        logic_logger.debug(f"t = True и начат таймер")
                except Exception as Error:
                    logic_logger.critical("Критическая ошибка при проверки данных")
                    print(f"Критическая ошибка при проверке данных: \n{Error}")
                    print("Обратитесь за помощью к разработчику")
                    time.sleep(5)
                    exit()
                else:
                    logic_logger.debug("Проверка данных успешно завершилась")

    def switch_Active(self, ok):
        self.Active = not self.Active
        print(self.Active)
        logic_logger.info(f"Состояние Active переключено на: {self.Active}")

if __name__ == "__main__":
    main_prog = OrigonFish()