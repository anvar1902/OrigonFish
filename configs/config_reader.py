import logging
import os
import json
import codecs
import time
from shutil import copy

if not os.path.isdir("logs"): os.mkdir("logs")
config_logger = logging.getLogger(__name__.split('.')[-1])
config_logger.setLevel(logging.DEBUG)

log_handler = logging.FileHandler("logs/" + __name__.split('.')[-1] + ".log", mode='w')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
config_logger.addHandler(log_handler)

class Config:
    def __init__(self):
        self.CONFIG_DIR = "configs"
        self.this_dir = os.path.dirname(os.path.abspath(__file__))

    def config_totality_fix(self):
        time.sleep(1)
        print("Начата проверка на целостность конфигов")
        config_logger.info("Начата проверка на целостность конфигов")

        os.system("cls")
        os.system("clear")

        try:
            if not os.path.isdir(self.CONFIG_DIR): os.mkdir(self.CONFIG_DIR)
            for jf in os.listdir(self.this_dir):
                if jf.endswith('.json'):
                    fixed_config = False
                    print(f"Проверка целостности конфига: {jf}")
                    config_logger.info(f"Проверка целостности конфига: {jf}")

                    if not os.path.exists(os.path.join(self.CONFIG_DIR, jf)):
                        copy(os.path.join(self.this_dir, jf), os.path.join(self.CONFIG_DIR, jf))
                        fixed_config = True

                    else:
                        print(f"Конфиги на месте\nНачата проверка настроек")
                        try:
                            try:
                                with codecs.open(os.path.join(self.this_dir, jf)) as json_config:
                                    data = json.load(json_config)
                                config_logger.debug("Исходный конфиг успешно открыт")

                                with codecs.open(os.path.join(self.CONFIG_DIR, jf)) as json_config:
                                    damaged_data = json.load(json_config)
                                config_logger.debug("Повреждённый конфиг успешно открыт")

                            except Exception as Error:
                                print(f"Критическая ошибка при открытии конфигов: \n{Error}")
                                config_logger.critical("Критическая ошибка при открытие конфигов", exc_info=True)
                                os.close(1)

                            for jkey in data:
                                    if isinstance(damaged_data[jkey], type(data[jkey])):
                                        print(f"Настройка {jkey} в конфиге {jf} цела")
                                        config_logger.info(f"Настройка {jkey} в конфиге {jf} цела")

                                    else:
                                        print(f"Настройка {jkey} конфиге: {jf} повреждёна\nПересоздаю конфиг...")
                                        config_logger.info(f"Настройка {jkey} конфиге: {jf} повреждёна")
                                        os.remove(os.path.join(self.CONFIG_DIR, jf))
                                        copy(os.path.join(self.this_dir, jf), os.path.join(self.CONFIG_DIR, jf))
                                        fixed_config = True
                                        break
                        except:
                            print(f"Конфиг: {jf} вероятно повреждён \nПересоздаю конфиг...")
                            config_logger.info(f"Конфиг: {jf} вероятно повреждён\nПересоздаю конфиг")

                            try:
                                os.remove(os.path.join(self.CONFIG_DIR, jf))
                                copy(os.path.join(self.this_dir, jf), os.path.join(self.CONFIG_DIR, jf))
                                fixed_config = True
                                print(f"Конфиг {jf} был успешно пересоздан")
                                config_logger.debug(f"Конфиг {jf} был успешно пересоздан")

                            except Exception as Error:
                                print(f"Критическая ошибка при пересоздании конфига: \n{Error}")
                                config_logger.critical("Критическая ошибка при пересоздании конфига", exc_info=True)
                                time.sleep(5)
                                os.close(1)

                    if not fixed_config:
                        print(f"Конфиг {jf} полностью цел")
                        config_logger.info(f"Конфиг {jf} полностью цел")
                    else:
                        print(f"Конфиг {jf} успешно восстановлен")
                        config_logger.info(f"Конфиг {jf} успешно восстановлен")
                    os.system("cls")
                    os.system("clear")

        except Exception as Error:
            print(f"Критическая ошибка проверки целостности конфигов: {Error}")
            print("Сообщите об ошибке разработчику")
            config_logger.error("Критическая ошибка проверки целостности конфигов", exc_info=True)
            time.sleep(5)
            os.close(1)

    def get_config(self, config_file: str, key):
        while 1:
            try:
                full_path = os.path.join(self.CONFIG_DIR, f'{config_file}.json')
                logging.debug(f"Получен полный путь к {config_file}.json")

                with codecs.open(full_path, 'r') as json_config:
                    data = json.load(json_config)

                config_logger.info(f"Получены данные из {config_file}")
                config_logger.debug(f"Данные из {config_file}: {data}")
                return data[key]
            except Exception as Error:
                print(f"Ошибка при получении данных из конфига: \n{Error}\nЗапускаю проверку целостности конфигов")
                config_logger.error("Ошибка при получении данных из конфига\nЗапускаю проверку целостности конфигов", exc_info=True)
                self.config_totality_fix()