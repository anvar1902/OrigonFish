import os
import logging

from logic import OrigonFish
from auto_updater import Updater
from configs.config_reader import Config

if not os.path.isdir("logs"): os.mkdir("logs")
main_logger = logging.getLogger(__name__.split('.')[-1])
main_logger.setLevel(logging.DEBUG)

log_handler = logging.FileHandler("logs/" + __name__.split('.')[-1] + ".log", mode='w')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
main_logger.addHandler(log_handler)
main_logger.debug("Логгер запущен")

all_log_handler = logging.FileHandler("logs/all.log", mode='w')
logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[all_log_handler,]
                    )


CURRECT_VERSION = "1.1.1"
URL = "https://github.com/anvar1902/OrigonFish"
PROGRAM_NAME = "OrigonFish.exe"
main_logger.debug("Инициализация начальных настроек")
main_logger.debug((CURRECT_VERSION, URL, PROGRAM_NAME))

conf = Config()
main_logger.debug("Создан экземпляр класса Config")

if __name__ == "__main__":
    AutoUpdater = Updater(CURRECT_VERSION, URL, PROGRAM_NAME)
    main_logger.debug("Создан экземпляр класса Updater")

    if not conf.get_config("settings", 'skip_updates'):
        main_logger.debug("Запуск проверки на новую версию программы")
        AutoUpdater.check_new_version()

    main_logger.debug("Создан экземпляр класса OrigonFish")
    main_logger.debug("Запущена мини игра")
    main_prog = OrigonFish()
