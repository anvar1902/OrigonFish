import os
import keyboard
import logging

from logic import OrigonFish
from auto_updater import Updater
from configs.config_reader import Config


logging.basicConfig(
                    level=logging.DEBUG,
                    filename="logs/" + __name__.split('.')[-1] + ".log",
                    filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s"
                    )


CURRECT_VERSION = "0.0.1"
URL = "https://github.com/anvar1902/OrigonFish"
PROGRAM_NAME = "OrigonFish.exe"

if __name__ == "__main__":
    if not os.path.isdir("logs"): os.mkdir("logs")
    AutoUpdater = Updater(CURRECT_VERSION, URL, PROGRAM_NAME)
    if not Config.get_config(0, "settings").skip_updates:
        AutoUpdater.check_new_version()

    main_prog = OrigonFish()
