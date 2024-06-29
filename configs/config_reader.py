import logging
import os
import io
import json
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

    def config_fixing(self, conf, conf_source, conf_target):
        try:
            print("Начато восстановление конфига")
            config_logger.info("Начато восстановление конфига")
            os.remove(conf_target)
            copy(conf_source, conf_target)

        except Exception as Error:
            print(f"Критическая ошибка при восстановлении конфига {conf}: \n{Error}")
            config_logger.critical(f"Критическая ошибка при восстановлении конфига {conf}", exc_info=True)
            time.sleep(5)
            os.close(1)

        else:
            print(f"Конфиг {conf} был успешно восстановлен")
            config_logger.debug(f"Конфиг {conf} был успешно восстановлен")

    def config_check_totality(self, conf):
        fixed_config = False
        conf_target = os.path.join(self.CONFIG_DIR, conf)
        conf_source = os.path.join(self.this_dir, conf)
        print(f"Проверка целостности конфига: {conf}")
        config_logger.info(f"Проверка целостности конфига: {conf}")

        try:
            if not os.path.exists(conf_target):
                print(f"Конфиг {conf} не найден")
                config_logger.info(f"Конфиг {conf} не найден")
                self.config_fixing(conf, conf_source, conf_target)
                fixed_config = True

            else:
                print(f"Конфиги на месте\nНачата проверка настроек")
                try:
                    with io.open(conf_target) as json_config:
                        damaged_data = json.load(json_config)

                except:
                    print(f"Конфиг: {conf} повреждён")
                    config_logger.info(f"Конфиг: {conf} повреждён")
                    self.config_fixing(conf, conf_source, conf_target)
                    fixed_config = True
                else:
                    config_logger.info("Повреждённый конфиг успешно открыт")


                try:
                    with io.open(conf_source) as json_config:
                        data = json.load(json_config)

                except Exception as Error:
                    print(f"Критическая ошибка при открытии исходного конфига: \n{Error}")
                    config_logger.critical("Критическая ошибка при открытии исходного конфига", exc_info=True)
                    time.sleep(5)
                    os.close(1)
                else:
                    config_logger.debug("Исходный конфиг успешно открыт")

                    for jkey in data:
                        if isinstance(damaged_data[jkey], type(data[jkey])):
                            print(f"Настройка {jkey} в конфиге {conf} цела")
                            config_logger.info(f"Настройка {jkey} в конфиге {conf} цела")

                        else:
                            print(f"Настройка {jkey} конфиге: {conf} повреждёна\nПересоздаю конфиг...")
                            config_logger.info(f"Настройка {jkey} конфиге: {conf} повреждёна")
                            os.remove(conf_target)
                            copy(conf_source, conf_target)
                            fixed_config = True
                            break
        except:
            print(f"Конфиг: {conf} вероятно повреждён")
            config_logger.critical(f"Конфиг: {conf} вероятно повреждён")
            self.config_fixing(conf, conf_source, conf_target)
            fixed_config = True

        if not fixed_config:
            print(f"Конфиг {conf} полностью цел")
            config_logger.info(f"Конфиг {conf} полностью цел")
        time.sleep(1)
        os.system("cls")
        os.system("clear")

    def configs_totality_fix(self):
        time.sleep(1)
        print("Начата проверка на целостность конфигов")
        config_logger.info("Начата проверка на целостность конфигов")

        os.system("cls")
        os.system("clear")

        try:
            if not os.path.isdir(self.CONFIG_DIR): os.mkdir(self.CONFIG_DIR)
            for jf in os.listdir(self.this_dir):
                if jf.endswith('.json'):
                    self.config_check_totality(jf)

        except Exception as Error:
            print(f"Критическая ошибка проверки целостности конфигов: {Error}")
            print("Сообщите об ошибке разработчику")
            config_logger.critical("Критическая ошибка проверки целостности конфигов", exc_info=True)
            time.sleep(5)
            os.close(1)

    def get_config(self, config_file: str, key):
        while 1:
            try:
                full_path = os.path.join(self.CONFIG_DIR, f'{config_file}.json')
                config_logger.debug(f"Получен полный путь к {config_file}.json")

                with io.open(full_path, 'r') as json_config:
                    data = json.load(json_config)

                config_logger.info(f"Получены данные из {config_file}")
                config_logger.debug(f"Данные из {config_file}: {data}")
                config_logger.debug(f"Возвращаемые данные: {data[key]}")
                return data[key]
            except Exception as Error:
                print(f"Ошибка при получении данных из конфига: \n{Error}\nЗапускаю проверку целостности конфигов")
                config_logger.error("Ошибка при получении данных из конфига\nЗапускаю проверку целостности конфигов", exc_info=True)
                self.configs_totality_fix()
