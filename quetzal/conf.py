import os
import n
import yaml



base_dir = os.path.dirname(n.__file__)



class LoadConfig:

    def __init__(self, config_file_path):
        yaml_file = open(base_dir + config_file_path)
        self._quetzal_config = yaml.load(yaml_file)
        yaml_file.close()

    def get_config(self):
        return self._quetzal_config




class QuetzalConfig:
    @staticmethod
    def load(file_path='/app.yaml'):
        quetzal_config = LoadConfig(file_path)
        return quetzal_config.get_config()
