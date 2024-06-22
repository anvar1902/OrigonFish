import os
import json
import codecs
from shutil import copy, copyfile

CONFIG_DIR = "configs"

class Config:
    def __init__(self, type_config: int, data: dict):
        if type_config == 0:
            # coordinates.json
            self.coordinates = data['coordinates']
        elif type_config == 1:
            # colors.json
            self.background = tuple(data['background'])
            self.cursor = tuple(data['cursor'])
            self.target = tuple(data['target'])

    @staticmethod
    def get_config(type_config: int, config_file: str) -> dict:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR)
        if not os.path.exists(os.path.join(CONFIG_DIR, "coordinates.json")): copy(os.path.join(this_dir, "coordinates.json"), os.path.join(CONFIG_DIR, "coordinates.json"))
        if not os.path.exists(os.path.join(CONFIG_DIR, "colors.json")): copy(os.path.join(this_dir, "colors.json"), os.path.join(CONFIG_DIR, "colors.json"))

        full_path = os.path.join(CONFIG_DIR, f'{config_file}.json')
        with codecs.open(full_path, 'r', encoding='utf-8') as config:
            data = json.load(config)
        return Config(type_config, data)