import os
import glob
import json
import codecs
from shutil import copy, copyfile



class Config:
    def __init__(self, type_config: int, data: dict):
        if type_config == 0:
            # settings.json
            self.time_wait_minigame = data['time_wait_minigame']
            self.skip_updates = data['skip_updates']
        elif type_config == 1:
            # coordinates.json
            self.coordinates = data['coordinates']
        elif type_config == 2:
            # colors.json
            self.background = tuple(data['background'])
            self.cursor = tuple(data['cursor'])
            self.target = tuple(data['target'])

    @staticmethod
    def get_config(type_config: int, config_file: str) -> dict:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        CONFIG_DIR = "configs"
        if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR)
        for jf in os.listdir():
            if jf.endswith('.json'):
                if not os.path.exists(os.path.join(CONFIG_DIR, jf)):
                    copy(os.path.join(this_dir, jf), os.path.join(CONFIG_DIR, jf))

        full_path = os.path.join(CONFIG_DIR, f'{config_file}.json')
        with codecs.open(full_path, 'r', encoding='utf-8') as config:
            data = json.load(config)
        return Config(type_config, data)