import os

from logic import OrigonFish
from auto_updater import Updater
from configs.config_reader import Config

CURRECT_VERSION = "0.0.1"
URL = "https://github.com/anvar1902/OrigonFish"
#PROGRAM_NAME = "OrigonFish.exe"
UPDATER_NAME = "updater.exe"
UPDATER_TAG = "updater"

PROGRAM_NAME = "main.exe"

if __name__ == "__main__":
    #os.remove(UPDATER_NAME)
    AutoUpdater = Updater(CURRECT_VERSION, URL, PROGRAM_NAME, UPDATER_NAME, UPDATER_TAG)
    print("\n".join(["Aya", "AyaT", "AyaL"]))
    if not Config.get_config(0, "settings").skip_updates:
        AutoUpdater.check_new_version()
    OrigonFish()
